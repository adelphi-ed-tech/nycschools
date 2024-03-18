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
import platform
import subprocess
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import pandas as pd
import geopandas as gpd

from yaspin import yaspin
from yaspin.spinners import Spinners

# from . import config, schools, exams, budgets, geo, nysed, shsat
from . import config
from .tools import suppress_warnings

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_data_dir():
    return config.data_dir


def read_file(path):
    if path.endswith(".geojson"):
        return gpd.read_file(path)
    elif path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".feather"):
        return pd.read_feather(path)
    else:
        raise ValueError(f"Unknown file type: {path}")

def write_file(df, path):
    if path.endswith(".geojson"):
        df.to_file(path, driver="GeoJSON")
    elif path.endswith(".csv"):
        df.to_csv(path, index=False)
    elif path.endswith(".feather"):
        df.to_feather(path)
    else:
        raise ValueError(f"Unknown file type: {path}")

def load(path):
    remote_path = config.urls["datasite"].url + path
    # if config.data_dir is None or config.data_dir == "":
    #     local_path = os.path.join(config.data_dir, path)
    #     if os.path.exists(local_path):
    #         return local_path
    #     else:
    #         df = read_file(remote_path)
    #         write_file(df, local_path)
    #         return df
    return read_file(remote_path)

def download_file(url, local_filename):
    """Optimize file download using requests library."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

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
    resp = requests.get(url)
    with open(archive, "wb") as f:
        f.write(resp.content)

    with py7zr.SevenZipFile(archive, mode='r') as z:
        z.extractall(path=data_dir)

    os.remove(archive)
    return data_dir


def get_venv_activate():
    """Finds the activation script for a running virtual environment
    or `None` if not running a venv."""

    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        return os.path.join(venv_path, 'bin', 'activate')
    return None


def find_config_file():
    """Looks for virtual environment activation scripts
    or bash configuration files in known locations.
    
    Returns:
        str: the path to the configuration file or `None` if not found
    """
    paths = [
        get_venv_activate(),
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.bash_profile"),
        os.path.expanduser("~/.profile")
    ] 
    
    for path in paths:
        if path and os.path.exists(path):
            return path
    
    warnings.warn(f"""Could not find a venv or bash configuration file to edit.
You should manually set the NYC_SCHOOLS_DATA_DIR environment variable.
See the full documentation at: {config.urls["docbook"].url}""")
    
    return None
    


def set_env_var(data_dir):
    """Attempts to set the NYC_SCHOOLS_DATA_DIR environment variable
    based on the user's platform."""

    # This will return 'Windows', 'Linux', or 'Darwin' (for macOS)
    os_type = platform.system()

    if os_type == "Windows":
        subprocess.run(["setx", "NYC_SCHOOLS_DATA_DIR", data_dir])
    elif os_type in ["Linux", "Darwin"]:
        config_path = find_config_file()
        if not config_path:
            return
        print("Writing env var to", config_path)
        with open(config_path, "a") as f:
            f.write(f"export NYC_SCHOOLS_DATA_DIR={data_dir}\n")
        print(f"""To access the data files in your current terminal session,
you must run the following command:
source {config_path}
""")



def download_cache():
    """Download the data archive and save it to the local drive.
    This interactive terminal program prompts the user for
    the location to save the data files. Once the files
    are downloaded and expanded it attempts to write the path
    to the data files into the python configuration environment.
    """
    print("Default data location:", config.data_dir)
    data_dir = ""

    def prompt_data():
        path = input("Enter the path to the data directory (or <enter> for default): ")
        if path == "":
            path = config.data_dir
        # check if it exists, if not create it, catch errors and re-prompt
        try:
            print("Creating data cache: ", path)
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
    auto_config = input("Automatically set environment variable? [Y/n]: ")
    if auto_config.lower() == "y" or len(auto_config) == 0:
        set_env_var(data_dir)
        print("Environment variable set.")
    else:
        print("""You must configure the NYC_SCHOOLS_DATA_DIR environment variable.
See the full documentation at: {config.urls["docbook"].url}""")


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

