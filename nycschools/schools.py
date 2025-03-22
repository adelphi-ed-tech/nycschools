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
import numpy as np
import re

import pandas as pd
from thefuzz import fuzz

from . import geo
from . import config

from nycschools.dataloader import load


__demo_filename = os.path.join(config.data_dir, config.urls["demographics"].filename)

class demo():
    """The `demo` class bundles some common sets of column names
    to make it easier to work with the school demographic `DataFrame`

    Examples:
    ----------
    from nycschools import schools

    df = schools.load_school_demographics()
    basic = df[schools.demo.short_cols]
    basic.head()
    """
    raw_cols = [
       'dbn', 'school_name', 'year', 'total_enrollment',
       'grade_pk', 'grade_k', 'grade_1', 'grade_2', 'grade_3',
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
        'school_type',
        'total_enrollment',
        'grade_3k',
        'grade_pk',
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
        'non_binary_n',
        'non_binary_pct',
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
        'eni',
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
        'eni'
    ]

    short_cols = ["dbn","school_name", "short_name", "clean_name", "ay"]

    default_map = {
        'female':'female_n',
        'female_1':'female_pct',
        'male':'male_n',
        'male_1':'male_pct',
        'neither_female_nor_male_1': 'neither_female_nor_male_pct',
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
        'economic_need_index':'eni'
    }


def str_pct(row, pct_col, enroll_col):
    """generic function to take percentages represented as Strings and convert to real
    expects data to look like '84.33%' or .8433, 'Above 95%', 'Below 5%'
    Example: df["economic_need_index"] = df.apply(lambda row: str_pct(row, "economic_need_index", "total_enrollment"), axis = 1)
    """

    # just call the population size `n`
    n = row[enroll_col]

    # get the percentage as a string
    pct = str(row[pct_col])
    if pct.endswith("%"):
        pct = pct[:-1]
    if "Above" in pct:
        pct = n * .96 / n
    elif "Below" in pct:
        pct = n * .04 / n
    elif pct == "No Data":
        return 0

    try:
        pct = float(pct)
    except Exception as ex:
        print(
            f"Exception in {pct_col}: {row['dbn']} - {row['year']}. Value: {pct}")
        raise ex
    # some percentages are whole numbers 0..100, others are real numbers 0..1
    if pct >= 1:
        pct = pct / 100

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
    path = config.urls["demographics"].filename
    df = load(path)
    df.zip = df.zip.fillna(0).astype("int32")
    df.beds = df.beds.fillna(0).astype("int64")
    for c in df.columns:
        if c.startswith("grade_"):
            df[c] = pd.to_numeric(df[c], downcast='integer', errors='coerce')
    return df

def get_demographics(df):
    """Loads and cleans school demographic data from a pandas DataFrame.
    The initial data is joined with location data to make it
    more easily merged with other data sets.

    Parameters
    -----------
    df : DataFrame, a "raw" DataFrame of school demographic data from NYC Schools or Open Data Portal

    Returns
    -------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
    """

    boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}

    df["ay"] = df["year"].apply(lambda year: int(year.split("-")[0]))
    df["district"] = df["dbn"].apply(lambda dbn: int(dbn[:2]))

    df["boro"] = df["dbn"].apply(lambda dbn: boros[dbn[2]])
    df["school_num"] = df.dbn.apply(lambda dbn: int(dbn[3:]))
    df["charter"] = df.district.apply(lambda x: 1 if x == 84 else 0)

    # figure out what grades they teach
    df["pk"] = df["grade_pk"] > 0
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
    
    # calculate school type based on district number
    df["school_type"] = None
    df.loc[(df.district > 0)  & (df.district < 33), "school_type"] = "community"
    df.loc[df.district == 84, "school_type"] = "charter"
    df.loc[df.district == 75, "school_type"] = "d75"
    df.loc[df.district == 79, "school_type"] = "alternative"
    df = join_loc_data(df)
    return get_default_cols(df)


def get_default_cols(df):
    missing = set(demo.default_cols) - set(df.columns)
    print(df.ay.unique(), missing)
    for c in missing:
        df[c] = np.nan
    df = df[demo.default_cols]
    return df


def get_demo_2006():
    """Load the 2006 demographic data from the NYC Open Data Portal"""
    df = pd.read_csv(config.urls["demographics"].data_urls["2006"])
    def map_col(c):
        if c.startswith("grade"):
            return f"grade_{c[len('grade'):]}"
        if c == "sped_percent":
            return "swd_pct"
        if c == "sped_num":
            return "swd_n"
        if c == "prek":
            return "grade_pk"
        if c == "k":
            return f"grade_{c}"
        if c.endswith("_num"):
            return c.replace("_num", "_n")
        if c.endswith("_percent"):
            return c.replace("_percent", "_pct")
        if c.endswith("_per"):
            return c.replace("_per", "_pct")
        if c == "name":
            return "school_name"
        return c

    df = df.rename(columns=map_col)

    # parse AY and year
    df["ay"] = df.schoolyear // 10000
    df["year"] = df.ay.apply(lambda x: f"{x}-{((x % 10) + 1):02}")

    # make percentages real
    def check(n):
        if pd.isna(n) or pd.isnull(n):
            return 0
        try:
            float(n)
            return float(n)
        except:
            return 0
    # fill missing free lunch data
    df.fl_pct = df.fl_pct.apply(check)
    df.frl_pct = df.frl_pct.apply(check)

    # fix the grades and percentages
    for c in df.columns:
        if c.startswith("grade_"):
            df[c] = pd.to_numeric(df[c], downcast='integer', errors='coerce')
        if c.endswith("_pct"):
            df[c] = np.round(df[c] / 100, 4)

    df["poverty_pct"] = np.maximum(df.fl_pct, df.frl_pct)
    df["poverty_n"] = np.floor(df.poverty_pct * df.total_enrollment).astype(int)

    df["district"] = df["dbn"].apply(lambda dbn: int(dbn[:2]))

    boros = {"K": "Brooklyn", "X": "Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}
    df["boro"] = df["dbn"].apply(lambda dbn: boros[dbn[2]])
    df["school_num"] = df.dbn.apply(lambda dbn: int(dbn[3:]))
    df["charter"] = 0


    # figure out what grades they teach
    df["pk"] = df["grade_pk"] > 0
    df["elementary"] = df["grade_2"] > 0
    df["middle"] = df["grade_7"] > 0
    df["hs"] = df["grade_10"] > 0

    # make it easier to look up schools
    df["school_type"] = df.apply(school_type, axis=1)
    df["clean_name"] = df.apply(lambda row: clean_name(row.school_name), axis=1)
    df["short_name"] = df.apply(short_name, axis=1)

    df['eni'] = 0
    df['missing_race_ethnicity_data_n'] = 0
    df['missing_race_ethnicity_data_pct'] = 0
    df['multi_racial_n'] = 0
    df['multi_racial_pct'] = 0
    df['native_american_n'] = 0
    df['native_american_pct'] = 0

    df = join_loc_data(df)
    return get_default_cols(df)


def get_demo_2013():
    def map_col(c):
        if c.endswith("_1") and not c.startswith("grade"):
            return c.replace("_1", "")
        if c.endswith("_2") and not c.startswith("grade"):
            return c.replace("_2", "_1")
        if c == "grade_pk_half_day_full_day":
            return "grade_3k_pk_half_day_full"
        return c

    df13 = pd.read_csv(config.urls["demographics"].data_urls["2013"])

    df13 = df13.rename(columns=map_col)
    df13["multi_racial"] = df13['multiple_race_categories_not_represented']
    df13["multi_racial_1"] = df13['multiple_race_categories_not_represented_1']
    df13['missing_race_ethnicity_data'] = 0
    df13['missing_race_ethnicity_data_1'] = 0
    df13['native_american'] = 0
    df13['native_american_1'] = 0

    df13.rename(columns={"grade_3k_pk_half_day_full": "grade_pk"}, inplace=True)
    df13["neither_female_nor_male"] = 0
    df13["neither_female_nor_male_pct"] = 0
    df13 = get_demographics(df13)
    # fix the percentages
    for c in df13.columns:
        if c.startswith("grade_"):
            df13[c] = pd.to_numeric(df13[c], downcast='integer', errors='coerce')
        if c.endswith("_pct")and not c == "poverty_pct":
            df13[c] = np.round(df13[c] / 100, 4)

    # the other data set has 2016 data, don't duplicate it
    return df13[df13.ay.isin([2013, 2014, 2015, 2017])]


def get_demo_2016():
    demo_2016 = pd.read_csv(config.urls["demographics"].data_urls["2016"])
    demo_2016 = demo_2016[demo_2016.year == "2016-17"]
    # make the columns match the most recent data set
    demo_2016.rename(
        columns={"grade_3k_pk_half_day_full": "grade_pk"}, inplace=True)
    demo_2016["neither_female_nor_male"] = 0
    demo_2016["neither_female_nor_male_pct"] = 0
    return get_demographics(demo_2016)


def get_demo_2022():
    """Read the latest demographic data from an Excel download"""
    def xls_cols(col):
        d = {
            "multi-racial": "multi_racial",
            "multi-racial_1": "multi_racial_1",
            "grade_pk_(half_day_&_full_day)": "grade_pk",
            "missing_race/ethnicity_data": "missing_race_ethnicity_data",
            "missing_race/ethnicity_data_1": "missing_race_ethnicity_data_1"
        }
        col_name = col.lower().replace(" ", "_")
        if col_name[0] == "%":
            col_name = col_name[2:] + "_1"
        elif col_name[0] == "#":
            col_name = col_name[2:]
        if col_name in d:
            return d[col_name]
        return col_name

    xls = pd.read_excel( config.urls["demographics"].data_urls["2022"], sheet_name=None)
    df = xls["School"]
    df.rename(columns=xls_cols, inplace=True)
    df = get_demographics(df)

    return df

def get_demo_2023():
    """Read the latest demographic data from an Excel download"""
    def xls_cols(col):
        d = {
            "multi-racial": "multi_racial",
            "multi-racial_1": "multi_racial_1",
            "grade_pk_(half_day_&_full_day)": "grade_pk",
            "neither_female_nor_male": "non_binary_n",
            "neither_female_nor_male_1": "non_binary_pct",
            "missing_race/ethnicity_data": "missing_race_ethnicity_data",
            "missing_race/ethnicity_data_1": "missing_race_ethnicity_data_1"
        }
        col_name = col.lower().replace(" ", "_")
        if col_name[0] == "%":
            col_name = col_name[2:] + "_1"
        elif col_name[0] == "#":
            col_name = col_name[2:]
        if col_name in d:
            return d[col_name]
        return col_name
    xls = pd.read_excel( config.urls["demographics"].data_urls["2023"], sheet_name=None)
    df = xls["School"]
    df.rename(columns=xls_cols, inplace=True)
    df = get_demographics(df)
    return df


def save_demographics():
    demo_2006 = get_demo_2006()
    demo_2013 = get_demo_2013()
    demo_2016 = get_demo_2016()
    demo_2022 = get_demo_2022()
    demo_2023 = get_demo_2023()
    df = demo_2023.copy()
    # join the dataframes, but don't add any academic year 2x
    for data in [demo_2022, demo_2016, demo_2013, demo_2006]:
        df = pd.concat([df, data[~data.ay.isin(df.ay)]], ignore_index=True)

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


def load_hs_directory(ay=2021):
    """Loads the NYC High School Directory data from the NYC Open Data
    Portal. This is a thin wrapper around `pd.read_csv()` and
    requires an internet connection. By default, the most recent directory
    is returned. For a different academic year, pass the `ay` parameter.
    Data is available for academic years 2013-2021. The data varies greatly
    from year to year, so they are not compiled into a single DataFrame.

    Parameters
    -----------
    ay : int , default 2021
         the academic year for the directory data

    Returns
    --------
    DataFrame
        a pandas DataFrame holding the high school directory data

    """
    urls = config.urls["hs_directory"].data_urls
    ay = str(ay)

    if ay not in urls.keys():
        raise ValueError(f"No data for academic year: {ay}")
    url = urls[ay]
    df = pd.read_csv(url)
    df["ay"] = int(ay)
    return df
