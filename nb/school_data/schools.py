import pandas as pd
import numpy
import math
import re
from thefuzz import fuzz


class demo():
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
        'district',
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
        'clean_name'
    ]

    core_cols = ['dbn', 'district', 'boro', 'school_name', 'ay', 'total_enrollment',
       'asian_n', 'asian_pct', 'black_n', 'black_pct',
       'hispanic_n', 'hispanic_pct','white_n', 'white_pct',
       'swd_n', 'swd_pct', 'ell_n', 'ell_pct', 'poverty_n', 'poverty_pct',
       'eni_pct']

    short_cols = ["dbn", "school_name", "short_name", "clean_name", "ay"]

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
    """
    load and prep the school demographics data
    generic function to take percents as Strings and convert to real
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
    """
    load and prep the school demographics data
    generic function to take percents as Strings and convert to integers
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


# a dict of borough abbreviations
boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}
# parse school distrcit from dbn
def district(dbn): return int(dbn[:2])
# parse boro abbreviation from dbn
def boro(dbn): return boros[dbn[2]]
# convert academic year spring to an integer with the year in the Fall
def ay(year): return int(year.split("-")[0])


def school_type(school):
    """
        Any school that serves middle school kids
        is considered a middle school here.
    """

    if school["middle"]:
        return "MS"
    if school["elementary"]:
        return "PS"
    if school["hs"]:
        return "HS"
    return "NA"


def clean_name(sn):
    """creates a simplified school name that is easier to search/index"""
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


def load_school_demographics(refresh=False):
    """
    Loads the NYC school-level demographic data from the
    open data portal and create a dataframe., ascending=False
    Adds new columns to the dataframe:
         short_name: the best guess at the nuload_ELAtestmerical name of the school (e.g. PS 9)
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
    return the dataframe
    """
    return pd.read_csv("school-demographics.csv")
    #
    #
    # if refresh:
    #     return save_demographics()
    # else:
    #     try:
    #         # try to load it locally to save time
    #         df = pd.read_csv("school-demographics.csv")
    #         return df
    #     except FileNotFoundError:
    #         return save_demographics()

def save_demographics():
    demo_url = "https://data.cityofnewyork.us/resource/vmmu-wj3w.csv?$limit=1000000"
    df = pd.read_csv(demo_url)

    df["ay"] = df["year"].apply(ay)

    df["district"] = df["dbn"].apply(district)
    df["boro"] = df["dbn"].apply(boro)
    df["school_num"] = df.dbn.apply(lambda dbn: int(dbn[3:]))

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
    df = df[demo.default_cols]
    df.to_csv("school-demographics.csv", index=False)
    return df

def search(df, qry):
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



# ------------------------------------------------------------------------------

def load_ela_exam_spreadsheet():
    """
    Load ELA exam information from the Excel workbook downloaded from the Open Data
    Portal. The workbook has different sheets for each demographic
    category of students. Each sheet has the same columns.
    """
    sheet_names = ["all", "swd", "ethnicity", "gender", "econ_status", "ell"]
    # open the Excel workbook
    xls = pd.ExcelFile('ela.xlsx')
    # read each sheet into a list of DataFrames
    data = [pd.read_excel(xls, sheet) for sheet in sheet_names]
    # combine them into a single dataframe
    ela_df = pd.concat(data, ignore_index=True)


    # convert these to numbers or coerce to NaN
    cols = [
        "mean_scale_score",
        "level_1",
        "level_1_pct",
        "level_2",
        "level_2_pct",
        "level_3",
        "level_3_pct",
        "level_4",
        "level_4_pct",
        "level_3_4",
        "level_3_4_pct"
    ]
    for col in cols:
        if col.endswith("pct"):
            ela_df[col] = pd.to_numeric(ela_df[col], downcast='float', errors='coerce')
        else:
            ela_df[col] = pd.to_numeric(ela_df[col], downcast='integer', errors='coerce')



    ela_df.to_csv("ela-combined.csv", index=False)
