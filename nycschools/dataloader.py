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
from types import SimpleNamespace
import json

import wget
import arrow

from . import config


def load_data_files(data_dir=""):
    """Downloads all of the source data files to the local
    drive and saves them into `platformdirs.site_data_dir`
    for this application."""

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