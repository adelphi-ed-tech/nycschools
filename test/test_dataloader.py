from nycschools import config, dataloader as loader
import requests

def test_read_urls():
    """Reads the urls download data file and makes sure they can all be reached."""
    assert "demographics" in config.urls
    for key, link in config.urls.items():
        print(f"checking {key}")
        r = requests.get(link.url)
        assert r.status_code == 200
