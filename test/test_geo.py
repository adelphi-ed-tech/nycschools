from nycschools import config, geo, dataloader, schools


def test_merge():
    a = schools.load_school_demographics()
    b = geo.load_school_locations()
    c = b.merge(a, on="dbn", how="inner")
    c.explore()


def test_load_zipcodes():
    df = geo.load_zipcodes()
    a = set(schools.load_school_demographics().zip)
    a.remove(0)
    b = set(df.zip)
    assert len(a.difference(b)) < 3, "Missing some zip codes we expected" + str(a.difference(b))


def test_load_school_locations():
    df = geo.load_school_locations()

def test_load_districts():
    df = geo.load_districts()

    assert len(df) > 32, "Not enough districts represented"
    assert len(df) < 40, "Seems like too many school districts for NYC, expcted 1-32,75, etc"
    expected_keys = ['district', 'area', 'length', 'geometry']
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"



def test_get_points():
    urls = config.urls
    df = geo.get_points()
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
    expected_keys = ['dbn', 'zip', 'geo_district', 'district', 'x', 'y', 'geometry']
    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"

def test_get_locations():
    urls = config.urls
    df = geo.get_locations()
    assert len(df) > 1800, "Too few schools found"
    assert len(df) < 2400, "Seems like too many schools"
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
        'open_date',
        'police_precinct',
        'primary_building_code',
        'principal_name',
        'principal_phone_number',
        'principal_title',
        'state_code',
        'status_descriptions']

    for k in expected_keys:
        assert k in df, f"Missing expected key: {k}"
