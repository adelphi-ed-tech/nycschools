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
from nycschools import datasets
import pandas as pd
import geopandas as gpd
from bs4 import BeautifulSoup
import requests
import os
import os.path
from datetime import datetime


from . import config
urls = config.urls
school_location_file = os.path.join(config.data_dir, "school_locations.geojson")

def load_zipcodes():
    """Load the NYC zip code boundaries as a GeoDataFrame from data_dir.
    Zip codes are compiled from the NYC Data Portal via the US Post Office"""
    df = gpd.read_file(os.path.join(config.data_dir,urls["zipcodes"].filename))
    return df

def load_school_locations():
    """Returns a GeoDataFrame with the school locations and location meta-data"""

    try:
        df = gpd.read_file(school_location_file)
        # convert df.open_date to an int
        df.open_date = df.open_date.apply(lambda x: x.year)
        df.open_date = df.open_date.fillna(0).astype(int)
        return df
    except Exception as e: # geopandas throws DriveError, but I don't know where to import it to catch it
        if e.type != "<class 'fiona.errors.DriverError'>":
            raise e

    return get_and_save_locations()


def load_school_geo_points():
    """Load only the school location points as a GeoDataFrame"""
    df = load_school_locations()
    return df[["dbn", "x", "y", "geometry"]]

def get_and_save_locations(filename=school_location_file):
    points = get_points()
    locations = get_locations()
    points = points.merge(locations, on="dbn", how="left")
    df = gpd.GeoDataFrame(points)
    df.to_file(filename, driver="GeoJSON")
    return df

def get_points(geojsonurl=urls["school_geo"].url):
    """Read the school location points and zipcodes from an Open Data Portal GeoJSON URL"""
    # this is the API feed for the location points
    # it's the best place to get zip codes

    df = gpd.read_file(geojsonurl)
    df = df.drop_duplicates()

    df = df.rename(columns={"xcoordinat":"x","ycoordinat":"y",})
    df.x = pd.to_numeric(df.x, errors='coerce')
    df.y = pd.to_numeric(df.y, errors='coerce')
    df = df[df.x > 0]
    df.bbl = df.bbl.astype(str)
    df.bbl = df.bbl.str.replace(".0", "")
    df["dbn"] = df.ats_code
    df["district"] = df.adimindist.astype(int)
    df = df.rename(columns={"geodistric":"geo_district"})
    cols = ['dbn', 'zip', 'geo_district', 'district', 'x','y', 'bbl', 'geometry']

    df = df[cols]
    df.zip = df.zip.astype("string")
    return df

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
        'police_precinct',
        'primary_building_code',
        'principal_name',
        'principal_phone_number',
        'principal_title',
        'state_code',
        'status_descriptions']

    locations = locations[cols]
    locations.beds = locations.beds.astype("string")
    locations.open_date = locations.open_date.apply(lambda x: int(str(x).split('-')[0]))
    return locations

def load_school_footprints():
    path = os.path.join(config.data_dir, urls["building_footprints"].school_footprints_file)
    gdf = gpd.read_file(path)
    return gdf

def load_city_footprints():
    path = os.path.join(config.data_dir, urls["building_footprints"].city_footprints_feather)
    gdf = gpd.read_file(path)

    return gdf


def get_school_footprints():
    """Load all building footprints from the NYC Dept of Buildings
    Open Data Portal. Merge these shapes with school locations
    and save the footprints"""
    print("Getting footprints from URL")
    url=urls["building_footprints"].url
    foot = gpd.read_file(url)
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

def load_districts(url=urls["district_geo"].url):
    """Get geo shape file for NYC school districts, indexed by district number."""
    districts = gpd.read_file(url)
    # rename the columns
    districts.columns = ['district', 'area', 'length', 'geometry']
    districts.district = pd.to_numeric(districts.district, downcast='integer', errors='coerce')
    districts = districts.to_crs(epsg=4326)
    return districts

