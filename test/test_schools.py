import os.path
from nycschools import config, schools

def test_load_school_demographics():
    """Tests if schools can load demographics from local dataset and has reasonable values."""

    df = schools.load_school_demographics()
    check_school_data(df)

def test_save_demographics():
    """Tests if school demographics can be downloaded, cleaned, and combined correctly from NYC sources."""
    df = schools.save_demographics()
    check_school_data(df)

def check_school_data(df):
    assert df is not None, "Demo data frame is null"
    n = len(df)
    assert n > 28000, f"We should have about 28k rows, too few found ({n})"
    assert n < 32000, f"We should have about 28k rows, too many found ({n})"
    expected_keys = schools.demo.default_cols
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"

    # at least all of these academic years should be in the data
    a = {2016, 2018, 2019, 2020, 2021, 2022, 2023}
    b = set(df.ay.unique())
    assert a.issubset(b), f"Missing some years we expected: {a.difference(b)}"

    a = {1, 26,  2, 28,  3,  4,  5, 13,  6,  7,  8,  9, 10, 14, 11, 12, 15,
     16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 75, 79, 84}
    b = set(df.district.unique())
    assert a.issubset(b), f"Missing some districts we expected: {a.difference(b)}"
    percents = [c for c in df.columns if c.endswith("pct")] + ["eni"]
    for c in percents:
        assert df[c].min() >= 0, f"Percent less than zero found in {c}"
        assert df[c].max() <= 1, f"Percent greater than 1 find in {c}"
    counts = [c for c in df.columns if c.endswith("_n")]
    upper = df.total_enrollment.max()
    assert upper in range(5900, 6200), f"Max school size of {upper} outside of expected {range(5900, 6200)}"
    for c in counts:
        assert df[c].min() >= 0, f"Count value ({df[c].min()}) less than zero found in {c}"
        assert df[c].max() <= upper, f"Count value ({df[c].max()}) greater than max ({upper}) found in {c}"


def test_get_demo_2023():
    """Tests if schools can load demographics from local dataset and has reasonable values."""

    df = schools.get_demo_2023()
    assert df is not None, "Demo data frame is null"
    assert df.ay.max() >= 2023
    n = len(df)
    assert n > 9_000, f"We should have about 9,300 rows, too few found ({n})"
    assert n < 10_000, f"We should have about 9,300 rows, too many found ({n})"
    expected_keys = schools.demo.default_cols
    a = set(expected_keys)
    b = set(df.columns)
    if not a & b:
        print(f"Missing keys: {a-b}")
        raise AssertionError(f"Missing keys: {a-b}")

    # at least all of these academic years should be in the data
    a = {2019, 2020, 2021, 2022, 2023}
    b = set(df.ay.unique())
    if not a.issubset(b):
        print(f"Missing some years we expected: {a.difference(b)}")
        raise AssertionError(f"Missing years: {a-b}")

    a = {1, 26,  2, 28,  3,  4,  5, 13,  6,  7,  8,  9, 10, 14, 11, 12, 15,
         16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 75, 79, 84}
    b = set(df.district.unique())
    assert a.issubset( b), f"Missing some districts we expected: {a.difference(b)}"
    percents = [c for c in df.columns if c.endswith("pct")] + ["eni"]
    for c in percents:
        assert df[c].min() >= 0, f"Percent less than zero found in {c}"
        assert df[c].max() <= 1, f"Percent greater than 1 find in {c}"
    upper = df.total_enrollment.max()
    assert upper in range( 5900, 6200), f"Max school size of {upper} outside of expected {range(5900, 6200)}"
    counts = [c for c in df.columns if c.endswith("_n")]
    for c in counts:
        # print(f"Checking {c}: min({df[c].min()}), max({df[c].max()})")
        assert df[c].min( ) >= 0, f"Count value ({df[c].min()}) less than zero found in {c}"
        assert df[c].max( ) <= upper, f"Count value ({df[c].max()}) greater than max ({upper}) found in {c}"




def test_save_demographics():
    df = schools.save_demographics()
    assert df is not None, "Demo data frame is null"
    assert os.path.exists(schools.__demo_filename), "no demo file in data_dir"
    expected_keys = schools.demo.default_cols
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"


def test_load_hs_directory():
    def check_year(ay):
        df = schools.load_hs_directory(ay)
        assert df is not None, "HS directory data frame is null"
        n = len(df)
        assert n > 400, f"We should have about 400 rows, too few found ({n})"
        assert "dbn" in df, "Missing dbn column"
    
    for ay in range(2013, 2021):
        check_year(ay)