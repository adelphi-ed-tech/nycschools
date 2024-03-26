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

from requests import Session
import pandas as pd
import os

from concurrent.futures import ThreadPoolExecutor, as_completed


from . import config
from .dataloader import load


def load_snapshots():
    """
    Loads the "snapshot" data from the NYC DOE data portal.
    This data contains core columns only for all "school types"
    mainly focusing on school demographics and teacher demographics.
    """
    filename = config.urls["snapshots"].filename
    return load(filename)


def get_snapshot_schools():
    """
    Returns the list of schools in the snapshot data.
    """

    results = []


    def read_year(year, file):
        try:
            url = f"https://tools.nycenet.edu/vue-assets/static/data/sqs/{year}/{file}.csv"
            x = pd.read_csv(url)
            x["year"] = year
            return x
        except:
            print("no data,", year)
            return pd.DataFrame()


    for year in range(2016, 2023):
        results.append(read_year(year, "school_info"))
        results.append(read_year(year, "school_info_pk"))


    doe = pd.concat(results, axis=0)
    return doe
    # path = os.path.join(config.data_dir, "snapshot_school_list.csv")
    # doe.to_csv("snapshot_school_list.csv", index=False)
    return doe
    


