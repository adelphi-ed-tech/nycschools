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

from requests import Session
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

from concurrent.futures import ThreadPoolExecutor, as_completed


from . import config
from .dataloader import load


import subprocess

def wget(url, destination):
    """Use system wget to download a file"""
    try:
        subprocess.run(['wget', '-q', '-O', destination, url], check=True)
        return destination
    except subprocess.CalledProcessError as e:
        if e.returncode == 8:
            print("There was a server error, possibly a 404 or similar.")
        else:
            print(f"Download failed with error code: {e.returncode}")
        return None


def load_snapshots():
    """
    Loads the "snapshot" data from the NYC DOE data portal.
    This data contains core columns only for all "school types"
    mainly focusing on school demographics and teacher demographics.
    """
    filename = config.urls["snapshots"].filename
    df = load(filename)
    
    return make_geo(df)


def fix_ethnicity(df):
    data = df.copy()
    race_cols = ['race_asian_pct', 'race_black_pct', 'race_hispanic_pct', 'race_white_pct']

    def cp_eth(row, col):
        race = col.split("_")[1]
        col_n = f"ethnicity_{race}_n"
        col_raw = f"ethnicity_{race}_pct_raw"
        if pd.isnull(row[col_n]):
            pct = row[col]
            if isinstance(pct, str) and pct.endswith("%"):
                pct = pct[:-1]
            pct = float(pct)

            pct = float(pct) / 100
            n = int(row["enrollment"] * pct)
            row[col_n] = n
            row[col_raw] = pct
        row[col_n] = int(row[col_n])
        return row

    def fix_eth(row):
        for col in race_cols:
            row = cp_eth(row, col)
        return row


    data = data.apply(fix_eth, axis=1)
    data.drop(columns=race_cols, inplace=True)
    return data

def fix_pct(df):
    pct_cols = [c for c in df.columns if c.endswith( "pct") or c == "attendance_rate"]


    def pct(row):
        for col in pct_cols:
            if pd.isnull(row[col]):
                row[col] = 0.0
                continue
            pct = row[col]
            try:
                pct = float(pct)
            except:
                if pct.endswith("%"):
                    pct = pct[:-1]
                    pct = float(pct) / 100
                elif "fewer than 5" in pct:
                    pct = .01
            row[col] = pct
        return row


    df = df.apply(pct, axis=1)
    return df

def fix_admissions(df):
    data = df.copy()
    zone_map = {
        "Zoned School": "Zoned",
        "Zoned": "Zoned",
        "Choice School": "Choice",
        "Non-Zoned": "Non-Zoned",
        "Non-Zoned School": "Non-Zoned",
        "charter lottery": "Charter Lottery",
        "Zoned, District G&T": "Zoned, District G&T",
        "District G&T, Zoned": "Zoned, District G&T",
        "Citywide G&T School": "Citywide G&T",
        "Gifted & Talented School": "Citywide G&T",
        "G&T Only School": "Non-Zoned, District G&T",
        "Non-Zoned, District G&T": "Non-Zoned, District G&T",
        "District G&T, Non-Zoned": "Non-Zoned, District G&T"
    }

    data.all_es_admissionsmethods = data.all_es_admissionsmethods.map(zone_map)
    return data

def fix_colocations(df):
    data = df.copy()
    data["colocated"] = data.co_located.apply(lambda x: False if x == 'No' or not x else True)
    data["colocated_schools"] = data.co_located

    def colo(x):
        if x == "No" or not x or x == "Yes":
            return ""
        if "(" in x:
            start = x.find("(")
            end = x.find(")")
            return x[start+1:end]
        if "[" in x:
            start = x.find("[")
            end = x.find("[")
            return x[start+1:end]
        return ""


    data.colocated_schools = data["colocated_schools"].apply(colo)
    data["colocated_n"] = data.colocated_schools.apply( lambda x: 0 if len(x) == 0 else len(x.split(",")) + 1)
    return data


def rename_cols(col):
    col_map = {
        'location_name_long': 'school_name',
        'district': 'geo_district',
        'abbr_school_type': 'school_type',
        'enrollment': 'total_enrollment',
        'ethnicity_amerindian_n': 'amerindian_n',
        'ethnicity_amerindian_pct_raw': 'amerindian_pct',
        'ethnicity_asian_n': 'asian_n',
        'ethnicity_asian_pct_raw': 'asian_pct',
        'ethnicity_black_n': 'black_n',
        'ethnicity_black_pct_raw': 'black_pct',
        'ethnicity_hispanic_n': 'hispanic_n',
        'ethnicity_hispanic_pct_raw': 'hispanic_pct',
        'ethnicity_pacific_n': 'pacific_n',
        'ethnicity_pacific_pct_raw': 'pacific_pct',
        'ethnicity_white_n': 'white_n',
        'ethnicity_white_pct_raw': 'white_pct',
        'latitude': 'lat',
        'longitude': 'long',
        'x_coordinate': 'x',
        'y_coordinate': 'y',
    }

    if col in col_map:
        return col_map[col]
    if col.endswith("_raw"):
        return col[:-4]
    return col
    

def save_school_rank(df):

    drop = [
        'hs_rank1_pct',
        'hs_rank1_school_name',
        'hs_rank2_pct',
        'hs_rank2_school_name',
        'hs_rank3_pct',
        'hs_rank3_school_name',
        'hs_rank4_pct',
        'hs_rank4_school_name',
        'hs_rank5_pct',
        'hs_rank5_school_name',
    ]
    cols = [ 'dbn', 'ay', 'school_name', 'school_type' ] + drop
    next = df[cols].copy()
    next = next[next.hs_rank1_school_name.notnull()]
    next = next.melt(id_vars=["dbn", "ay", "school_type", "school_name"], value_vars=[f"hs_rank{i}_school_name" for i in range(1, 6)], var_name="rank", value_name="next_school")
    next["rank"] = next["rank"].apply(lambda x: int(x.split("_")[1][-1:]))
    path = os.path.join(config.data_dir, config.urls["snapshots"].rank_filename)
    next.to_csv(path, index=False)

    return df.drop(columns=drop)


def make_geo(data):
    df = data.copy()
    df['geometry'] = [Point(xy) for xy in zip(df['long'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    return gdf

def clean_snapshot():
    raw = load(config.urls["snapshots"].raw_snapshot)

    cols = [
        "dbn", "location_name_long", "abbr_school_type", "address", "all_es_admissionsmethods", "all_ms_admissionsmethods",
        "attendance_rate", "authorizer_website", "ay", "champs_sports_boys", "champs_sports_coed", "champs_sports_girls",
        "city_state_zip", "co_located", "dates_of_review", "district", "dual_lang", "ell_n", "ell_pct_raw",
        "enrollment", "es_directory", "ethnicity_amerindian_n", "ethnicity_amerindian_pct_raw", "ethnicity_asian_n", 
        "ethnicity_asian_pct_raw", "ethnicity_black_n", "ethnicity_black_pct_raw", "ethnicity_hispanic_n", "ethnicity_hispanic_pct_raw",
        "ethnicity_pacific_n", "ethnicity_pacific_pct_raw", "ethnicity_white_n", "ethnicity_white_pct_raw",
        "race_asian_pct", "race_black_pct", "race_hispanic_pct", "race_other_pct", "race_white_pct",
        "extracurricularactivities_ms", "formal_authorizer", "gender_female_n", "gender_female_pct_raw", "gender_male_n", "gender_male_pct_raw",
        "gender_x_n", "gender_x_pct_raw", "grades_text", "high_opt_out_sch", "hs_rank1_pct", "hs_rank1_school_name",
        "hs_rank2_pct", "hs_rank2_school_name", "hs_rank3_pct", "hs_rank3_school_name", "hs_rank4_pct", "hs_rank4_school_name", "hs_rank5_pct", "hs_rank5_school_name",
        "iep_n", "iep_pct_raw", "overview_ms", "online_admissions_link_ms", "panorama_id", "principal_name", "principal_phone_number",
        "principal_years", "quality_review_url", "quality_review_year", "state_program_designation", "student_chronic_absent", "teacher_3yr_exp_pct",
        "teacher_ethnicity_amerindian_pct", "teacher_ethnicity_asian_pct", "teacher_ethnicity_black_pct",
        "teacher_ethnicity_hispanic_pct", "teacher_ethnicity_pacific_pct", "teacher_ethnicity_white_pct", "website_es",
        "website_ms", "latitude", "longitude", "x_coordinate", "y_coordinate",
    ]
    data = raw[cols]
    data = fix_ethnicity(data)
    data = fix_pct(data)
    data = fix_admissions(data)
    data = fix_colocations(data)
    data = data.rename(columns=rename_cols)
    data["district"] = data.dbn.apply(lambda x: int(x[:2]))
    data = save_school_rank(data)

    gdf = make_geo(data)
    path = os.path.join(config.data_dir, config.urls["snapshots"].filename)
    data.to_feather(path)

    return gdf


def scrape_school(dbn, url, ay, session, error_log = []):
    """Load the JSON data for a single school from the nycenet snapshot unpublished API"""
    try:
        response = session.get(url)
        if response.status_code == 200:
            json = response.json()
            snap = {
                "dbn": dbn,
                "ay": ay,
                "url": url,
            }
            for x in json:
                if x["dbn"] != dbn:
                    print("dbn mismatch", dbn, x["dbn"])
                key = x["varname"]
                val = x["value"]
                if not key in snap:
                    snap[key] = val
                elif val != "N/A" and snap[key] != val:
                    error_log.append(f"conflicting values ({dbn}): { key}: `{val}` | `{snap[key]}`")

            df = pd.DataFrame.from_records([snap])
            return df
        if response.status_code == 404:
            error_log.append(f"404 ({dbn}): {url}")
        else:
            error_log.append(f"other:({response.status_code}), ({dbn}): {url}")
        return None
    except Exception as e:
        error_log.append((dbn, url, e))
        return None


def scrape_nycenet(data, max_workers=50):
    """Fetch data from a list of URLs in parallel using threading
    
    Parameters
    ----------
    data : a list of tuples (dbn, year, url)
    max_workers : int the number of threads to use, default is 50

    Returns
    -------
    DataFrame the scraped data, combined into a single DataFrame. 
              The data contains many null values as all schools 
              and all years are not consistent in the data they provide.
    """
    session = Session()
    errors = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_school, dbn, url, year - 1, session, error_log=errors) for dbn, year, url in data]
        results = []
        for future in as_completed(futures):
            data = future.result()
            if data is not None and len(data) > 0:
                results.append(data)
    try:
        all = pd.concat(results, axis=0, ignore_index=True)
        session.close()
        return all
    except Exception as e:
        session.close()
        return pd.DataFrame()



def get_snapshot_schools():
    """
    Returns the list of schools in the snapshot data.
    """

    results = []
    tmp = os.path.join(config.data_dir, "tmp")
    if not os.path.exists(tmp):
        os.makedirs(tmp)

    def read_year(year, file):
        try:
            csv_out = os.path.join(tmp, f"{year}_{file}.csv")
            url = f"https://tools.nycenet.edu/vue-assets/static/data/sqs/{year}/{file}.csv"
            print(url)
            path = wget(url, csv_out)
            if path and os.path.exists(path):
                x = pd.read_csv(path)
                x["year"] = year
                return x
            return pd.DataFrame()
        except Exception as e:
            return pd.DataFrame()


    # get the current calendar year in os time
    year = pd.Timestamp.now().year
    print("End year:", year)
    for year in range(2016, year):
        results.append(read_year(year, "school_info"))
        results.append(read_year(year, "school_info_pk"))


    doe = pd.concat(results, axis=0)
    make_url = lambda x: f"https://tools.nycenet.edu/api/v1/data/school/app/snapshot/all/{x.year}/{x.dbn}/{x.report_type}"
    doe["url"] = doe.apply(make_url, axis=1)

    path = os.path.join(config.data_dir, "snapshot_school_list.csv")
    doe.to_csv(path, index=False)
    return doe
    
def get_snapshots():
    """
    Fetch the snapshot data from the NYC DOE data portal.
    """
    doe = get_snapshot_schools()
    
    

