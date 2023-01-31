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


def get_data_dir():
    return config.data_dir


def download_cache(data_dir=""):
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
    if not data_dir.strip():
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

You can change the data dir by updating your config file, located at:
{config.config_file}

or by setting the environment variable:
NYC_SCHOOLS_DATA_DIR
""")


if __name__ == "__main__":
    main()
