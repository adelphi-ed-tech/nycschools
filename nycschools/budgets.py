# NYC School Data
# Copyright (C) 2023. Matthew X. Curinga
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
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from . import config, schools

import dotenv
dotenv.load_dotenv()

__galaxyfile = os.path.join(config.data_dir, config.urls["galaxy"].filename)



def load_galaxy_budgets():
    """Loads the galaxy budgets from the local cache.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    data : pandas.DataFrame
        A single DataFrame that combines all of the budget data scraped from the web
        for all schools in the database."""   

    return pd.read_csv(__galaxyfile)

def open_webdriver():
    """Opens a Selenium webdriver using the Chrome/Chromium 
engine for Selenium. If the environment variables `CHROME_PATH` 
and `CHROMEDRIVER_PATH` are set, they will be used to 
initialize the webdriver. Otherwise, the webdriver will be 
initialized using the default installation."""

    # don't launch the browser GUI
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    # if the environment variables are set, use them
    chrome_path = os.environ.get("CHROME_PATH", None)
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", None)

    if chrome_path:
        chrome_options.binary_location = chrome_path
    if chromedriver_path:
        s = Service(chromedriver_path)
        return webdriver.Chrome(service=s, options=chrome_options)

    return webdriver.Chrome(options=chrome_options)

def __fix_cols(data, sections, dbn):
    """normalizes column names from scraped data."""

    col_map = {
        'title': 'item',
        'assignment': 'item',
        'organizational category': 'item',
        'total': 'item',
        'total.1': 'item',
        'grand total': 'item',
        'type of class/service': 'service'
    }


    data = data.copy()
    
    for i, section in enumerate(sections):
        data[i]["category"] = section
        data[i].columns = [c.lower() for c in data[i].columns]
        data[i].rename(columns=col_map, inplace=True)
        school_col = [c for c in data[i].columns if c.lower().startswith(dbn.lower())]
        if len(school_col) > 0:
            data[i].rename(columns={school_col[0]: 'item'}, inplace=True)
    return data


def get_galaxy_summary(dbn, ay, driver):
    """Gets the 'galaxy summary' budget for a school from the DOE website.
    
    Parameters
    ----------
    dbn : str
        The school's DBN.
    ay : int
        The school year, currently only the most recent school year (2022-2023) is available.
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        The Selenium webdriver.
        
    Returns
    -------
    data : pandas.DataFrame
        A single DataFrame that combines all of the budget data scraped from the web
        for the school specified by `dbn` and `ay`."""

    url_stem = config.urls["galaxy"].url_stem
    url = f"{url_stem}{dbn[2:]}"

    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    # use the section header as row category
    sections = [section.get_text().strip() for section in soup.select('.TO_Section')]
    data = pd.read_html(html)
    data = __fix_cols(data, sections, dbn)
    data = pd.concat(data)
    data["dbn"] = dbn
    data["ay"] = ay

    return data

def get_galaxy_budgets():
    """Scrapes the 'galaxy summary' budget for all schools from the DOE website."""
    df = schools.load_school_demographics()
    dbns = df[df.district < 33].dbn.unique()
    driver = open_webdriver()
    budgets = []
    not_found = []
    for dbn in dbns:
        try:
            budgets.append(get_galaxy_summary(dbn, 2022, driver))
        except ValueError:
            not_found.append(dbn)
        except:
            print(f"Error scraping {dbn}")
            not_found.append(dbn + "*")

    data = pd.concat(budgets)
    data.item = data.item.str.lower()
    data.to_csv(__galaxyfile, index=False)

    return data, not_found