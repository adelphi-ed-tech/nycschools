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
import os.path
import math
import re

import pandas as pd
from thefuzz import fuzz

from . import geo
from . import config


__demo_filename = os.path.join(config.data_dir, "school-demographics.csv")

class demo():
    """The `demo` class bundles some common sets of column names
    to make it easier to work with the school demographic `DataFrame`

    Examples:
    ----------
    from nycschools import schools

    df = schools.load_school_demographics()
    basic = df[schools.demo.short_cols]
    basic

    """
    raw_cols = [
       'dbn', 'school_name', 'year', 'total_enrollment',
       'grade_3k_pk_half_day_full', 'grade_k', 'grade_1', 'grade_2', 'grade_3',
       'grade_4', 'grade_5', 'grade_6', 'grade_7', 'grade_8', 'grade_9',
       'grade_10', 'grade_11', 'grade_12', 'female', 'female_1', 'male',
       'male_1', 'asian', 'asian_1', 'black', 'black_1', 'hispanic',
       'hispanic_1', 'multi_racial', 'multi_racial_1', 'native_american',
       'native_american_1', 'white', 'white_1', 'missing_race_ethnicity_data',
       'missing_race_ethnicity_data_1', 'students_with_disabilities',
       'students_with_disabilities_1', 'english_language_learners',
       'english_language_learners_1', 'poverty', 'poverty_1',
       'economic_need_index'
    ]

    default_cols = [
        'dbn',
        'beds',
        'district',
        "geo_district",
        'boro',
        'school_name',
        'short_name',
        'ay',
        'year',
        'total_enrollment',
        'grade_3k_pk_half_day_full',
        'grade_k',
        'grade_1',
        'grade_2',
        'grade_3',
        'grade_4',
        'grade_5',
        'grade_6',
        'grade_7',
        'grade_8',
        'grade_9',
        'grade_10',
        'grade_11',
        'grade_12',
        'female_n',
        'female_pct',
        'male_n',
        'male_pct',
        'asian_n',
        'asian_pct',
        'black_n',
        'black_pct',
        'hispanic_n',
        'hispanic_pct',
        'multi_racial_n',
        'multi_racial_pct',
        'native_american_n',
        'native_american_pct',
        'white_n',
        'white_pct',
        'missing_race_ethnicity_data_n',
        'missing_race_ethnicity_data_pct',
        'swd_n',
        'swd_pct',
        'ell_n',
        'ell_pct',
        'poverty_n',
        'poverty_pct',
        'eni_pct',
        'clean_name',
        'zip'
    ]

    core_cols = [
        'dbn',
        'beds',
        'district',
        "geo_district",
        'boro',
        'school_name',
        'ay',
        'total_enrollment',
        'female_n',
        'female_pct',
        'male_n',
        'male_pct',
        'asian_n',
        'asian_pct',
        'black_n',
        'black_pct',
        'hispanic_n',
        'hispanic_pct',
        'white_n',
        'white_pct',
        'swd_n',
        'swd_pct',
        'ell_n',
        'ell_pct',
        'poverty_n',
        'poverty_pct',
        'eni_pct'
    ]

    short_cols = ["dbn","school_name", "short_name", "clean_name", "ay"]

    default_map = {
        'female':'female_n',
        'female_1':'female_pct',
        'male':'male_n',
        'male_1':'male_pct',
        'asian':'asian_n',
        'asian_1':'asian_pct',
        'black':'black_n',
        'black_1':'black_pct',
        'hispanic':'hispanic_n',
        'hispanic_1':'hispanic_pct',
        'multi_racial':'multi_racial_n',
        'multi_racial_1':'multi_racial_pct',
        'native_american':'native_american_n',
        'native_american_1':'native_american_pct',
        'white':'white_n',
        'white_1':'white_pct',
        'missing_race_ethnicity_data':'missing_race_ethnicity_data_n',
        'missing_race_ethnicity_data_1':'missing_race_ethnicity_data_pct',
        'students_with_disabilities':'swd_n',
        'students_with_disabilities_1':'swd_pct',
        'english_language_learners':'ell_n',
        'english_language_learners_1':'ell_pct',
        'poverty':'poverty_n',
        'poverty_1':'poverty_pct',
        'economic_need_index':'eni_pct'
    }


def str_pct(row, pct_col, enroll_col):
    """generic function to take percentages represented as Strings and convert to real
    expects data to look like '84.33%', 'Above 95%', 'Below 5%'
    Example: df["economic_need_index"] = df.apply(lambda row: str_pct(row, "economic_need_index", "total_enrollment"), axis = 1)
    """
    pct = row[pct_col][:-1]
    # just call the population size `n`
    n = row[enroll_col]
    try:
        pct = float(pct) / 100
    except:
        if "Above" in pct:
            pct = n * .96 / n
        elif "Below" in pct:
            pct = n * .04 / n
        else:
            print(f"Exception in {col}: {row['dbn']} - {row['year']}. Value: {pct}")
    return float(pct)

def str_count(row, col, enroll_col):
    """generic function to take whole number counts represented as Strings and convert to integers
    expects data to look like '246', 'Above 95%', 'Below 5%'
    Example: df["poverty"] = df.apply(lambda row: str_count(row, "poverty", "total_enrollment"), axis = 1)
    """
    count = row[col]
    # just call the population size `n`
    n = row[enroll_col]
    try:
        return int(count)
    except:
        if "Above" in count:
            return int(math.ceil(n * .96))
        elif "Below" in count:
            return int(math.floor(n * .04))
        else:
            print(f"Exception in {col}: {row['dbn']} - {row['year']}. Value: {count}")

def school_type(school):
    """Any school that serves middle school kids is considered a middle school here."""

    if school["middle"]:
        return "MS"
    if school["elementary"]:
        return "PS"
    if school["hs"]:
        return "HS"
    return "NA"


def clean_name(sn):
    """Creates a simplified school name that is easier to search/index

    """
    sn = sn.lower()
    sn = sn.strip()
    sn = sn.replace(".", "")
    clean = []
    for word in sn.split(" "):
        try:
            n = int(word)
            clean.append(str(n))
        except:
            clean.append(word)

    sn = " ".join(clean)

    # ms, is, ps followed by a number
    p = re.compile(r"\b([m|p|i]s [0-9]*)")
    m = p.search(sn)
    if m:
        sn = sn.replace(m.group(0), "")
    sn = sn.strip()
    # if the only thing left is the boro, short name will be school num + boro
    if sn in ["bronx", "brooklyn", "manhattan", "queens", "staten island"]:
        sn = f"{m.group(0)} {sn}"
    return sn


def short_name(row):
    """Attempts to guess the common "short name" for a school.
For example, the full name might be "P.S. 015 Roberto Clemente".
This school is probably commonly referred to as PS 15."""
    sn = row.school_name.upper()
    if "P.S." in sn or "P. S." in sn:
        return f"PS {row.school_num}"
    if "M.S." in sn or "M. S." in sn:
        return f"MS {row.school_num}"
    if "I. S." in sn or "I.S." in sn:
        return f"IS {row.school_num}"

    return f"{row.school_type} {row.school_num}"


def load_school_demographics():
    """ Loads the NYC school-level demographic data from the
    open data portal and create a dataframe.

    Adds new columns to the data:

           short_name: the best guess for the common name of the school (e.g. PS 9)
                       or "" if none exists
             district: the school district number [1..32, 75, 79, 84]
                 boro: borough code string ["M","B","X","Q","R"]
            boro_name: string of the full borough name
                 year: the academic year as an integer representing the calendar
                       year in the fall of the school year
          white_asian: combined number of white and asian students
            non_white: total number of non white students
      non_white_asian: total number of non white or asian students
       black_hispanic: total number of black and hispanic students
              charter: 1 for charter schools, 0 for community public schools
                 beds: the New York State BEDS code for the school
                  zip: school zip code
         geo_district: the geographic school district where the school is located
                       will differ for schools where district is > 32

    Returns
    --------------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
        in the data portal

    """

    # try to load it locally to save time
    df = pd.read_csv(__demo_filename)
    df.zip = df.zip.fillna(0).astype("int32")
    df.beds = df.beds.fillna(0).astype("int64")
    1 == 1
    return df

def save_demographics(url=config.urls["demographics"].url):
    """Loads and cleans school demographic data from a NYC Open Data
    Portal URL. The data is joined with some location data to make it
    more easily merged with other data sets. A local copy of the data
    is saved as a .csv in the `nycschools` data directory.

    Parameters
    -----------
    url : str , default loads the url from config.urls with the 'demographics' key
          the URL to the most recent NYC school demographics

    Returns
    -------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
        in the data portal

    """
    df = pd.read_csv(url)

    boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}

    df["ay"] = df["year"].apply(lambda year: int(year.split("-")[0]))
    df["district"] = df["dbn"].apply(lambda dbn: int(dbn[:2]))

    df["boro"] = df["dbn"].apply(lambda dbn: boros[dbn[2]])
    df["school_num"] = df.dbn.apply(lambda dbn: int(dbn[3:]))
    df["charter"] = df.district.apply(lambda x: 1 if x == 84 else 0)

    # figure out what grades they teach
    df["pk"] = df["grade_3k_pk_half_day_full"] > 0
    df["elementary"] = df["grade_2"] > 0
    df["middle"] = df["grade_7"] > 0
    df["hs"] = df["grade_10"] > 0

    # make it easier to look up schools
    df["school_type"] = df.apply(school_type, axis=1)
    df["clean_name"] = df.apply(lambda row: clean_name(row.school_name), axis=1)
    df["short_name"] = df.apply(short_name, axis=1)

    df["poverty"] = df.apply(lambda row: str_count(row, "poverty", "total_enrollment"), axis = 1)
    df["poverty_1"] = df.apply(lambda row: str_pct(row, "poverty_1", "total_enrollment"), axis = 1)
    df["economic_need_index"] = df.apply(lambda row: str_pct(row, "economic_need_index", "total_enrollment"), axis = 1)
    df = df.rename(columns=demo.default_map)

    df = join_loc_data(df)
    df = df[demo.default_cols]
    df.to_csv(__demo_filename, index=False)

    return df


def join_loc_data(df):
    """Join NYS BEDS id, zip code, and other location data.

    """
    school_loc = geo.load_school_locations()
    # with the left join, we might be missing zip and beds for some schools
    df = df.merge(school_loc[["dbn", "beds", "zip", "geo_district"]], on="dbn", how="left")
    # df.beds = df.beds.fillna(0)
    df.geo_district = df.geo_district.fillna(0)
    df.geo_district = df.geo_district.astype(int)
    # df.zip = df.zip.fillna(0).astype("int32")
    df.beds = pd.to_numeric(df.beds , downcast='integer', errors='coerce')
    df.beds = df.beds.fillna(0).astype("int64")

    # df.beds = df.beds.fillna(0).astype("int64")

    def get_geo(row):
        d = row.district
        if row.geo_district > 0:
            return row.geo_district
        if d > 0 and d <=32:
            return d
        return 0
    df.geo_district = df.apply(get_geo, axis=1)
    return df

def search(df, qry):
    """Search a DataFrame for a school using fuzzy logic.


    Parameters
    ----------
    df : DataFrame
         a pandas DataFrame containing school data, such as the
         data returned from `load_school_demographics()`
    qry : the school name or search term to look for in the data set

    Returns
    ---------
    DataFrame
        the schools that match the `qry` or an empty DataFrame
        if no matches were found

    """
    t = df.copy(deep=False)
    latest = t.ay.max()
    # just check the lastest year
    t = t[t["ay"] == latest]

    # see if there's an exact name match
    q = clean_name(qry)
    results = t.query(f"clean_name == '{q}'")
    if len(q) > 0 and len(results) > 0:
        return results

    # look it up by number
    results = t.query(f"short_name == '{qry.upper()}'")
    if len(results) > 0:
        return results

    # fuzzy search -- add a fuzzy search match column
    t["match"] = t.school_name.apply(lambda sn: fuzz.token_set_ratio(qry, sn))
    t = t.query("match > 80")
    t = pd.DataFrame(t)
    # now sort the results based on the ratio match
    t["match"] = t.clean_name.apply(lambda sn: fuzz.ratio(qry, sn))
    results = t.sort_values(by=["match"], ascending=False)

    return results
