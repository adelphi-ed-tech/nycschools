import pandas as pd
import geopandas as gpd
import folium

# school data points
# https://data.cityofnewyork.us/Education/2019-2020-School-Point-Locations/a3nt-yts4

def load_school_locations(refresh=False):

    filename = "school_locations.csv"
    if not refresh:
        try:
            df =  pd.read_csv(filename)
        except FileNotFoundError:
            url = "https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000"
            df = pd.read_csv(url)
            df.to_csv(filename, index=False)

    # duplicate some cols for aliases
    df["dbn"] = df.system_code
    df["x"] = df.longitude
    df["y"] = df.latitude

    # drop rows that might be missing geolocation data or have bad data
    df = df[df.x.notnull() & df.y.notnull()]
    df = df[df.y > 0]

    geo = gpd.points_from_xy(x=df.x,y=df.y)
    districts = gpd.GeoDataFrame(df, geometry=geo, crs="EPSG:4326")

    return districts


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
