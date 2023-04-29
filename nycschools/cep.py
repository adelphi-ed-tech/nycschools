# NYC School Data
# Copyright (C) 2023. Matthew X. Curinga
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
import re

import pandas as pd
import requests


from . import config, schools



def get_ceps():
    stem = config.urls["cep"].url_stem
    df = schools.load_school_demographics()
    df = df[df.ay == df.ay.max()]
    out_dir = os.path.join(config.data_dir, "ceps")
    os.makedirs(out_dir, exist_ok=True)
  
    def download(dbn):
        url = f"{stem}cep_{dbn[2:]}.pdf"
        out = os.path.join(out_dir, f"{dbn}.pdf")
        if not os.path.exists(out):
            r = requests.get(url)
            if r.status_code == 200:
                with open(out, "wb") as f:
                    f.write(r.content)
                return None
            else:
                print(f"Error downloading {dbn}: {r.status_code}")
                return dbn
    not_found = df.dbn.apply(download)