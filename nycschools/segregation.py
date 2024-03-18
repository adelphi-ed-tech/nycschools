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
"""
This package groups together several functions for
analyzing segregation within groups. It is tested
in reference to segregation patterns in NYC Public Schools.

References
-----------

Allen, R., & Vignoles, A. (2007). What should an index of school segregation measure? _Oxford Review of Education_, _33_(5), 643–668. https://doi.org/10.1080/03054980701366306

Elbers, B. (2021). A Method for Studying Differences in Segregation Across Time and Space. Sociological Methods & Research. https://doi.org/10.1177/0049124121986204
[code](https://elbersb.github.io/segregation/index.html)

Frankel, D. M., & Volij, O. (2011). Measuring school segregation. _Journal of Economic Theory_, _146_(1), 1–38. https://doi.org/10.1016/j.jet.2010.10.008

Reardon, S. F., & O’Sullivan, D. (2004). Measures of Spatial Segregation. _Sociological Methodology_, _34_(1), 121–162. https://doi.org/10.1111/j.0081-1750.2004.00150.x

Sakoda, J. M. (1981). A Generalized Index of Dissimilarity. _Demography_, _18_(2), 245–250. https://doi.org/10.2307/2061096


"""

import pandas as pd
import numpy as np


def entropy(probabilities):
    """
    Calculate the entropy of a list of probabilities.
    """
    p = [p for p in probabilities if p > 0]
    return -np.sum(p * np.log(p))

def mutual_information(df, group="g", unit="u", n="n"):
    data = df.copy()

    N = data[n].sum()
    # marginal probabilities
    data['p_ug'] = data[n] / N
    p_u = data.groupby(unit)[n].sum() / N  # each unit
    p_g = data.groupby(group)[n].sum() / N  # each group

    data['p_u'] = data[unit].map(p_u)
    data['p_g'] = data[group].map(p_g)
    M = np.sum(data['p_ug'] * np.log(data['p_ug'] / (data['p_u'] * data['p_g'])))
    E = entropy(p_g)
    H = M / E
    return M, H

def dissimilarity(df, cat, group="g", unit="u", n="n"):
    """Calculate the dissimilarity index for a group
    compared to the non-group population.

    Parameters
    ----------
    df : DataFrame
        A DataFrame in "long" format with columns for the group (g), the unit (u), and the
        total population (n). Each row represents the population at a group-unit intersection.
        In our school data, the unit would be the school (identified by DBN) the group
        would be one of the racial/ethnic categories (black, asian) or other demographic
        category (poverty, ELL, SWD) and the population would be the enrollment number
        of that group at that school (40 ELL students at 13K009).
    cat : str
        The category to compare to the non-group population. For example, "white" or "black".
        If there are four distinct values in the group column (e.g. "white", "black", "hispanic", "asian"),
        and cat is "white", then the dissimilarity index will be calculated for the white population
        against the total non-white population.
    group : str
        The name of the column in `df` that contains the group labels.
    unit : str
        The name of the column in `df` that contains the unit labels. (e.g. "school", "zipcode", "tract", "state")
    n : str
        The name of the column in `df` that contains the population counts.

    Returns
    -------
    float
        The dissimilarity index (D) for the group compared to the non-group population.
        D is a number between 0 and 1, where 0 indicates perfect integration and 1 indicates
        complete segregation.
    
    """
    data = df.copy()

    N = data[n].sum() # total population
    group_data = data[data[group] == cat] # just the rows for our group
    G = group_data[n].sum() # group population
    X = N - G # non-group population

    G_i = group_data[n]  # group at each location
    N_u = data.groupby(unit)[n].sum()
    N_u = group_data[unit].map(N_u)
    X_i = N_u - G_i

    P_g = G_i / G
    P_o = X_i / X
    D = np.sum(np.abs(P_g - P_o)) / 2

    return D

