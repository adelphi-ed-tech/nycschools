#!/usr/bin/env python
# coding: utf-8

# Querying & Selecting
# ====================
# 
# In this Notebook we go over some of the ways of querying data in a dataframe.
# 
# - `[]` slice notation for subsets of data
# - `query()` method of `DataFrame` to search data
# - using `isin()`, `isnull()`
# - drop_duplicates()
# 

# In[1]:


# import schools from the nycschool package
from nycschools import schools, exams

# load the demographic data into a `DataFrame` called df
df = schools.load_school_demographics()


# In[2]:


# we already saw how to get a subset of columns
# let's get just these columns from out data
cols = ["dbn", "ay", "school_name", "district", "poverty_pct", "ell_pct", "swd_pct"]
df = df[cols]
df


# Selecting just one year
# ---------------------------------
# We can see that our data contains multiple years of data for each school.
# We can filter or query the data to just get a single year.
# 
# To do this, we will use the slice notation similary to above, however,
# instead of a list of columns, we have a Boolean expression using
# one of the columns in our data set.
# 
# `df[df.ay == 2020]` returns only the rows where `ay` equals `2020`
# 

# In[3]:


ay_2020 = df[df.ay == 2020]
ay_2020.head()


# Compound expressions
# ----------------------------------
# We can use Boolean operators to make more complex queries. 
# `pandas` uses the `&` operator for Boolean **and**
# and the `|` operator for Boolean **or**. Note that you should wrap
# your equality expressions inside of parenethesis.
# 
# To write bug-free code, we do not recommend mixing `and` and `or`
# clauses in the same query.
# 
# Below are two examples:
# 
# - `df[(df.district == 13) & (df.ay == 2020)]`
#    find data forschools in district 13 _and_ academic year 2020-21
# - `df[(df.poverty_pct > .9) | (df.ell_pct >= .4)]`
#    find school data where the school's poverty percent is greater than 90% _or_
#    the percent of studnts classified as English Language Learners is greater
#    than or equal to 40%
# 

# In[4]:


df[(df.district == 13) & (df.ay == 2020)].head()


# In[5]:


df[(df.poverty_pct > .9) | (df.ell_pct >= .4)].head()


# In[6]:


# this works, but it is confusing and error prone
df[(df.ay == 2020)  & ((df.poverty_pct > .9) | (df.ell_pct >= .4))].head()


# In[7]:


# rather than mixing | and &, we can write our code more clearly in two lines
data = df[df.ay == 2020]
data = data[(data.poverty_pct > .9) | (data.ell_pct >= .4)]
data.head()


# Finding a subset of data
# -----------------------------------
# `DataFrame` has a usefule function called `isin()` that lets us filter data on a `Series`
# if the value is in a set of values. First, we'll do a simple example where we find
# all of the schools in a district `[3,8,15]`

# In[8]:


districts = [3, 8, 5]
data = df[df.district.isin(districts)]
data[["dbn", "district", "school_name"]]


# Using `drop_duplicates`
# -----------------------------------------------------
# In the display of the table above, since we chose not to show all of the columns, we have repeated columns. Sometimes we will want just the unique results. We saw that `unique()` works for a `Series`. It doesn't work for a dataframe, however.
# 
# Luckily, we have `drop_duplicates()` which serves a similar function...see:
# 

# In[9]:


data[["dbn", "district", "school_name"]].drop_duplicates()


# Filtering missing data
# -------------------------------
# You will not always have complete data, and sometimes you need to find rows with missing records. You may want to update them with some default or derived values, or, you may simpley want to exclude them from your data.
# 
# In this example, we will use `nycschools` to load the grade 3-8 ELA NYS exams. We will then filter out all of the rows that don't have a score. Some rows are null because not enough students took the exam. Others may be missing data because their students were exempt from the exam or other reasons.

# In[10]:


from nycschools import exams
ela = exams.load_ela()
print(f"There are {len(ela):,} total records in ela")
ela.head()


# In[11]:


missing = ela[ela.mean_scale_score.isnull()]
print(f"There are {len(missing):,} records in ela with null values for mean_scale_score. NaN means 'Not a Number'")

missing

