import pytest
from nycschools import config, exams


@pytest.mark.skip(reason="too slow for normal testing")
def test_load_ela_excel():
    df = exams.load_ela_excel()
    check_state_test(df)

@pytest.mark.skip(reason="too slow for normal testing")
def test_load_math_excel():
    df = exams.load_math_excel()
    check_state_test(df)

def test_load_charter_ela():
    df = exams.load_charter_ela()
    check_state_test(df)

def test_load_charter_math():
    df = exams.load_charter_math()
    check_state_test(df)

def test_load_math():
    df = exams.load_math()
    check_state_test(df)
    cats = {'All Students', 'Not SWD', 'SWD', 'Asian', 'Black', 'Hispanic',
           'White', 'Female', 'Male', 'Econ Disadv', 'Not Econ Disadv',
           'Current ELL', 'Ever ELL', 'Never ELL'}
    for c in cats:
        assert df[df.category == c].number_tested.max() > 200, "not enough students tested in category: " + c

def test_load_ela():
    df = exams.load_ela()
    check_state_test(df)
    cats = {'All Students', 'Not SWD', 'SWD', 'Asian', 'Black', 'Hispanic',
           'White', 'Female', 'Male', 'Econ Disadv', 'Not Econ Disadv',
           'Current ELL', 'Ever ELL', 'Never ELL'}
    for c in cats:
        assert df[df.category == c].number_tested.max() > 200, "not enough students tested in category: " + c

def test_load_math_ela_long():
    df = exams.load_math_ela_long()
    assert "exam" in df.columns, "missing exam column from long data"


def test_load_math_ela_wide():
    df = exams.load_math_ela_wide()
    cols = df.columns
    math_cols = [c for c in cols if c.endswith("_math")]
    ela_cols = [c for c in cols if c.endswith("_ela")]
    assert len(math_cols) > 0
    assert len(ela_cols) > 0
    assert len(ela_cols) == len(math_cols)



def check_regents(df):
    expected_cols = {'dbn', 'school_type', 'school_level', 'regents_exam', 'year',
                     'category', 'number_tested', 'mean_score', 'below_65_n', 'below_65_pct',
                     'above_64_n', 'above_64_pct', 'above_79_n', 'above_79_pct',
                     'college_ready_n', 'college_ready_pct', 'test_year', 'ay'}
    assert df is not None, "data frame is null"
    assert set(df.columns) == expected_cols, "missing expected columns"
    assert len(df.regents_exam.unique()) > 8, "not enough regents exams"

def test_load_regents_excel():
    df = exams.load_regents_excel()
    check_regents(df)


def test_load_regents():
    df = exams.load_regents()
    check_regents(df)





# ---------------------------------------------------------------------------
def check_state_test(df):
    assert df is not None, "data frame is null"
    n = len(df)
    assert n > 20, f"Only ({n}) records found"
    expected_keys = exams.numeric_cols
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"

    percents = [c for c in df.columns if c.endswith("pct")]
    for c in percents:
        assert df[c].min() >= 0, f"Percent less than zero found in {c}"
        assert df[c].max() <= 1, f"Percent greater than 1 find in {c}"
    counts = [c for c in df.columns if c.endswith("_n")]
    upper = df.number_tested.max()
    upper_range = range(int(upper * .8), int(upper *1.2))
    assert upper in upper_range, f"Max school size of {upper} outside of expected {upper_range}"
    for c in counts:
        assert df[c].max() <= upper, f"Count value ({df[c].max()}) greater than max ({upper}) found in {c}"
