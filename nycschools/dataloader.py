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
import py7zr
import requests
import sys
import warnings
from yaspin import yaspin
from yaspin.spinners import Spinners

from . import config

def get_data_dir():
    return config.data_dir


def download_data():
    path = find_data_dir(config)
    if path:
        config.data_dir = path
        return path
    
    return download_archive(config.data_dir)


def find_data_dir(config):
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
    # first look locally
    for path in paths:
        if path and os.path.exists(path) and contains_data_files(path):
            config.data_dir = path
            return path
    # if not, try to mount a google drive
    path = mount_colab_data_dir()
    if path and contains_data_files(path):
        config.data_dir = path
        return path
    return None


def mount_colab_data_dir():
    """Try to mount a google drive directory in colab
    and then search for the data directory by looking
    for a directory with the known name 'nyc-schools-data'."""

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
You can download the data files by running: `python -m nycschools.dataloader -d`
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
        print("no data dir")
        data_dir = config.data_dir
    else:
        config.data_dir = data_dir

    print("using data dir", data_dir)

    url = config.urls["school-data-archive"].url
    filename = config.urls["school-data-archive"].filename
    data_dir = os.path.abspath(data_dir)
    archive = os.path.join(data_dir, filename)
    print("7zip", archive)
    resp = requests.get(url)
    with open(archive, "wb") as f:
        f.write(resp.content)

    with py7zr.SevenZipFile(archive, mode='r') as z:
        z.extractall(path=data_dir)

    os.remove(archive)
    return data_dir


def get_venv_activate():

    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        return os.path.join(venv_path, 'bin', 'activate')
    return None

def download_cache():
    data_dir = ""

    def prompt_data():
        path = input("Enter the path to the data directory (or <enter> for default): ")
        # check if it exists, if not create it, catch errors and re-prompt
        try:
            os.makedirs(path, exist_ok=True)
        except:
            print(f"Could not create directory {path}")
            return prompt_data()
        
        # check if it's writeable
        if not os.access(path, os.W_OK):
            print(f"Cannot write to directory {path}")
            print("Either change file permissions or choose a different directory.")
            return prompt_data()
        return path

    data_dir = prompt_data()
    print(f"Downloading school data to {data_dir}")

    with yaspin(text="loading...", spinner=Spinners.bouncingBall) as sp:
        sp.side = "right"
        data_dir = download_archive(data_dir)
        sp.ok("✔")

    print(f"Data successfully saved to: {data_dir}")

    venv_path = get_venv_activate()
    if venv_path:
        print(f"""
To use the NYC Schools data, you must set the NYC_SCHOOLS_DATA_DIR environment variable.
You can set this in your virtual environment activation script 
and then load the settings by executing the following commands:
              
echo 'export NYC_SCHOOLS_DATA_DIR={data_dir}' >> {venv_path}
source {venv_path}

""")
    else:
        print(f"""
To use the NYC Schools data, you must set the NYC_SCHOOLS_DATA_DIR environment variable.
- Linux/MacOS: export NYC_SCHOOLS_DATA_DIR={data_dir}
- Windows: set NYC_SCHOOLS_DATA_DIR={data_dir}

See the full documentation at:
{config.urls["docbook"].url}

""")

def main():
    """Show the path to the `data_dir` where school data is stored.
To use the interactive downloader, run `python -m nycschools.dataloader -d`.
    """
    print(f"Current data directory: {config.data_dir}")

    # read args if exists
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("docs", main.__doc__)
            return
        elif sys.argv[1] == "-d" or sys.argv[1] == "--download":
            download_cache()
            return
        else:
            print("Unrecognized argument. Run `python -m nycschools.dataloader --help` for help.")
            return
    

if __name__ == "__main__":
    main()
