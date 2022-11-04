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
import pandas as pd
import numpy as np
import wget

import os.path
import zipfile

from . import config
urls = config.urls


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


def load_charter_ela(url=urls["charter_ela"].url):
    """
    Loads the charter school ELA exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    filename = os.path.join(config.data_dir, urls["charter_ela"].filename)
    return load_charter_test(url, filename)

def load_charter_math(url=urls["charter_math"].url):
    """
    Loads the charter school Math exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    filename = os.path.join(config.data_dir, urls["charter_math"].filename)
    return load_charter_test(url, filename)

def load_charter_test(url, filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        pass

    df = pd.read_csv(url)
    df = charter_cols(df)
    df.to_csv(filename, index=False)

    return df

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


def load_ela():
    """
    Loads the New York State ELA grades 3-8 ELA exam results for all categories.
    If a local .csv data file exists, it will return results from that file. If
    no local file is available, itt will loads the Excel data file for from the
    NYC Data Portal and then cobmines the results with charter school data into
    a `DataFrame`. _This can be slow_.
    @return `DataFrame`
    """
    filename = os.path.join(config.data_dir, urls["nyc_ela"].filename)
    try:
        df = pd.read_csv(filename, low_memory=False)
    except FileNotFoundError:
        df = load_ela_excel()
    return df.sort_values(by=["dbn", "ay"])


def load_math():
    """
    Loads the New York State Math grades 3-8 ELA exam results for all categories.
    If a local .csv data file exists, it will return results from that file. If
    no local file is available, itt will loads the Excel data file for from the
    NYC Data Portal and then cobmines the results with charter school data into
    a `DataFrame`. _This can be slow_.
    @return `DataFrame`
    """
    filename = os.path.join(config.data_dir, urls["nyc_math"].filename)
    try:
        df = pd.read_csv(filename, low_memory=False)
    except FileNotFoundError:
        df = load_math_excel()
    return df.sort_values(by=["dbn", "ay"])


def load_regents():
    """
    Loads the New York State Regents exam scores for all categories.
    @return `DataFrame`
    """
    filename = os.path.join(config.data_dir, urls["nyc_math"].filename)
    try:
        df = pd.read_csv(filename, low_memory=False)
    except FileNotFoundError:
        df = load_math_excel()
    return df.sort_values(by=["dbn", "ay"])
    if refresh:
        return load_regents_excel()

    try:
        # try to load it locally to save time
        return pd.read_csv("regents-exams.csv")
    except FileNotFoundError:
        return load_regents_excel()

# ==============================================================================

def charter_cols(data):
    df = data.copy()

    if "unnamed_column" in df:
        del df["unnamed_column"]

    df["ay"] = df["year"] - 1

    new_cols = {
        'year': 'test_year',
        'level_1': 'level_1_n',
        'level_1_1': 'level_1_pct',
        'level_2': 'level_2_n',
        'level_2_1': 'level_2_pct',
        'level_3': 'level_3_n',
        'level_3_1': 'level_3_pct',
        'level_4': 'level_4_n',
        'level_4_1': 'level_4_pct',
        'level_3_4': 'level_3_4_n',
        'level_3_4_1': 'level_3_4_pct'
    }

    df = df.rename(columns=new_cols)

    df["charter"] = 1
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if col.endswith("pct"):
            df[col] = df[col] / 100

    return df


def load_regents_excel():
    url = ""
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


def load_math_excel(url=urls["nyc_math"].url):
    """
    Load NYS Math test scores from the Excel workbook rather than the API. NYC DOE
    fails to release the demographic breakdowns for test results via its open
    data api.
    """

    df = read_nys_exam_excel(url)
    charter_df = load_charter_math()
    df = pd.concat([df, charter_df])
    filename = os.path.join(config.data_dir, urls["nyc_math"].filename)
    df.to_csv(filename, index=False)
    return df

def load_ela_excel(url=urls["nyc_ela"].url):
    """
    Load NYS ELA test scores from the Excel workbook rather than the API. NYC DOE
    fails to release the demographic breakdowns for test results via its open
    data api.
    """

    df = read_nys_exam_excel(url)
    charter_df = load_charter_ela()
    df = pd.concat([df, charter_df])
    filename = os.path.join(config.data_dir, urls["nyc_ela"].filename)
    df.to_csv(filename, index=False)
    return df
