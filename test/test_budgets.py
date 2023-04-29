import pytest
from nycschools import budgets, config
import os, os.path

datafile = os.path.join(config.data_dir, config.urls["galaxy"].filename)
expected_cols = ['item', 'positions', 'budget', 'category', 'grade', 'service',
                 'subject', 'dbn', 'ay']

def test_open_webdriver():
    driver = budgets.open_webdriver()
    driver.get("https://www.example.com")
    html = driver.page_source
    assert "Example Domain" in html


def test_get_galaxy_summary():
    driver = budgets.open_webdriver()
    data = budgets.get_galaxy_summary("01M015", 2022, driver)
    driver.quit()
    assert set(data.columns) == set(expected_cols)
    assert len(data) > 5


@pytest.mark.skip(reason="too slow for normal testing")
def test_get_galaxy_budgets():
    if os.path.exists(datafile):
        os.remove(datafile)
    data, not_found = budgets.get_galaxy_budgets()
    assert set(data.columns) == set(expected_cols)
    assert len(data) > 100_000
    assert len(not_found) > 50
    assert os.os.path.exists(datafile)


def test_load_galaxy_budgets():
    data = budgets.load_galaxy_budgets()
    assert set(data.columns) == set(expected_cols)
    assert len(data) > 100_000
    assert len(data[data.dbn.isnull()]) == 0
