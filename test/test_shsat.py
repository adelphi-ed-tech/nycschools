import pytest
from nycschools import shsat, config
import os

def test_load_admission_offers():
    df = shsat.load_admission_offers()


    cols = {'ay', 'dbn', 'feeder_name', 
            'hs_applicants_n', 'offers_n', 'testers_n'}
    
    assert cols.issubset(df.columns)
    assert df.ay.nunique() > 5
    assert df.dbn.nunique() > 500

def test_save_administration_offers():
    df = shsat.save_administration_offers()
    f = os.path.join(config.data_dir, config.urls["shsat_apps"].filename)
    # assert os.path.exists(f), "File not found " + f

