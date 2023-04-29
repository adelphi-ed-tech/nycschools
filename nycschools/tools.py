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


# demo_cols = set(demo.columns)
# geo_cols = set(df.columns)
# demo_cols.intersection(geo_cols)

def quick_merge(a, b, on="dbn"):
    
    diff = list(a.columns.intersection(b))

    diff.remove(on)
    a = a.copy()
    a.drop


    return a[diff].merge(b,how="inner",on=on)
