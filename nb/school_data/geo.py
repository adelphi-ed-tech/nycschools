import pandas as pd
import geopandas as gpd
import folium

# school data points
# https://data.cityofnewyork.us/Education/2019-2020-School-Point-Locations/a3nt-yts4

def load_school_locations(refresh=False):

    filename = "school_locations.geojson"
    if not refresh:
        try:
            df =  gpd.read_file(filename)
        except FileNotFoundError:
            geojsonurl = "https://data.cityofnewyork.us/resource/a3nt-yts4.geojson?$limit=1000000"
            df = gpd.read_file(geojsonurl)

            df = df.rename(columns={"xcoordinat":"x","ycoordinat":"y",})
            df.x = pd.to_numeric(df.x, errors='coerce')
            df.y = pd.to_numeric(df.y, errors='coerce')
            df = df[df.x > 0]
            df["dbn"] = df.ats_code

            df = df[["x","y","dbn","zip","loc_name"]]

            url = "https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000"
            loc2 = pd.read_csv(url)
            loc2["dbn"] = loc2.system_code
            cols = [
                'dbn',
                'administrative_district_code',
                'administrative_district_name',
                'beds',
                'borough_block_lot',
                'census_tract',
                'community_district',
                'community_district_1',
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

            loc2 = loc2[cols]

            df = df.merge(loc2, on="dbn", how="left")
            df.to_json(filename, index=False)

    return df


def load_districts(refresh=False):
    districts = gpd.read_file("https://data.cityofnewyork.us/api/geospatial/r8nu-ymqj?method=export&format=GeoJSON")
    # rename the columns
    districts.columns = ['district', 'area', 'length', 'geometry']
    districts.district = pd.to_numeric(districts.district, downcast='integer', errors='coerce')
    districts = districts.to_crs(epsg=4326)
    return districts

def add_labels(ax, df, col, fontsize=14):
    def label(row):
        xy=row.geometry.centroid.coords[0]
        ax.annotate(row[col], xy=xy, ha='center', fontsize=fontsize)

    df.apply(label, axis=1)
