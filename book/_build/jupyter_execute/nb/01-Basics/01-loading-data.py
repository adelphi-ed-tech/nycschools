#!/usr/bin/env python
# coding: utf-8

# Loading Data
# ============
# [[colab](https://colab.research.google.com/github/adelphi-ed-tech/nycschools/blob/main/docs-source/nb/01-Basics/01-loading-data.ipynb)] [[github](https://github.com/adelphi-ed-tech/nycschools/blob/main/docs-source/nb/01-Basics/01-loading-data.ipynb)]
# 
# This notebook loads the NYC School Demographic data.
# Working with this dataset, we look at some basic
# [Pandas](https://pandas.pydata.org/) operations.
# 
# We assume that you have a basic understanding of Python and
# Jupyter notebooks. This is a good start if you are new to
# Pandas and data science in Python.
# 
# In particular:
# 
# - loading data from the `nycschools` into a `DataFrame`
# - use `head()`, `tail()`, and `Series` (columns) to understand the data
# - access column `Series` by name using index notation
# - use `unique()`, `min()`, `max()`, `sum()`, and `mean()` to understand series data
# 
# 

# In[2]:


# import schools from the nycschool package
from nycschools import schools
# load the demographic data into a `DataFrame` called df
df = schools.load_school_demographics()


# Displaying data tables
# -----------------------
# If we display `df` notebook shows us some of the data from 
# the start of the data set and some from the end.
# 
# If we call `df.head()` we get the start of the data. `df.tail()` shows us the end of the data.
# 
# Comment/uncomment the different options to see how they work.

# In[2]:


df

# df.head()
# df.tail()


# In[3]:


# The the `columns` property shows us the names of the cols in our `df`.
df.columns


# We can access just one column using index notation -- 
# `df["poverty"]` gives us just that column. We can then display or sort the data using either
# the python built-in function `sorted()` or the pandas `Series` function `sort_values()`.
# If we call `unique()` we will get a list of the unique values in the `Series`. In the case
# of `poverty` that lets us see that the column contains string data, and not raw numbers
# if the poverty level is too high or too low.

# In[4]:


# get just the poverty column
poverty = df["poverty_pct"]

# pandas also supports "dot notation" for access to columns
# but you can't use dot notation if the column name is not a valid identifier, python keyword, 
# or name of a property or member function of the dataframe

poverty = df.poverty_pct # same as line 2 above

poverty = poverty.sort_values()
print("Note: precentages are displayed as real numbers between 0..1")
print(poverty.unique()) 


# We can get a subset of the data by using index notation with
# a list of column names:
# 
# `df[ ["dbn", "school_name", "total_enrollment", "poverty_n" ] ]` returns a `DataFrame`
# with 4 columns.

# In[5]:


df[ ["dbn", "school_name", "total_enrollment", "poverty_n" ] ]

