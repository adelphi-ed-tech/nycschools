import pandas as pd
import requests

# import numpy
# import math


def load_charter_ela():
    url = "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000"
    df = pd.read_csv(url)
    return charter_cols(df)


def load_charter_math():
    url = "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000"

    df = pd.read_csv(url)
    return charter_cols(df)

def charter_cols(df):
    df["test_year"] = df["year"]
    df["ay"] = df["test_year"] - 1
    new_cols = ['drop', 'dbn', 'school_name', 'grade', 'year', 'category',
    'number_tested', 'mean_scale_score', 'level_1_n', 'level_1_pct', 'level_2_n',
    'level_2_pct', 'level_3_n', 'level_3_pct', 'level_4_n', 'level_4_pct',
    'level_3_4_n', 'level_3_4_pct', 'test_year', 'ay']

    df.columns = new_cols

    core_cols = ['dbn', 'ay', 'test_year', 'grade', 'category',
    'number_tested', 'mean_scale_score', 'level_1_n', 'level_1_pct', 'level_2_n',
    'level_2_pct', 'level_3_n', 'level_3_pct', 'level_4_n', 'level_4_pct',
    'level_3_4_n', 'level_3_4_pct', 'year']
    df = df[core_cols]
    df["charter"] = True
    return df


def load_ela(refresh=False):
    if refresh:
        ela_df = load_charter_ela()
    else:
        try:
            # try to load it locally to save time
            ela_df = pd.read_csv("ela-combined.csv")
        except FileNotFoundError:
            ela_df = load_ela_excel()
    charter_df = load_charter_ela()
    df = pd.concat([ela_df, charter_df])
    return df.sort_values(by=["dbn", "ay"])


def load_math(refresh=False):
    if refresh:
        math_df = load_math_excel()
    else:
        try:
            # try to load it locally to save time
            math_df = pd.read_csv("math-combined.csv")
        except FileNotFoundError:
            math_df = load_math_excel()
    charter_df = load_charter_math()
    df = pd.concat([math_df, charter_df])
    return df.sort_values(by=["dbn", "ay"])

def read_excel(url):
    xls = pd.read_excel(url, sheet_name=None)
    sheet_names = ['All', 'SWD', 'Ethnicity', 'Gender', 'Econ Status', 'ELL']

    data = [xls[sheet] for sheet in sheet_names]
    df = pd.concat(data, ignore_index=True)

    cols = ['DBN', 'Grade', 'Year', 'Category', 'Number Tested', 'Mean Scale Score',
            '# Level 1', '% Level 1', '# Level 2', '% Level 2', '# Level 3',
            '% Level 3', '# Level 4', '% Level 4', '# Level 3+4', '% Level 3+4']

    new_cols = ['dbn', 'grade', 'year', 'category', 'number_tested',
                'mean_scale_score', 'level_1_n', 'level_1_pct', 'level_2_n', 'level_2_pct',
                'level_3_n', 'level_3_pct', 'level_4_n', 'level_4_pct', 'level_3_4_n',
                'level_3_4_pct']
    df = df[cols]
    df.columns = new_cols

    # convert these to numbers or coerce to NaN
    numeric_cols = [
        'number_tested',
        "mean_scale_score",
        "level_1_n",
        "level_1_pct",
        "level_2_n",
        "level_2_pct",
        "level_3_n",
        "level_3_pct",
        "level_4_n",
        "level_4_pct",
        "level_3_4_n",
        "level_3_4_pct"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df["test_year"] = df["year"]
    df["ay"] = df["year"] - 1
    df["charter"] = False
    return df

def load_math_excel():
    """
    Load NYS Math test scores from the Excel workbook rather than the API. NYC DOE
    fails to release the demographic breakdowns for test results via its open
    data api.
    """

    url = "https://data.cityofnewyork.us/api/views/365g-7jtb/files/17910cb0-8a62-4037-84b5-f0b4c2b3f71f?download=true&filename=school-math-results-2013-2019-(public).xlsx"
    df = read_excel(url)
    df.to_csv("math-combined.csv", index=False)
    return df

def load_ela_excel():
    """
    Load NYS ELA test scores from the Excel workbook rather than the API. NYC DOE
    fails to release the demographic breakdowns for test results via its open
    data api.
    """

    url = "https://data.cityofnewyork.us/api/views/hvdr-xc2s/files/4db8f0e7-0150-4302-bed7-529c89efa225?download=true&filename=school-ela-results-2013-2019-(public).xlsx"

    df = read_excel(url)
    df.to_csv("ela-combined.csv", index=False)
    return df
