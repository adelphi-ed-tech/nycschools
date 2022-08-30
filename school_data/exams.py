import pandas as pd
import numpy as np


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




def load_charter_ela(refresh=False):
    """
    Loads the charter school ELA exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    url = "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000"
    filename = "charter-ela.csv"
    return load_charter_test(url, filename, refresh)

def load_charter_math(refresh=False):
    """
    Loads the charter school Math exam results for the "All Students"
    category from the NYC Open Data Portal. Columns are re-named for consistency.
    """
    filename = "charter-math.csv"
    url = "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000"
    return load_charter_test(url, filename, refresh)

def load_charter_test(url, filename, refresh=False):

    if not refresh:
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

def load_nyc_nysed():
    return pd.read_csv("nysed-nyc-exams.csv")

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

    try:
        # try to load it locally to save time
        return pd.read_csv("regents-exams.csv")
    except FileNotFoundError:
        return load_regents_excel()

def load_nysed_exams(refresh=False):
    """
    Load the grades 3-8 math and ela exam results for all schools and distrcicts
    in New York State, in a long data format. This is the only data set that has
    demographic test results for charter schools in NYC. This data has all of
    the same columns as the NYC `load_math_ela_long`. Note that NYS does not report the same
    demographic categories as New York City. In particular, the two groups
    handle ENL students differently. NYC has 3 categories (current ell, ever
    ell, never ell) where NYS only has ELL and Non-ELL.

    The NYS data includes categories that are not part of the NYC data
    such as homelessness, foster care, and parents in armed services.
    """
    if refresh:
        return read_nysed_exam_excel()
    try:
        # try to load it locally to save time
        return pd.read_feather("nysed-exams.feather")
    except FileNotFoundError:
        return read_nysed_exam_excel()


def load_nysed_nyc_exams():
    """
    Loads the New York State version of grades 3-8 Math and ELA exams
    which includes charter and community schools.
    """
    return pd.read_feather("nyc-nysed-exams.feather")

# ==============================================================================
# filename = "3-8_ELA_AND_MATH_RESEARCHER_FILE_2021.xlsx"

def read_all_nysed_data():
    files = [
        "3-8_ELA_AND_MATH_RESEARCHER_FILE_2021.csv",
        "3-8_ELA_AND_MATH_RESEARCHER_FILE_2019.csv",
        "3-8_ELA_AND_MATH_RESEARCHER_FILE_2018.csv"
    ]
    nysed = pd.concat([read_nysed_exam_excel(f) for f in files])
    return nysed


def read_nysed_exam_excel(filename):
    """
    Read the Excel file that has all test scores for all schools and districts
    in New York State.
    """

    nysed = pd.read_csv(filename)
    nysed.columns = [c.upper() for c in nysed.columns]
    print(filename)
    print(nysed.columns)
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

    def map_col(col):
        if col in col_map:
            return col_map[col]
        else:
            return col
    nysed = nysed.rename(columns=map_col)


    print(nysed.columns)

    # nysed.test_year = nysed.test_year.apply(lambda x: x.date().year)
    nysed.test_year = nysed.test_year.apply(lambda x: int(x.split("/")[-1]))
    nysed["ay"] = nysed.test_year - 1
    nysed["level_3_4_n"] = nysed.level_3_n + nysed.level_4_n
    nysed.grade = nysed.grade.apply(lambda x: int(x[6]))
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



    nysed.category = nysed.category.apply(map_cats)

    nysed.exam = nysed.exam.map({"ELA":"ela","Mathematics":"math"})

    for col in numeric_cols:
        nysed[col] = pd.to_numeric(nysed[col], errors='coerce')

    cols = [
        'beds',
        'ay',
        'exam',
        'grade',
        'category',
        'test_year',
        'mean_scale_score',
        'number_tested',
        'number_not_tested',
        'level_1_n',
        'level_1_pct',
        'level_2_n',
        'level_2_pct',
        'level_3_n',
        'level_3_pct',
        'level_4_n',
        'level_4_pct',
        'level_3_4_n',
        'level_3_4_pct'

    ]

    missing_cols = set(cols).difference(set(nysed.columns))
    print(missing_cols)
    for c in missing_cols:
        nysed[c] = None

    #
    # all_grades = calc_all_grades(nysed.sample(500))
    # nysed = nysed[cols]
    # all_grades = all_grades[cols]
    # nysed = nysed.append(all_grades, ignore_index=True)

    # convert percents from 0-100 to 0-1 to match other data
    pct_cols = [c for c in cols if c.endswith("pct")]
    for c in pct_cols:
        # nysed[c] = nysed[c].fillna(0)
        nysed[c] = nysed[c] / 100


    nysed = nysed[cols]
    # save as csv for outside use
    nysed.to_csv("nysed-exams.csv", index=False)
    # this is a big file, so save as feather for internal use
    nysed.to_feather("nysed-exams.feather")

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
    # add all students category to nysed
    def all_grades_for_school(row):
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


def charter_cols(data):
    df = data.copy()
    df["test_year"] = df["year"]
    df["ay"] = df["test_year"] - 1
    new_cols = ['drop', 'dbn', 'school_name', 'grade', 'category',
    'number_tested', 'mean_scale_score', 'level_1_n', 'level_1_pct', 'level_2_n',
    'level_2_pct', 'level_3_n', 'level_3_pct', 'level_4_n', 'level_4_pct',
    'level_3_4_n', 'level_3_4_pct', 'test_year', 'ay']

    df.columns = new_cols

    core_cols = ['dbn', 'ay', 'test_year', 'grade', 'category',
    'number_tested', 'mean_scale_score', 'level_1_n', 'level_1_pct', 'level_2_n',
    'level_2_pct', 'level_3_n', 'level_3_pct', 'level_4_n', 'level_4_pct',
    'level_3_4_n', 'level_3_4_pct', 'year']
    df = df[core_cols]
    df["charter"] = 1
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
    df["charter"] = 0
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
