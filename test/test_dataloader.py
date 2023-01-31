from nycschools import config, dataloader as loader
import requests
import os
import pytest
import shutil

@pytest.mark.skip(reason="too slow for normal testing")
def test_read_urls():
    """Reads the urls download data file and makes sure they can all be reached."""
    assert "demographics" in config.urls
    for key, link in config.urls.items():
        print(f"checking {key}")
        r = requests.get(link.url)
        assert r.status_code == 200


def test_download_cache():
    if os.path.exists("test-data"):
        shutil.rmtree("test-data")

    os.mkdir("test-data")
    loader.download_cache(data_dir="test-data")
    files = [
        "charter-ela.csv",
        "charter-math.csv",
        "nyc-ela.csv",
        "nyc-math.csv",
        "nysed-exams.csv",
        "nysed-exams.feather",
        "school-demographics.csv",
        "school_locations.geojson"
    ]

    for f in files:
        assert os.path.exists(f"test-data/{f}")
    shutil.rmtree("test-data")