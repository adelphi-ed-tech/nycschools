from nycschools import config, dataloader as loader
import requests
import os
import pytest
import shutil


tmp_data_dir = "/tmp/nyc-schools-test-data"

@pytest.mark.skip(reason="too slow for normal testing")
def test_read_urls():
    """Reads the urls download data file and makes sure they can all be reached."""
    assert "demographics" in config.urls
    for key, link in config.urls.items():
        print(f"checking {key}")
        r = requests.get(link.url)
        assert r.status_code == 200


@pytest.mark.skip(reason="deprecated")
def test_download_source():
    loader.download_source()

def test_contains_data_files():

    assert loader.contains_data_files(config.data_dir), "data files should be present in the default data directory"

    if os.path.exists(tmp_data_dir):
        shutil.rmtree(tmp_data_dir)
    os.mkdir(tmp_data_dir)
    assert not loader.contains_data_files(tmp_data_dir)
    shutil.rmtree(tmp_data_dir)


@pytest.mark.skip(reason="too slow for normal testing")
def test_download_archive():
    
    if os.path.exists(tmp_data_dir):
        shutil.rmtree(tmp_data_dir)

    os.mkdir(tmp_data_dir)
    loader.download_archive(data_dir=tmp_data_dir)
    assert loader.contains_data_files(tmp_data_dir)
    shutil.rmtree(tmp_data_dir)


