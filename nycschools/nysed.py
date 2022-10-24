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


def load_nysed_exams(refresh=False):
    """
    Load the grades 3-8 math and ela exam results for all schools and distrcicts
    in New York State, in a long data format. This is the only data set that has
    demographic test results for charter schools in NYC. This data has all of
    the same columns as the NYC `load_math_ela_long`. Note that NYS does not
    report the same demographic categories as New York City. In particular, the
    two groups handle ENL students differently. NYC has 3 categories (current
    ell, ever ell, never ell) where NYS only has ELL and Non-ELL.

    The NYSED data includes categories that are not part of the NYC data such as
    homelessness, foster care, and parents in armed services.
    """

    try:
        # try to load it locally to save time
        return pd.read_feather("nysed-exams.feather")
    except FileNotFoundError:
        return read_nysed_exam_excel()

def load_nysed_ela_math_archives(urls=urls["nysed_math_ela"].urls):
    """
    Downloads all of the zip archives listed in the urls configuraiton. Extract
    the archives into a temp folder and read them as dataframes. Concats the
    dataframes into a single df and return.
    """
    tmp = os.path.join(config.data_dir, "tmp")
    if not os.path.exists(tmp):
        os.mkdir(tmp)

    # download and extract all of the .zip files from NYSED data portal
    for url in urls:
        download_and_extract(url, tmp)

    # delete all of the files we don't care about from the temp dir
    # and parse all of the ones we _do_ care about
    files = os.listdir(tmp)
    data = []

    for f in files:
        if f.endswith("mdb") or "RESEARCHER_FILE" not in f:
            os.remove(os.path.join(tmp, f))
        else:
            data.append(os.path.join(tmp, f))

    return pd.concat([read_nysed_exam(d) for d in data])


def download_and_extract(url, tmp):
    """Download and extract the .zip archives from NYSED"""
    zippath = os.path.join(tmp, url.split("/")[-1])
    wget.download(url, out=zippath)
    zip = zipfile.ZipFile(zippath)
    zip.extractall(path=tmp)



def fix_cols(df):
    """
    Fixes the columns in the dataframe so that each NYSED year is consistent
    with the other years' columns and column name/formats match other  NYC DOE
    columns in the data portal.
    """
    nysed = df.copy()

    col_map = {
        'NAME': 'school_name',
        "BEDSCODE":"beds",
        "SUBGROUP_NAME":"category",
        "ITEM_SUBJECT_AREA":"exam",
        "ITEM_DESC":"grade",
        "SY_END_DATE":"test_year",
        "TOTAL_TESTED":"number_tested",
        'TOTAL_ENROLLED': 'total_enrollment',
        'TOTAL_NOT_TESTED': 'number_not_tested',
        'L1_COUNT':"level_1_n",
        'L1_PCT':"level_1_pct",
        'L2_COUNT':"level_2_n",
        'L2_PCT':"level_2_pct",
        'L3_COUNT':"level_3_n",
        'L3_PCT':"level_3_pct",
        'L4_COUNT':"level_4_n",
        'L4_PCT':"level_4_pct",
        'L3-L4_PCT':"level_3_4_pct",
        'MEAN_SCALE_SCORE':"mean_scale_score",
        'SUBGROUP_CODE': 'subgroup_code'
    }

    # rename columns to match NYC cols
    def map_col(col):
        if col in col_map:
            return col_map[col]
        else:
            return col
    nysed = nysed.rename(columns=map_col)

    if "total_enrollment" not in nysed:
        nysed["total_enrollment"] = 0
    if "number_not_tested" not in nysed:
        nysed["number_not_tested"] = 0

    return nysed[list(col_map.values())]



def fix_data(df):
    """
    Cleans data in the dataframe so that row-level data is
    consistent across test years and matches NYC math/ela data sets:
    - student categories are consistent
    - counts and percents are consistent
    - exam category is consistent
    """

    nysed = df.copy()
    try: # this for excel
        nysed.test_year = nysed.test_year.apply(lambda x: x.date().year)
    except: # or this for csv
        nysed.test_year = nysed.test_year.apply(lambda x: int(x.split("/")[-1]))

    cat_map = {
        'English Language Learner': "Current ELL",
        'Asian or Native Hawaiian/Other Pacific Islander': 'Asian',
        'Hispanic or Latino': 'Hispanic',
        'Black or African American': 'Black',
        'Not Economically Disadvantaged': 'Not Econ Disadv',
        'Economically Disadvantaged': 'Econ Disadv',
        'Students with Disabilities': 'SWD',
        'General Education Students': 'Not SWD',
        'Non-English Language Learner': 'Never ELL'
    }

    def map_cats(cat):
        if cat in cat_map:
            return cat_map[cat]
        return cat

    # rename the student demo categories to match NYC
    nysed.category = nysed.category.apply(map_cats)

    # rename the exams to match NYC
    nysed.exam = nysed.exam.map({"ELA":"ela","Mathematics":"math"})


    # make counts into integers
    count_cols = [c for c in nysed.columns if c.endswith("_n")]
    # if we have these cols, add them too
    for c in ["number_tested", "total_enrollment", "number_not_tested", "test_year"]:
        if c in nysed:
            count_cols.append(c)
    for col in count_cols:

        nysed[col] = pd.to_numeric(nysed[col], errors='coerce')
        nysed[col] = nysed[col].fillna(0)
        nysed[col] = nysed[col].astype(int)

    nysed["ay"] = nysed.test_year - 1
    nysed["level_3_4_n"] = nysed.level_3_n + nysed.level_4_n

    # parse the grade leve string to just the grade int
    nysed.grade = nysed.grade.apply(lambda x: int(x[6]))


    # convert percents from 0-100 to 0-1 to match other data
    def fix_pct(x):
        if not x or x == "" or x =="-" or x == 0:
            return 0

        if hasattr(x, "endswith") and x.endswith("%"):
            x = x[:-1]

        if 0 <= x <= 1:
            return x
        try:
            x = float(x)
            x /= 100
            return x
        except:
            print("couldn't fix", x)
            return x

    pct_cols = [c for c in nysed.columns if c.endswith("pct")]
    for c in pct_cols:
        nysed[c] = nysed[c].apply(fix_pct)

    return nysed


def read_nysed_exam(filename):
    """
    Read the Excel file that has all test scores for all schools and districts
    in New York State.
    """

    try:
        nysed = pd.read_csv(filename)
    except:
        nysed = pd.read_excel(filename)

    nysed = fix_cols(nysed)
    nysed = fix_data(nysed)
    



    #
    # all_grades = calc_all_grades(nysed.sample(500))
    # nysed = nysed[cols]
    # all_grades = all_grades[cols]
    # nysed = nysed.append(all_grades, ignore_index=True)




    # nysed = nysed[cols]
    # save as csv for outside use
    # nysed.to_csv("nysed-exams.csv", index=False)

    # this is a big file, so save as feather for internal use
    # nysed.to_feather("nysed-exams.feather")

    return nysed



def map_nysed_nyc(nysed):
    dbn_list = pd.read_feather("dbn-beds-list.feather", columns=["dbn","beds"])
    dbn_list[dbn_list.beds.isin(nysed.beds)].drop_duplicates()
    cols = list(nysed.columns)
    # add dbn to nysed
    combined = nysed.merge(dbn_list, on="beds", how="inner")
    cols = ["dbn"] + cols
    combined = combined[cols]
    combined.to_feather("nyc-nysed-exams.feather")

    return combined



def calc_all_grades(nysed):
    """
    NYSED data doesn't include All Grades like NYC schools, so this function
    adds an "All Grades" category with aggregate data for each school.
    """

    # add all students category to nysed
    def all_grades_for_school(row):
        """For each school, calculate the aggregate result for all grades"""
        qry = f"beds == '{row.beds}' and ay == {row.ay} and category == '{row.category}' and exam=='{row.exam}'"
        data = nysed.query(qry)

        mean_scale_score = np.average(data.mean_scale_score, weights=data.total_enrollment)
        num_tested = data.number_tested.sum()
        levels = ["1","2","3","4","3_4"]
        if num_tested == 0:
            levels_n = [0] * len(levels)
            levels_pct = [0] * len(levels)
        else:
            levels_n = [data[f"level_{i}_n"].sum() for i in levels]
            levels_pct = [n / num_tested for n in levels_n ]
        result = {
              'ay': row.ay,
              'exam': row.exam,
              'grade': "All Grades",
              'category': row.category,
              'test_year': data.test_year.max(),
              'mean_scale_score': mean_scale_score,
              'number_tested': num_tested,
              'number_not_tested': data.number_not_tested.sum(),
              'level_1_n': levels_n[0],
              'level_1_pct': levels_pct[0],
              'level_2_n': levels_n[1],
              'level_2_pct': levels_pct[1],
              'level_3_n': levels_n[2],
              'level_3_pct': levels_pct[2],
              'level_4_n': levels_n[3],
              'level_4_pct': levels_pct[3],
              'level_3_4_n': levels_n[4],
              'level_3_4_pct': levels_pct[2],
              'beds': data.beds.max()
        }
        rows.append(result)

    rows = []
    cols = ["beds","ay","exam","category","test_year"]
    t = nysed[cols]

    t = t.drop_duplicates()
    t.apply(all_grades_for_school, axis=1)

    return pd.DataFrame(rows)


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
        if col.endswith("pct"):
            df[col] = df[col] / 100

    df["test_year"] = df["year"]
    df["ay"] = df["year"] - 1
    del df["year"]
    df["charter"] = 0
    return df
