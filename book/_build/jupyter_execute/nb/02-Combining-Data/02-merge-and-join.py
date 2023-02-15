#!/usr/bin/env python
# coding: utf-8

# Merges & Joins
# ==============
# Here, finally, we combine data sets together. I say finally because this is one of the _first_ things you will do when working with real world data. `nycschools` has already combined multiple data sets into its core DataFrames, but you will want to combine this data in new ways, make new DataFrames from your results, and pull in new data from the outside world.

# In[21]:


import pandas as pd
from nycschools import schools, exams

# school demographics in one frame
demo = schools.load_school_demographics()

# exam results in another frame
ela = exams.load_ela()
math = exams.load_math()


# Merging Data
# ----------------------
# When two data sets have a shared key then combining them into a single dataframe is straightforward. Here we use the `merge()` function in `DataFrame` to combine the school demographcs and ela test results into a single data frame. We merge them "on" the `dbn` and `ay` columns because these cols represent a unique identifier for each row in both data sets. _Note_ that the result has only the intersecton of both datasets. If our demographic data has a DBN that's not in the test data set, that school's data will be dropped from the results.

# In[18]:


demo.merge(ela, on=["dbn", "ay"]).head()


# Astute readers will see a new column called `school_name_x` in our results. You can't see it in the truncated data above, but there is also a `school_name_y`. Both data sets had a `school_name` column, so `pandas` suffixed the one from `demo` with `x` and the one from `ela` with `y`.
# 
# Because both columns _should_ contain the same data (because they have the save DBN for the same school year), in this case we can just drop one of the columns before the merge. We'll drop `school_name` from `ela` because the demographics data set should have our canoninical school names.

# In[19]:


ela2 = ela.drop(columns="school_name")
demo.merge(ela2, on=["dbn", "ay"]).head()


# Merge with suffixes: wide data
# --------------------------------------------
# When we have a data set where we use columns to represent different categories of data, we can call this "wide data." In this example, we're going to make a test results data frame that has math and ela test scores in the same row.
# 
# At the start of this notebook we loaded both the math and ela exam data. Note that they have exactly the same columns. When we _merge_ them, we're going to **suffix** the ela data with `_ela` and the math data with `_math`. We will drop `school_name` from one of the data sets and use `["dbn", "ay", "test_year", "grade", "category"]` to join the two.
# 

# In[32]:


ela2 = ela.drop(columns="school_name")
wide = ela2.merge(math, on=["dbn", "ay", "test_year", "grade", "category"], suffixes=["_ela", "_math"])
wide.head()


# Now that we have the wide data, we can easily compare math and ela results for the same set school/year/grade/category. Below we will calculate a new column called `test_delta` that shows the difference between math and ela results for the same cohort of students in the same school. This will let us see, for example, which if any schools are "unbalanced" in math and ELA. Later, we might correlate this to other demographic data such as high percentages of ELL or SWD students.

# In[37]:


wide["test_delta"] = wide.mean_scale_score_math - wide.mean_scale_score_ela
wide["test_delta_abs"] = abs(wide.mean_scale_score_math - wide.mean_scale_score_ela)

wide = wide.sort_values(by="test_delta_abs", ascending=False)

wide[["dbn","grade","ay","category","mean_scale_score_math", "mean_scale_score_ela", "test_delta"]].head()


# Concatenate DataFrames: long data
# ---------------------------------------------------
# If we have two DataFrames with the same columns (like our math and ela results) we can concatenate the data from one df onto the other to create a longer dataframe. Generally, this is a more flexible format for analysis than the wide data format. In our math/ela example, it allows us to, for example, easily average the math and ela test scores together (filtering for group, year, etc).
# 
# In the example here we will add a new column, `test`, which will have the value of "ela" or "math". This column will let us know whether that row reports a math test or ela test result.

# In[40]:


math["test"] = "math"
ela["test"] = "ela"
long = pd.concat([math, ela])
long

