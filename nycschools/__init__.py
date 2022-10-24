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
    data = importlib.resources.read_text("nycschools", "dataurls.json")
    urls = json.loads(data)
    for k,v in urls.items():
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
