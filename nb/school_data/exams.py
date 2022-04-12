import pandas as pd
import requests

# import numpy
# import math


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



def load_charter_ela():
    """
    Loads the charter school ELA exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    url = "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000"
    df = pd.read_csv(url)
    return charter_cols(df)


def load_charter_math():
    """
    Loads the charter school Math exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    url = "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000"

    df = pd.read_csv(url)
    return charter_cols(df)

def load_math_ela_wide():
    """
    Load a combined `DataFrame` with both math and ela test results
    in a "wide" data format.
    All of the math result columns have the suffix `_math`
    and the ELA columns have the suffix `_ela`.
    """
    math_df = load_math()
    ela_df = load_ela()
    combined = math_df.merge(ela_df, how="inner", on=["dbn", "ay", "grade"], suffixes=["_math", "_ela"])
    return combined

def load_math_ela_long():
    """
    Load a combined `DataFrame` with both math and ela test results
    in a "wide" data format.
    All of the math result columns have the suffix `_math`
    and the ELA columns have the suffix `_ela`.
    """
    math_df = load_math().copy()
    ela_df = load_ela().copy()
    math_df["exam"] = "math"
    ela_df["exam"] = "ela"
    return pd.concat([math_df, ela_df])

def load_ela(refresh=False):
    """
    Loads the New York State ELA grades 3-8 ELA exam results for all categories.
    If a local .csv data file (`ela-combined.csv`) exists, it will return
    results from that file. If `refresh==True` or the file does not
    exist, it will load the Excel data file from the NYC Data Portal
    and then combined the results into a `DataFrame`. _This is slow_.
    @param refresh `True` to force a reload of data from the live site.
    @return `DataFrame`
    """
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
    """
    Loads the New York State Math grades 3-8 ELA exam results for all categories.
    If a local .csv data file (`math-combined.csv`) exists, it will return
    results from that file. If `refresh==True` or the file does not
    exist, it will load the Excel data file from the NYC Data Portal
    and then combined the results into a `DataFrame`. _This is slow_.
    @param refresh `True` to force a reload of data from the live site.
    @return `DataFrame`
    """
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


def load_regents(refresh=False):
    """
    Loads the New York State Regents exam scores for all categories.
    If a local .csv data file (`regents-exams.csv`) exists, it will return
    results from that file. If `refresh==True` or the file does not
    exist, it will load the Excel data file from the NYC Data Portal
    and then combined the results into a `DataFrame`. _This is slow_.
    @param refresh `True` to force a reload of data from the live site.
    @return `DataFrame`
    """
    if refresh:
        return load_regents_excel()
    else:
        try:
            # try to load it locally to save time
            return pd.read_csv("regents-exams.csv")
        except FileNotFoundError:
            return load_regents_excel()
# ==============================================================================
def charter_cols(data):
    df = data.copy()
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
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def load_regents_excel():
    url = "https://data.cityofnewyork.us/api/views/2h3w-9uj9/files/ae520e30-953f-47a0-9654-c77900232236?download=true&filename=2014-15-to-2018-19-nyc-regents-overall-and-by-category---public%20(1).xlsx"
    xls = pd.read_excel(url, sheet_name=None)
    cols = [
        'School DBN',
        'School Type',
        'School Level',
        'Regents Exam',
        'Year',
        'Category',
        'Total Tested',
        'Mean Score',
        'Number Scoring Below 65',
        'Percent Scoring Below 65',
        'Number Scoring 65 or Above',
        'Percent Scoring 65 or Above',
        'Number Scoring 80 or Above',
        'Percent Scoring 80 or Above',
        'Number Scoring CR',
        'Percent Scoring CR']

    new_cols = [
        'dbn',
        'school_type',
        'school_level',
        'regents_exam',
        'year',
        'category',
        'number_tested',
        'mean_score',
        'below_65_n',
        'below_65_pct',
        'above_64_n',
        'above_64_pct',
        'above_79_n',
        'above_79_pct',
        'college_ready_n',
        'college_ready_pct']

    sheet_names = ['All Students',
        'By Gender',
        'By Ethnicity',
        'By ELL Status',
        'By SWD Status']

    data = [xls[sheet] for sheet in sheet_names]
    df = pd.concat(data, ignore_index=True)
    df = df[cols]
    df.columns = new_cols
    numeric_cols = new_cols[6:]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df["test_year"] = df["year"]
    df["ay"] = df["year"] - 1
    df = df.sort_values(by=["dbn","ay","regents_exam","category"])
    df.to_csv("regents-exams.csv", index=False)
    return df


def read_nys_exam_excel(url):
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
    df = read_nys_exam_excel(url)
    df.to_csv("math-combined.csv", index=False)
    return df

def load_ela_excel():
    """
    Load NYS ELA test scores from the Excel workbook rather than the API. NYC DOE
    fails to release the demographic breakdowns for test results via its open
    data api.
    """

    url = "https://data.cityofnewyork.us/api/views/hvdr-xc2s/files/4db8f0e7-0150-4302-bed7-529c89efa225?download=true&filename=school-ela-results-2013-2019-(public).xlsx"

    df = read_nys_exam_excel(url)
    df.to_csv("ela-combined.csv", index=False)
    return df
