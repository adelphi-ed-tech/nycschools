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
urls = config.urls

def load_class_size():
    pass

def get_class_22():


    url = urls["class_size"].data_urls["2022"]
    xls = pd.read_excel(url, sheet_name=None)
    # first sheet is k-8
    k8 = xls["K-8 Avg"]
    hs = xls["MS HS Avg"]
    ptr = xls["PTR"]

    df = pd.concat([k8, hs], axis=0)
    df["ay"] = 2022

    df.columns = ['dbn', 'school_name', 'grade', 'program_type',
                'students_n', 'classes_n', 'avg_class_size',
                'min_class_size', 'max_class_size', 'dept', 'subject',
                'ay']


    def fix_rows(row):
        if row.min_class_size == "<15":
            row.min_class_size = row.students_n
        if row.max_class_size == "<15":
            row.max_class_size = row.students_n
        if row.grade in ['K', 1, 2, 3, 4, 5,]:
            row.subject = "Elementary"
            row.dept = "Elementary"
        if row.program_type == "ICT" and not row.dept:
            row.dept = "ICT"
        if row.program_type == "ICT" and not row.subject:
            row.dept = "ICT"

        return row

    df = df.apply(fix_rows, axis=1)
    return df, ptr


def get_class_size():
    """Loads and cleans class size data for each year that it is available
    in the `datasets`. Currently data is available for each year from
    2009-2021 excluding the 2020-2021 school year.

    Returns
    -------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
        in the data portal

    """
    years =[]
    for url in urls.class_size.data_urls:
        df = load_class_size(url.ay, url.url)
        years.append(df)
    df = pd.concat(years)
    df.to_csv(os.path.join(config.data_dir, "class_size.csv"), index=False)

def load_class_size(ay, url):
    df = pd.read_csv(url)

    boros = {"K":"Brooklyn", "X":"Bronx", "M": "Manhattan", "Q": "Queens", "R": "Staten Island"}

    df["ay"] = ay

    df = df.rename(columns=demo.default_map)

    return df

