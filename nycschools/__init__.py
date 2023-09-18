# NYC School Data
# Copyright (C) 2022-2023. Matthew X. Curinga
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
import warnings
import os.path
from types import SimpleNamespace
from .datasets import urls as __urls


def get_version():
    """Returns the version of the nycschools package"""
    return "0.1.0"

def __read_urls():
    """Reads the urls from the datasets module"""
    urls = {}
    for k,v in __urls.items():
        urls[k] = SimpleNamespace(**v)
    return urls


def get_config():
    """Initialize the configuration settings.

Parameters
----------
None

Returns
-------
SimpleNamespace : 
    A namespace object with the following attributes:
    - data_dir : str
        The path to the data directory.
    - urls : dict
        A dictionary of URLs to download data if the local cache should be re-built.

Notes
-----
The location for local data files is determined by first looking for an environment variable called `NYC_SCHOOLS_DATA_DIR`. If this environment variable is not set, the data files are stored in a directory called `school-data` in the current directory. If this directory does not exist, it will be created.

To see and change these settings for your installation, run `python -m nycschools.dataloader`.
"""

    env_dir = os.environ.get("NYC_SCHOOLS_DATA_DIR", None)
    pwd = os.getcwd()
    local = os.path.join(pwd, "school-data")
    config = {}
    if env_dir:
        config["data_dir"] = env_dir
    else:
        config["data_dir"] = local
    
    if not os.path.exists(config["data_dir"]):
        no_data = f"""The data directory {config["data_dir"]} does not exist.
Run python -m nycschools.dataloader to download the data.
Please visit documentation on how to download the data at:
https://adelphi-ed-tech.github.io/nycschools/install.html

If you have downloaded the data and are seeing this warning, you may
need to set the environment variable NYC_SCHOOLS_DATA_DIR to the
path to the data directory.
"""

        warnings.warn(no_data)

    config["urls"] = __read_urls()

    return SimpleNamespace(**config)


config = get_config()
