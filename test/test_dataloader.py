from nycschools import dataloader as loader
import requests

def test_read_urls():
    """Reads the urls download data file and makes sure they can all be reached."""
    urls = loader.read_urls()
    assert "demographics" in urls
    for key, link in urls.items():
        print(f"checking {key}")
        req = requests.get(link["url"])
        assert req.status_code == 200


# def test_load_data_files():
#     loader.
