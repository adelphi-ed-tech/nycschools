# NYC School Data
# Copyright (C) 2022-23. Matthew X. Curinga
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

from .dataloader import load
from . import config

def load_admission_offers():
    return load(config.urls["shsat_apps"].filename)


def save_administration_offers():
    data_urls = config.urls["shsat_apps"].data_urls

    def shsat(ay, url):
        data = pd.read_csv(url)
        data.columns = ["dbn", "feeder_name", "hs_applicants_n", "testers_n", "offers_n"]
        data["ay"] = ay
        data["hs_applicants_n"] = data.hs_applicants_n.apply(lambda x: 2 if x == "0-5" else x)
        data["offers_n"] = data.offers_n.apply(lambda x: 2 if x == "0-5" else x)
        data["testers_n"] = data.testers_n.apply(lambda x: 2 if x == "0-5" else x)
        return data

    df = pd.concat([shsat(url, ay) for url, ay in data_urls.items()])
    df.hs_applicants_n = pd.to_numeric(df.hs_applicants_n, errors='coerce').astype('Int64')
    df.testers_n = pd.to_numeric(df.testers_n, errors='coerce').astype('Int64')
    df.offers_n = pd.to_numeric(df.offers_n, errors='coerce').astype('Int64')
    df["offers_pct"] = df.offers_n / df.testers_n
    f = os.path.join(config.data_dir, config.urls["shsat_apps"].filename)
    df.to_csv(f, index=False)
    return df