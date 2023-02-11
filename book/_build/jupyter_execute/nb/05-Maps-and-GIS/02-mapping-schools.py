#!/usr/bin/env python
# coding: utf-8

# Layered Maps
# ============
# This mapping examples uses both the district maps and school location data to create visualizations and interactive maps.
# 
# Examples include:
# - calling multiple plots to create map layers
# - changing the mouse over and mouse click data for interaction
# 

# In[1]:


import pandas as pd
import geopandas as gpd
import folium
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown as md

from nycschools import schools, exams, ui, geo


from IPython.display import display, HTML


# In[2]:


# load and clean the school demographics and school location data
demo = schools.load_school_demographics()
df = geo.load_school_locations()
districts = geo.load_districts()


# Plotting twice: schools inside of districts
# --------------------------------------------
# In the code above, we've loaded the school demographic data and merged it with the school location data. `districts` contains the shape files for the
# 32 geographic districts in the NYC Schools.
# 
# In the cell below, we create a new figure and axis and then plot both the `districts` and the `schools` using `ax` -- the same axis. This makes a graph where schools are plotted on top of the districts.

# In[3]:


# create the plot
fig, ax = plt.subplots(figsize=(16, 16))

# first, plot the districts onto `ax`
districts.plot(ax=ax)
# second, plot the schools onto `ax`
_ = df.plot(ax=ax,color="red")


# Folium map with styles
# -----------------------
# We've seen how the `explore()` function generates an interactive, geographic [Folium](https://python-visualization.github.io/folium/) map. In this example we create an interactive district map where we specificy more of the styles for the map to give it a unique look. We save the map into the `district_map` variable because we're going to re-use it later.[link text](https://)

# In[4]:


district_map = districts.explore(
     column="district", # use district for the categories (aka chloropath)
     popup=False,
     tooltip="district",
     tiles="CartoDB positron", # use "CartoDB positron" tiles
     cmap="tab20b", # use "tab20b" matplotlib colormap
     style_kwds=dict(color="black") # use black outline
    )
district_map


# Custom pop-ups
# ---------------
# This example demonstrates how to use data from our dataframe to create custom interactions with our map using mouse-over and pop-up events. We create an HTML `div` element to hold the pop-up and to give it styles.
# 
# Our maps want to use hex colors, so the `dist_map` function uses a little
# translation function from `nycschools.ui` that takes a standard
# matplot lib color map and wraps it so that it returns hex colors.

# In[5]:


def school_pop(row):
    "Create a lighlty styled DIV to hold our pop-up data"
    html =  f"""
<div style="min-width: 200px">
dbn: {row.dbn}<br>
district: {row.district}<br>
name: {row.school_name}<br>
size: {row.total_enrollment}<br>
pct poverty: {row.poverty_pct:.1%}<br>
pct Asian: {row.asian_pct:.1%}<br>
pct Black: {row.black_pct:.1%}<br>
pct Hispanic: {row.hispanic_pct:.1%}<br>
pct White: {row.white_pct:.1%}
</div>"""
    return html


def dist_map(x):
    """A color map function that returns hex colors in 4 categories:
    0. district school (for districts 1-32)
    1. charter school
    2. dist 75 (SWD)
    3. other school types
    """
    cmap = ui.hexmap(plt.get_cmap("tab10"))
    if x < 33:
        return cmap(0)
    if x == 84: 
        return cmap(1)
    if x == 75: 
        return cmap(2)
    return cmap(3)


# Layering Folium maps
# ---------------------
# In the first example, we plotted schools on top of a district plot using `matplotlib`. We can use the same approach to make more complex, interactive Folium maps with the `explore()` function in our `GeoDataFrame`. In this example we merge the school geo dataframe with our demographic data, then get a reduced set of shared columns to plot in the map. When we call `explore()` we pass the `district_map` in as the `m` argument, making that the base map for our plot.

# In[6]:


# get the columns we need for our pop-up
cols = ["dbn", "school_name", "total_enrollment", "poverty_pct", "asian_pct", "black_pct", "hispanic_pct", "white_pct"]


school_geo = df.merge(demo[cols], on="dbn")

school_geo = school_geo[cols + ["district",  "geometry", "x", "y"]]

school_geo["district_color"] = school_geo.district.apply(dist_map)
school_geo["school info"] = school_geo.apply(school_pop, axis=1)


school_geo.explore(m=district_map, tooltip=False, popup="school info", color="district_color")

