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

from .dataloader import load
from . import config
urls = config.urls
__class_size_file = os.path.join(config.data_dir, config.urls["class_size"].filename)
__ptr_file = os.path.join(config.data_dir, config.urls["class_size"].filename_ptr)

def load_class_size():
    return load(config.urls["class_size"].filename)

def load_ptr():
    return load(config.urls["class_size"].filename_ptr)

def get_class_22(url):
    """Read class size data for 2022 from
       the DOE InfoHub Excel file format.
       This data also contains pupil teacher ratios
       which are saved in a separate file.
    """

    xls = pd.read_excel(url, sheet_name=None)
    # first sheet is k-8
    k8 = xls["K-8 Avg"]
    hs = xls["MS HS Avg"]
    ptr = xls["PTR"]
    ptr.columns = ['dbn', 'school_name', 'ptr']
    ptr["ay"] = 2022

    df = pd.concat([k8, hs], axis=0)
    df["ay"] = 2022

    df.columns = ['dbn', 'school_name', 'grade', 'program_type',
                'students_n', 'classes_n', 'avg_class_size',
                'min_class_size', 'max_class_size', 'dept', 'subject',
                'ay']

    return df, ptr


def get_class_size_year(ay, url):
    def fix_rows(row):
        if row.min_class_size == "<15":
            row.min_class_size = row.students_n
        if row.max_class_size == "<15":
            row.max_class_size = row.students_n
        if row.grade in ['K', 1, 2, 3, 4, 5,]:
            row.subject = "Elementary"
            row.dept = "Elementary"
        return row

    if (ay == 2022):
        df, ptr = get_class_22(url)

        ptr.to_csv(__ptr_file, index=False)
    else:
        df = pd.read_csv(url, dtype={'dbn': str})
        df["ay"] = ay
        df.rename(columns={
            "number_of_students": "students_n", 
            "grade_level": "grade",
            "number_of_classes":"classes_n",
            "minimum_class_size":"min_class_size",
            "maximum_class_size":"max_class_size",
            "average_class_size":"avg_class_size"
            }, inplace=True)
        
    df = df.apply(fix_rows, axis=1)
    return df


def get_class_size():
    """Get class size data from the web and cleans class 
    size data for each year that it is available
    in the `datasets`. Currently data is available for each year from
    2009-2021 excluding the 2020-2021 school year.

    Returns
    -------
    DataFrame
        a pandas DataFrame holding school demographic data for all of the schools
        in the data portal

    """
    years =[]
    for ay, url in urls["class_size"].data_urls.items():
        data = get_class_size_year(int(ay), url)
        years.append(data)
    df = pd.concat(years)
    df.to_csv(__class_size_file, index=False)
    return df



