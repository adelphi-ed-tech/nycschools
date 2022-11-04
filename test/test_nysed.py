import pytest
import pandas as pd
import os.path
from nycschools import config, nysed
from test_exams import check_state_test

# @pytest.mark.skip(reason="too slow for normal testing")
def test_load_nysed_ela_math_archives():
    df = nysed.load_nysed_ela_math_archives()
    check_state_test(df)

    tmp = os.path.join(config.data_dir, "tmp")
    assert not os.path.exists(tmp), "temp files not cleaned up"

    feather = os.path.join(config.data_dir, "nysed-exams.feather")
    df = pd.read_feather(feather)
    check_state_test(df)

    csv = os.path.join(config.data_dir, "nysed-exams.csv")
    df = pd.read_csv(csv)
    check_state_test(df)


def test_load_nys_nysed():
    df = nysed.load_nys_nysed()
    n = len(df)
    assert n > 2_400_000, f"Only ({n}) records found"
    check_state_test(df)


def test_load_nyc_nysed():
    df = nysed.load_nyc_nysed()
    n = len(df)
    assert n > 680_000, f"Only ({n}) records found"
    check_state_test(df)
