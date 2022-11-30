# NYC School Data
# Copyright (C) 2022. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
import os
import os.path
import importlib.resources
import json
from types import SimpleNamespace
from platformdirs import PlatformDirs

# theser are the URLs into the open data portals
# update when new datasets are released
__urls = {
  "demographics": {
    "url": "https://data.cityofnewyork.us/resource/vmmu-wj3w.csv?$limit=1000000",
    "filename":"school-demographics.csv",
    "desc": "School demographic data from NYC Open Data Portal"
  },
  "school_geo": {
    "url": "https://data.cityofnewyork.us/resource/a3nt-yts4.geojson?$limit=1000000",
    "filename":"school-zipcodes.geojson",
    "desc": "location points with zipcodes"
  },
  "school_locations": {
    "url": "https://data.cityofnewyork.us/resource/wg9x-4ke6.csv?$limit=1000000",
    "filename":"school-locations.csv",
    "desc": "x,y geolocations and location meta data"
  },
  "district_geo": {
    "url": "https://data.cityofnewyork.us/api/geospatial/r8nu-ymqj?method=export&format=GeoJSON",
    "filename":"district-shapes.geojson",
    "desc": "shape file for school districts"
  },
  "charter_ela": {
    "url": "https://data.cityofnewyork.us/resource/sgjd-xi99.csv?$limit=1000000",
    "filename":"charter-ela.csv",
    "desc": "charter school 3-8 ELA results"
  },
  "charter_math": {
    "url": "https://data.cityofnewyork.us/resource/3xsw-bpuy.csv?$limit=1000000",
    "filename":"charter-math.csv",
    "desc": "charter school 3-8 math results"
  },
  "nyc_ela": {
    "url": "https://data.cityofnewyork.us/api/views/hvdr-xc2s/files/4db8f0e7-0150-4302-bed7-529c89efa225?download=true&filename=school-ela-results-2013-2019-(public).xlsx",
    "filename":"nyc-ela.csv",
    "desc": "excel file with non-charter school ELA test results with demographic categories"
  },
  "nyc_math": {
    "url": "https://data.cityofnewyork.us/api/views/365g-7jtb/files/17910cb0-8a62-4037-84b5-f0b4c2b3f71f?download=true&filename=school-math-results-2013-2019-(public).xlsx",
    "filename":"nyc-math.csv",
    "desc": "excel file with non-charter school math test results with demographic categories"
  },
  "nyc_regents": {
    "url": "https://data.cityofnewyork.us/api/views/2h3w-9uj9/files/ae520e30-953f-47a0-9654-c77900232236?download=true&filename=2014-15-to-2018-19-nyc-regents-overall-and-by-category---public%20(1).xlsx",
    "filename":"nyc-regents.csv",
    "desc": "regents exam results"
  },
  "nysed_math_ela": {
    "comment":"Each test year has its own URL, so this item doesn't match others in format",
    "url":"https://data.nysed.gov/downloads.php",
    "urls": [
      "https://data.nysed.gov/files/assessment/20-21/3-8-2020-21.zip",
      "https://data.nysed.gov/files/assessment/18-19/3-8-2018-19.zip",
      "https://data.nysed.gov/files/assessment/17-18/3-8-2017-18.zip",
      "https://data.nysed.gov/files/assessment/16-17/3-8-2016-17.zip",
      "https://data.nysed.gov/files/assessment/15-16/3-8-2015-16.zip"
    ],
    "filename":"nysed-exams.csv",
    "desc": "NYS grades 3-8 ELA and Math test in a .zip archive"
  }
}

dirs = PlatformDirs("nycschools", "mxc")

config_file = "nycschools.config"
config_paths = [
    os.path.join(dirs.site_config_dir, config_file),
    os.path.join(dirs.user_config_dir, config_file)
]

data_paths = [
    dirs.site_data_dir,
    dirs.user_data_dir
]



def read_urls():
    urls = {}
    for k,v in __urls.items():
        urls[k] = SimpleNamespace(**v)
    return urls


def get_config():

    for path in config_paths:
        if os.path.exists(path):
            with open(path,"r") as f:
                config = json.loads(f.read())
                config["urls"] = read_urls()
                return SimpleNamespace(**config)

    # create a new config in the user space
    path = os.path.join(dirs.user_config_dir, config_file)
    os.makedirs(os.path.dirname(path))
    config = {
        "config_file": path,
        "data_dir": find_data_dir()
    }
    with open(path,"w") as f:
        f.write(json.dumps(config, indent=2))

    config["urls"] = read_urls()
    return SimpleNamespace(**config)


def find_data_dir():
    """Finds a writeable data directory"""
    # if ther's a local data dir with data files in it
    # use that first
    local = os.path.join(".", "school-data")
    if os.path.exists(local):
        files = os.listdir(path)
        # there must be at least one data file already in our list
        if len(files) > 0:
            urls = read_urls()
            datafiles = [url.filename for url in urls]
            for f in datafiles:
                if f in files:
                    return local

    for path in data_paths:
        if check_write_edit_delete(path):
            return path

    if check_write_edit_delete(local):
        return local

    return None


def check_write_edit_delete(path):
    """Checks if path can be a suitable data dir"""

    print("Checking data dir at:", path)
    if os.path.exists(path):
        files = os.listdir(path)
        if len(files) > 0:
            # if the path exists and is not empty, assume it works
            return True
    else:
        try:
            print("trying to make", path)
            os.makedirs(path)
        except:
            return False


    f = os.path.join(path, ".tmp")
    msg = "testing data dir"
    with open(f, "w") as tmp:
        try:
            tmp.write(msg)
        except:
            return False

    with open(f, "r") as tmp:
        try:
            assert tmp.read() == msg
        except:
            return False

    with open(f, "a") as tmp:
        try:
            tmp.write("\nmore data")
        except:
            return False
    try:
        os.remove(f)
    except:
        return False

    return True

config = get_config()
