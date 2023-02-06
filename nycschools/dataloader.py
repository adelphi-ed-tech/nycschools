# NYC School Data
# Copyright (C) 2022. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU AFFERO GENERAL PUBLIC LICENSE (the "License") as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
import os
import os.path

import wget
import arrow
import py7zr
import requests

from . import config
import warnings

def get_data_dir():
    return config.data_dir


#   if not data_dir:
#     print(f"""
#   Could not find nyc-school-data in your Google Drive.
#   Please see the documentation to learn how to configure Google Colab:
#   https://adelphi-ed-tech.github.io/nycschools/  
# """)


def download_data():
    path = find_data_dir()
    if path:
        config.data_dir = path
        return path
    
    return download_archive()


def find_data_dir():
    """
    Tries to find an existing data directory populated
    with data, including searching through mounted
    google drive if the `colab` package is available
    and the g drive is mounted in the "standard" location
    of `/content/gdrive`.

    Returns:
        str: the path to the data directory
    """
    env_dir = os.environ.get("NYC_SCHOOLS_DATA_DIR", None)
    local = os.path.join(".", "school-data")

    paths = [config.data_dir, env_dir, local]
    for path in paths:
        if os.path.exists(path) and contains_data_files(path):
            config.data_dir = path
            return path
    path = mount_colab_data_dir()
    if contains_data_files(path):
        config.data_dir = path
        return path
    return None


def mount_colab_data_dir():
    """Try to mount a google drive directory in colab
    and then search for the data directory by looking
    for a directory with the know name 'nyc-schools-data'."""

    gdrive = "/content/gdrive"
    target = "nyc-schools-data"

    if not os.path.exists(gdrive):
        try:
            from google.colab import drive
            drive.mount(gdrive)
        except:
            return None

    # first check all of MyDrive
    for root, dirs, files in os.walk(f"{gdrive}/MyDrive"):
        if target in dirs:
            return os.path.join(root, f"{target}/data")

    # next check all of Shared Drives
    for root, dirs, files in os.walk(f"{gdrive}/Shareddrives"):
        if target in dirs:
            return os.path.join(root, f"{target}/data")

    return None



def contains_data_files(path):
    """
    Checks to see if the specified path contains
    the data files required by this application.

    Parameters:
        path (str): the path to check

    Returns:
        bool: True if the path contains the data files
            required by this application, False otherwise
    """
    files = set(os.listdir(path))
    if len(files) == 0:
        return False

    expected = {
        "charter-ela.csv",
        "charter-math.csv",
        "nyc-ela.csv",
        "nyc-math.csv",
        "nysed-exams.csv",
        "nysed-exams.feather",
        "school-demographics.csv",
        "school_locations.geojson"
    }

    if expected.issubset(files):
        return True
    
    missing = expected.difference(files)
    if len(missing) == len(expected):
        return False
    
    warnings.warn(f"""Some data files are missing from the data directory.
    Found files: {files.intersection(expected)}
    Missing files: {missing}
You can download the data files by running: `nycschools.download_cache()`
For more information, see:
https://adelphi-ed-tech.github.io/nycschools/""")

    
    return False



def download_archive(data_dir=None):
    """
    Downloads the school data archive to the local
    drive and saves it into `data_dir` then extracts
    the .7z archive. `data_dir` now contains the
    cleaned and compiled school data files.

    Parameters:
        data_dir (str): the path to the directory where
            the data files should be saved. If not specified,
            the package configuration `data_dir` is used.

    Returns:
        str: the path to the downloaded file
    """
    if not data_dir:
        data_dir = config.data_dir
    url = config.urls["school-data-archive"].url
    filename = config.urls["school-data-archive"].filename
    data_dir = os.path.abspath(data_dir)
    archive = os.path.join(data_dir, filename)
    resp = requests.get(url)
    with open(archive, "wb") as f:
        f.write(resp.content)

    with py7zr.SevenZipFile(archive, mode='r') as z:
        z.extractall(path=data_dir)

    os.remove(archive)
    return data_dir

def download_source_data(data_dir=""):
    """
    Downloads all of the source data files to the local
    drive and saves them into `data_dir`
    for this application. If `data_dir` is not
    specified, they are downloaded into the current
    directory.
    """

    if not data_dir.strip():
        data_dir = config.data_dir

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
        url = link.url
        print(f"""
downloading {key} from:
{url}""")

        filename = url.split("/")[-1].split("?")[0]
        if link.filename:
            filename = link.filename
        wget.download(url, out=os.path.join(data_dir, filename))

    end = arrow.utcnow()
    delta = end.humanize(start, only_distance=True)
    print(f"""
{len(urls)} files downloaded in {delta}
""")


def main():
    """Show the path to the `data_dir` where school data is stored.

    """
    print(f"""
{"*"*80}
Data directory:
{config.data_dir}

Change this by setting the environment variable:
NYC_SCHOOLS_DATA_DIR
""")


if __name__ == "__main__":
    main()
