import pytest
import numpy as np
import pandas as pd
from sklearn.metrics import mutual_info_score
import os.path
from nycschools import config
from nycschools import segregation as seg


test_M = 0.4255390
test_H = 0.4188083

def test_mutual_information():
    path = os.path.join(config.data_dir, "segdata.feather")
    df = pd.read_feather(path)

    M, H = seg.mutual_information(df, group="race", unit="school")
    assert abs(M - test_M) < 1e-6, f"Mutual information is {M}, not {test_M}"
    assert abs(H - test_H) < 1e-6, f"Theil H-index is {H}, not {test_H}"


def test_entropy():
    random_probs = np.random.rand(4)

    random_probs /= random_probs.sum()  # Normalize to sum to 1

    # Calculate the entropy of the random probability distribution
    ent = seg.entropy(random_probs)


    path = os.path.join(config.data_dir, "segdata.feather")
    df = pd.read_feather(path)
    N = df["n"].sum()
    p_u = df.groupby("school")["n"].sum() / N
    p_g = df.groupby("race")["n"].sum() / N
    group_E = 1.016071
    unit_E = 7.541018
    ge = seg.entropy(p_g)
    ue = seg.entropy(p_u)
    assert abs(ge - group_E) < 1e-4, f"Group entropy is {ge}, not {group_E}"
    assert abs(ue - unit_E) < 1e-4, f"Group entropy is {ue}, not {unit_E}"
    
def test_dissimilarity():
    test_data = pd.DataFrame(columns=["u","b","w"], data=[[1,50,10],[2,200,40],[3,10,100],[4,30,200],[5,10,150]])
    test_data = test_data.melt(id_vars="u", value_vars=["b","w"], var_name="g", value_name="n")
    D = seg.dissimilarity(test_data, "b")
    assert abs(D - 0.73) < .01
