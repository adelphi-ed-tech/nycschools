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
from . import config
from nycschools.dataloader import load


def load_snapshots():
    """
    Loads the "snapshot" data from the NYC DOE data portal.
    This data contains core columns only for all "school types"
    mainly focusing on school demographics and teacher demographics.
    """
    filename = config.urls["snapshots"].filename
    return load(filename)
