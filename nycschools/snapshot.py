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
import pandas as pd
import numpy as np
import wget

import os.path
import zipfile

from . import schools
from . import config
import shutil

urls = config.urls


def load_snapshots():
    """
    Loads the "snapshot" data from the NYC DOE data portal.
    This data contains core columns only for all "school types"
    mainly focusing on school demographics and teacher demographics.
    """
    path = os.path.join(config.data_dir, "nysed-exams.feather")
    return pd.read_feather(path)
