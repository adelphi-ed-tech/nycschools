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
import os.path

import pandas as pd


from . import config


def save_class_size():
    """Loads and cleans class size data for each year that it is available
    in the `datasets`. Currently data is available for each year from
    2009-2021 excluding the 2020-2021 school year.

    Returns
    -------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
        in the data portal

    """

def load_class_size(ay, url):
    df = pd.read_csv(url)

    boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}

    df["ay"] = ay

    df = df.rename(columns=demo.default_map)

    return df

