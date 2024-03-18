import pytest
from nycschools import config, geo, dataloader, schools
import warnings
import geopandas as gpd


def test_merge():
    a = schools.load_school_demographics()
    b = geo.load_school_locations()
    c = b.merge(a, on="dbn", how="inner")
    assert hasattr(c, "explore"), "The merged dataframe should be a GeoDataFrame with explore()"


def test_load_zipcodes():
    df = geo.load_zipcodes()
    a = set(schools.load_school_demographics().zip)
    a.remove(0)
    b = set(df.zip)
    missing = a.difference(b)
    assert len(missing) < 3, "Missing some zip codes we expected" + str(a.difference(b))
    if len(missing) > 0:
        print(f"Missing some zip codes from the zip code data set: {missing}""")

def test_load_school_locations():
    df = geo.load_school_locations()
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
    a = len(df)
    b = len(df.drop_duplicates(subset="dbn"))
    assert a == b, "Duplicate dbn values found"

    assert all(df.open_year.apply(lambda x: int(x) == x)), "open_year should be an integer"


def test_load_districts():
    df = geo.load_districts()

    assert len(df) > 32, "Not enough districts represented"
    assert len(df) < 40, "Seems like too many school districts for NYC, expcted 1-32,75, etc"
    expected_keys = ['district', 'area', 'length', 'geometry']
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"


def test_load_school_footprints():
    print("loading school footprints")
    df = geo.load_school_footprints()
    print(df.columns)
    dbn = schools.load_school_demographics().dbn
    missing = set(dbn).difference(set(df.dbn))
    print("missing school footprints:", len(missing))
    for dbn in missing:
        print(dbn)


@pytest.mark.skip(reason="too slow for normal testing")
def test_get_school_footprints():
    df = geo.get_school_footprints()
    expected_keys = ['dbn', 'geometry']
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"


def test_get_and_save_locations():
    df = geo.get_and_save_locations()
    assert isinstance(df, gpd.GeoDataFrame) and 'geometry' in df.columns, "expected a GeoDataFrame with geometry column"
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
    a = len(df)
    b = len(df.drop_duplicates(subset="dbn"))
    assert a == b, "Duplicate dbn values found"
    assert len(df[df.open_year.isna()]) == 0, "There should be no missing open_year values"
    # assert all(df.open_year.apply(lambda x: int(x) == x)), "open_year should be an integer"

def test_get_points():
    urls = config.urls
    df = geo.get_points()
    print(df.columns)
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
    a = len(df)
    b = len(df.drop_duplicates(subset="dbn"))
    assert a == b, "Duplicate dbn values found"
    expected_keys = ['dbn', 'zip', 'geo_district', 'district', 'x', 'y', 'geometry']
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"

def test_get_locations():
    urls = config.urls
    df = geo.get_locations()
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
    a = len(df)
    b = len(df.drop_duplicates(subset="dbn"))
    assert a == b, "Duplicate dbn values found"

    assert all(df.open_year.apply(lambda x: int(x) == x)), "open_date should be an integer"

    expected_keys = [
        'dbn',
        'administrative_district_code',
        'administrative_district_name',
        'beds',
        'borough_block_lot',
        'census_tract',
        'community_district',
        'community_school_sup_name',
        'council_district',
        'fax_number',
        'fiscal_year',
        'geographical_district_code',
        'grades_final_text',
        'grades_text',
        'highschool_network',
        'highschool_network_location',
        'highschool_network_name',
        'latitude',
        'location_category_description',
        'location_code',
        'location_name',
        'location_type_description',
        'longitude',
        'managed_by_name',
        'nta',
        'nta_name',
        'open_year',
        'police_precinct',
        'primary_building_code',
        'principal_name',
        'principal_phone_number',
        'principal_title',
        'state_code',
        'status_descriptions']

    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"
