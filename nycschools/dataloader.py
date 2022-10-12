import os
import os.path
import importlib.resources
import json
import wget
import arrow

from . import dirs, get_config

def read_urls():
    data = importlib.resources.read_text("nycschools", "dataurls.json")
    urls = json.loads(data)
    return urls




def load_data_files(data_dir=""):
    """Downloads all of the source data files to the local
    drive and saves them into `platformdirs.site_data_dir`
    for this application."""


    if not data_dir.strip():
        config = get_config()
        data_dir = config["data_dir"]

    data_dir = os.path.abspath(data_dir)

    print(f"""
Downloading NYC Schools Data Files
==================================
saving files to:
{data_dir}
""")
    urls = read_urls()
    start = arrow.utcnow()
    for key, link in urls.items():
        url = link["url"]
        print(f"""
downloading {key} from:
{url}""")

        filename = url.split("/")[-1].split("?")[0]
        if link["filename"]:
            filename = link["filename"]
        wget.download(url, out=os.path.join(data_dir, filename))

    end = arrow.utcnow()
    delta = end.humanize(start, only_distance=True)
    print(f"""
{len(urls)} files downloaded in {delta}
""")
