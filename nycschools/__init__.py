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
from .datasets import urls as __urls


def get_version():
    """Returns the version of the nycschools package"""
    return "0.1.0"

def __read_urls__():
    """Reads the urls from the datasets module"""
    urls = {}
    for k,v in __urls.items():
        urls[k] = SimpleNamespace(**v)
    return urls


def get_config():
    """initializes configuration settings.
    Determines the location for local data files by first
    looking for an environment variable called NYC_SCHOOLS_DATA_DIR

    If this ENV variable is not set, 
    data files are stored in a directory called `school-data` in the current
    directory. If this directory does not exist, it is created.

    To see (and see how to change) these settings for your installation,
    run `python -m nycschools.dataloader`

    Returns:
        SimpleNamespace: a namespace object with the following attributes:
            data_dir: the path to the data directory
            urls: a dictionary of urls to download data if the local
                  cache should be re-built
    """

    env_dir = os.environ.get("NYC_SCHOOLS_DATA_DIR", None)
    local = os.path.join(".", "school-data")
    config = {}
    if env_dir:
        config["data_dir"] = env_dir
    else:
        config["data_dir"] = local
    
    if not os.path.exists(config["data_dir"]):
        os.mkdir(config["data_dir"])
            
    config["urls"] = __read_urls__()
    return SimpleNamespace(**config)


config = get_config()
