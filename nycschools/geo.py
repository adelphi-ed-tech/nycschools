# NYC School Data
# Copyright (C) 2022. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU AFFERO GENERAL PUBLIC LICENSE (the "License") as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
from nycschools import datasets, dataloader
import pandas as pd
import geopandas as gpd
import os
import os.path
from datetime import datetime

from requests import Session
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import config, schools
from .dataloader import load

urls = config.urls
school_location_file = os.path.join(config.data_dir, urls["school_locations"].filename)

def load_zipcodes():
    """Load the NYC zip code boundaries as a GeoDataFrame from data_dir.
    Zip codes are compiled from the NYC Data Portal via the US Post Office"""
    df = load(urls["zipcodes"].filename)
    return df


def load_school_footprints():
    """Get the shapes for school building footprints"""
    gdf = load(urls["building_footprints"].school_footprints_file)
    return gdf

def load_city_footprints():
    """Get the shapes for all building footprints in the New York City."""
    path = config.urls["building_footprints"].city_footprints_feather
    df = load(path, gdf=True)
    all_feet = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    return all_feet

def load_district_neighborhoods():
    """Loads district number and neighborhood names"""
    df = load(urls["neighborhoods"].districts_filename)
    return df

def load_neighborhoods():
    """Load point data with neighborhood names"""
    df = load(urls["neighborhoods"].filename)
    return df

def load_school_locations():
    """Returns a GeoDataFrame with the school locations and location meta-data"""

    try:
        df = load(urls["school_locations"].filename)
        return df
    except Exception as e: # geopandas throws DriveError, but I don't know where to import it to catch it
        if e.type != "<class 'fiona.errors.DriverError'>":
            raise e

def load_school_geo_points():
    """Load only the school location points as a GeoDataFrame"""
    df = load_school_locations()
    return df[["dbn", "x", "y", "geometry"]]


def merge_districts(names):
    """Merge district number and neighborhood names"""
    districts = load_districts()

    def get_names(district):
        d = districts[districts.district == district]
        t = names[names.geometry.within(d.geometry.iloc[0])]
        t = ", ".join(t.neighborhood)
        return (district, t)

    df = pd.DataFrame(columns=["district", "neighborhood"], data=[ get_names(d) for d in districts.district])
    return df


def get_neighborhoods(geojsonurl=urls["neighborhoods"].url):
    """Read NYC neighborhood names from the Open Data Portal GeoJSON URL"""

    df = gpd.read_file(geojsonurl)
    df = df.rename(columns={"name": "neighborhood", "borough": "boro"})
    df = df[["neighborhood", "boro", "geometry"]]
    path = os.path.join(config.data_dir, urls["neighborhoods"].filename)
    df.to_file(path, driver="GeoJSON")
    dist_names = merge_districts(df)

    path = os.path.join(config.data_dir, urls["neighborhoods"].districts_filename)
    dist_names.to_csv(path, index=False)
    
    return df


def get_and_save_locations(filename=school_location_file):
    points = get_points()
    locations = get_locations()
    df = points.merge(locations, on="dbn", how="left")
    df.open_year = df.open_year.fillna(0)
    df.open_year = df.open_year.astype(int)
    out = df.copy()
    out.to_file(filename, driver="GeoJSON")
    return df

def get_points(geojsonurl=urls["school_geo"].url):
    """Read the school location points and zipcodes from an Open Data Portal GeoJSON URL"""
    # this is the API feed for the location points
    # it's the best place to get zip codes

    points = gpd.read_file(geojsonurl)
    cols = {
        'ATS': "dbn",
        'Geographic': "geo_district",
        'geometry': 'geometry'
    }
    points.rename(columns=cols, inplace=True)
    points = points[cols.values()]
    points["district"] = points.dbn.apply(lambda x: int(x[0:2]))


    zips = load_zipcodes()
    points.to_crs(zips.crs, inplace=True)
    points = gpd.sjoin(points, zips, how='left', predicate='within')


    points.drop(columns=['index_right'], inplace=True)
    points.zip = points.zip.astype(int)
    return points


def get_locations(url=urls["school_locations"].url):
    """
       Read school level data with many location-related columns: school x,y
       coords, and data about the school locations including NYS BEDS ids,
       census tract, and police precinct.
    """

    locations = pd.read_csv(url)
    locations = locations.drop_duplicates()
    locations["dbn"] = locations.system_code
    cols = [
        'dbn',
        'administrative_district_code',
        'administrative_district_name',
        'beds',
        'borough_block_lot',
        'census_tract',
        'community_district',
        'community_school_sup_name',
        'council_district',
        'fax_number',
        'fiscal_year',
        'geographical_district_code',
        'grades_final_text',
        'grades_text',
        'highschool_network',
        'highschool_network_location',
        'highschool_network_name',
        'latitude',
        'location_category_description',
        'location_code',
        'location_name',
        'location_type_description',
        'longitude',
        'managed_by_name',
        'nta',
        'nta_name',
        'open_date',
        'state_code',
        'status_descriptions']

    locations = locations[cols]
    locations["bbl"] = locations.borough_block_lot.apply(lambda x: str(x).split(".")[0])
    locations.beds = locations.beds.astype("string")
    locations.open_date = locations.open_date.fillna(0)
    locations.open_date = locations.open_date.apply(lambda x: int(str(x).split('-')[0] if x != 0 else 0))
    locations.rename(columns={"open_date": "open_year"}, inplace=True)
    return locations


def get_school_footprints():
    """Load all building footprints from the NYC Dept of Buildings
    Open Data Portal. Merge these shapes with school locations
    and save the footprints. Because of the size of the DOB data,
    a compressed (.feather) version is loaded from local or data.mixi.nyc.
    If this file is not found, the method fails."""
    print("Getting footprints from URL")
    url=urls["building_footprints"].url
    foot = load(url, gdf=True)
    foot.columns = [c.lowercase() for c in foot.columns]
    foot["bbl"] = foot.base_bbl.astype(str)
    foot.mpluto_bbl = foot.mpluto_bbl.astype(str)
    # saving local feather
    city_path = os.path.join(config.data_dir, urls["building_footprints"].city_footprints_feather)
    foot.to_feather(city_path)

    # merging with point locations for dbn
    school_loc = get_points()
    school_foot = foot.merge(school_loc[["dbn","bbl"]], on="bbl", how="inner")
    # saving to data dir
    school_path = os.path.join(config.data_dir, urls["building_footprints"].school_footprints_file)
    school_foot.to_file(school_path, driver="GeoJSON")
    return school_foot

def load_districts(url="foo"):
    """Get geo shape file for NYC school districts, indexed by district number."""
    # districts = gpd.read_file(url)
    districts = load(urls["district_geo"].filename)
    districts.district = districts.district.astype(int)
    districts = districts.to_crs(epsg=4326)
    return districts

def merge_campus_id(df):
    """Merges the campus_id into an DataFrame that has a 'dbn' column."""
    campus_dbn_file = urls["campus"].merge_filename
    # campus_dbn_file = os.path.join(config.data_dir, campus_dbn_file)
    # campus_dbn = dataloader.read_file(campus_dbn_file)
    campus_dbn = load(campus_dbn_file)
    df = df.merge(campus_dbn, on="dbn", how="left")
    df.campus_id = df.campus_id.astype("Int64")
    return df

def get_campuses():
    """Get the school campus data"""
    campus_file = urls["campus"].filename
    return load(campus_file)
    # campus_file = os.path.join(config.data_dir, urls["campus"].filename)
    # return dataloader.read_file(campus_file)

def create_campuses():
    """Create school campuses with deomgraphic data.
       A campus is a school building/location that houses one
       or more school. School campuses are only for the most
       recent academic year.
    """

    loc = load_school_locations()
    demos = schools.load_school_demographics()
    # join demographics to our locations for the most recent year
    demos = demos[demos.ay == demos.ay.max()]
    loc.drop(columns=["geo_district", "district", "zip", "beds"], inplace=True)
    loc = loc.merge(demos, on='dbn', how='inner')


    # let's find all the colocated schools by matching schools with the same point
    campuses = pd.DataFrame()
    # give each location an id
    campuses["geometry"] = loc.geometry.unique()
    campuses["campus_id"] = campuses.index + 1
    # give each location a campus id
    df = loc.merge(campuses, on="geometry", how="inner")
    # sort locations by size (descending) so the largest school on each campus appears "first"
    df = df.sort_values(by=["campus_id", "open_year"], ascending=True)
    campuses = df.groupby("campus_id").agg(
        num_schools=("dbn", "count"),
        campus=("school_name", "first"),
        open_year=("open_year", "first"),
        total_enrollment=("total_enrollment", "sum"),
        female_n=("female_n", "sum"),
        male_n=("male_n", "sum"),
        asian_n=("asian_n", "sum"),
        black_n=("black_n", "sum"),
        hispanic_n=("hispanic_n", "sum"),
        white_n=("white_n", "sum"),
        max_white_pct=("white_pct", "max"),
        min_white_pct=("white_pct", "min"),
        swd_n=("swd_n", "sum"),
        ell_n=("ell_n", "sum"),
        max_ell_pct=("ell_pct", "max"),
        min_ell_pct=("ell_pct", "min"),
        poverty_n=("poverty_n", "sum"),
        max_poverty_pct=("poverty_pct", "max"),
        min_poverty_pct=("poverty_pct", "min"),
        geometry=("geometry", "first")
    ).reset_index()

    campuses["white_diff"] = campuses.max_white_pct - campuses.min_white_pct
    campuses["ell_diff"] = campuses.max_ell_pct - campuses.min_ell_pct
    campuses["poverty_diff"] = campuses.max_white_pct - campuses.min_white_pct


    campuses['female_pct'] = campuses['female_n'] / campuses['total_enrollment']
    campuses['male_pct'] = campuses['male_n'] / campuses['total_enrollment']
    campuses['asian_pct'] = campuses['asian_n'] / campuses['total_enrollment']
    campuses['black_pct'] = campuses['black_n'] / campuses['total_enrollment']
    campuses['hispanic_pct'] = campuses['hispanic_n'] / campuses['total_enrollment']
    campuses['white_pct'] = campuses['white_n'] / campuses['total_enrollment']
    campuses['swd_pct'] = campuses['swd_n'] / campuses['total_enrollment']
    campuses['ell_pct'] = campuses['ell_n'] / campuses['total_enrollment']
    campuses['poverty_pct'] = campuses['poverty_n'] / campuses['total_enrollment']

    campuses["plurality"] = campuses[['asian_n', 'black_n', 'hispanic_n', 'white_n']].idxmax(axis=1)
    campuses.plurality = campuses.plurality.str.replace("_n", "")

    campuses = gpd.GeoDataFrame(campuses, geometry="geometry")
    campuses.set_crs(loc.crs, inplace=True)

    # save the data files for later use
    campus_file = urls["campus"].filename
    campus_file = os.path.join(config.data_dir, urls["campus"].filename)
    dataloader.write_file(campuses, campus_file)
    
    campus_dbn = df[["campus_id", "dbn"]]
    campus_dbn_file = urls["campus"].merge_filename
    campus_dbn_file = os.path.join(config.data_dir, campus_dbn_file)
    dataloader.write_file(campus_dbn, campus_dbn_file)
    
    return campuses
