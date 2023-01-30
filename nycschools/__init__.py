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
import json
from types import SimpleNamespace
from platformdirs import PlatformDirs
from .datasets import urls as __urls

dirs = PlatformDirs("nycschools", "mxc")

__config_file = "nycschools.config"
__config_paths = [
    os.path.join(dirs.site_config_dir, __config_file),
    os.path.join(dirs.user_config_dir, __config_file)
]

__data_paths = [
    dirs.site_data_dir,
    dirs.user_data_dir
]



def __read_urls():
    """Reads the urls from the datasets module"""
    urls = {}
    for k,v in __urls.items():
        urls[k] = SimpleNamespace(**v)
    return urls


def get_config():
    """initializes configuration settings.
    First, looks for an environment variable called NYC_SCHOOLS_DATA_DIR
    NYC_SCHOOLS_DATA_DIR is the path to a read/write directory where data files
    can be stored.

    If this ENV variable is not set, it looks for a local config file.

    It looks for writeable directories in the following order:
    1. `school-data` in the current directory
    2. `platformdirs.site_data_dir`
    3. `platformdirs.user_data_dir`

    To see (and see how to change) these settings for your installation,
    run `python -m nycschools.dataloader`

    Returns:
        SimpleNamespace: a namespace object with the following attributes:
            config_file: the path to the config file
            data_dir: the path to the data directory
            urls: a dictionary of urls to download data from    
    """

    env_dir = os.environ.get("NYC_SCHOOLS_DATA_DIR", None)
    for path in __config_paths:
        if os.path.exists(path):
            with open(path,"r") as f:
                config = json.loads(f.read())
                config["urls"] = __read_urls()
                # env var always overrides config file
                if env_dir:
                    config["data_dir"] = env_dir
                return SimpleNamespace(**config)


    # create a new config in the user space
    path = os.path.join(dirs.user_config_dir, __config_file)
    print("config file path:", path)

    # create the directory if it doesn't exist
    # the directory might exist due to previous install
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    
    
    config = {
        "config_file": path,
        "data_dir": find_data_dir(__data_paths, env_dir)
    }
    with open(path,"w") as f:
        f.write(json.dumps(config, indent=2))

    config["urls"] = __read_urls()
    return SimpleNamespace(**config)


def find_data_dir(data_paths, env_dir):
    """Finds a writeable data directory"""
    # if ther's a local data dir with data files in it
    # use that first
    
    local = os.path.join(".", "school-data")
    if env_dir:
        data_paths = [env_dir] + data_paths
    
    data_paths.append(local)

    for path in data_paths:
        if check_write_edit_delete(path):
            return path

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
