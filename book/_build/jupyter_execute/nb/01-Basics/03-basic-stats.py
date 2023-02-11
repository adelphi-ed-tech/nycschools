#!/usr/bin/env python
# coding: utf-8

# Basic Statistics
# ================
# 
# This Notebook shows us how to use the `pandas` to find
# basic quantitative descriptions of our data
# 
# Topics in this Notebook:
# 
# - dropping columns
# - minimum and maximum ranges
# - averages
# - counts
# - sorting data
# - correlations with `corr()`
# - `describe()`

# In[1]:


# import schools from the nycschool package
from nycschools import schools

# load the demographic data into a `DataFrame` called df
df = schools.load_school_demographics()

# let's just use one year of data
df = df[df.ay == 2020]

# use a subset of columns for this notebook
cols = [
    'dbn',
    'district',
    'boro',
    'school_name',
    'total_enrollment',
    'asian_pct',
    'black_pct',
    'hispanic_pct',
    'white_pct',
    'swd_pct',
    'ell_pct',
    'poverty_pct'
]
df = df[cols]


df.head()


# In[2]:


# sort the data and show just the 10 largest schools
# sort in descending order (biggest --> smallest)
data = df.sort_values(by="total_enrollment", ascending=False)

# show the first 10 rows
data[:10]


# In[3]:


# get just the total_enrollment column, called a Series in pandas
enrollment = df["total_enrollment"]
print("The largest school:", enrollment.max())
print("The smallest school:", enrollment.min())

print("Avg (mean) school size:", enrollment.mean())
print("Avg (median) school size:", enrollment.median())
print("Avg (mode, can return multiple values) school size:", list(enrollment.mode()))


# In[4]:


# the built in describe() function calculates several descriptive statististics for each column
# in the data frame and returns them as a new dataframe
df.describe()


# In[5]:


# we can also call describe aon a single series:
df.swd_pct.describe()


# In[6]:


# we can also call the corr() method to show correclations between columns
# we will take out "district" from this data because the district number
# is categorical -- not the measure of a value

# correlations close to 1 or negative one show high correlations
# closer to zero items are not closely correlated
data = df.drop(columns=["district"])
data.corr()


# In[7]:


# last, we can use styles to make the correlation table easier to read
# note: you need to run this cell to see the colors -- it's get saved without the styled output
corr = data.corr()
# a coolwarm color map will show values in a gradient where -1 is the deepest blue and 1 is deepest red
corr.style.background_gradient(cmap='coolwarm')

