import pandas as pd
import numpy


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
    return float(pct)

# a dict of borough abbreviations
boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}
# parse school distrcit from dbn
def district(dbn): return int(dbn[:2])
# parse boro abbreviation from dbn
def boro(dbn): return boros[dbn[2]]
# convert academic year spring to an integer with the year in the Fall
def ay(year): return int(year.split("-")[0])

def load_school_demographics():
    demo_url = "https://data.cityofnewyork.us/resource/vmmu-wj3w.csv?$limit=1000000"
    df = pd.read_csv(demo_url)
    df["poverty_1"] = df.apply(lambda row: str_pct(row, "poverty_1", "total_enrollment"), axis = 1)
    df["economic_need_index"] = df.apply(lambda row: str_pct(row, "economic_need_index", "total_enrollment"), axis = 1)
    df["year"] = df["year"].apply(ay)
    df["district"] = df["dbn"].apply(district)
    df["boro"] = df["dbn"].apply(boro)
    return df

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
