#!/usr/bin/env python
# coding: utf-8

# Groups & Aggregates
# ===================
# 
# In this notebook we look at how to change the level that we use to analyze data by **grouping** multiple
# rows into a single row. This `groupby` function allows us to look at the school data by district,
# borough, or academic year. To group data, you specifiy the column name or column names for the group. All unique names or combinations will become a single row.
# 
# The _other_ rows of data need to be **aggregated** in some way. Common aggregate functions include `sum` (e.g. find the total enrolled students in Brooklyn), `count` (find unique schools in Queens), and `mean` (find the average percent poverty of students in the Bronx).

# In[1]:


from nycschools import schools

df = schools.load_school_demographics()


# Total Enrollment by Boro
# ------------------------------------
# For this example, we create a simplified data set that only has 2 columns:
# `boro` and `total_enrollment`. We also limit it to only the 2020 academic year.
# 
# We call the `groupby()` function of `DataFrame`and pass in "boro" as the column name for the group.
# From there, we call `.sum()` on the resulting GroupBy object. This will sum up the enrollment in each school,
# in each borough.
# 

# In[2]:


boros = df[df.ay == 2020]
boros = boros[["boro", "total_enrollment"]]

boros.groupby("boro").sum()


# We see in th results that Brooklyn had the most students enrolled in 2020 (n=346802) and Staten Island
# had the fewest (n=63824).
# 
# We also notice that `total_enrolmment` doesn't appear on the same level as `boro`. If we want to be able to treat `total_enrollment` as a "normal" column, we need to call `reset_index()` after our aggregate function.
# 
# Like this:

# In[3]:


boros.groupby("boro").sum().reset_index()


# Using a `dict` of aggregate columns
# ----------------------------------------------------
# Now, we might have a few more questions about this simple measure of school enrollment. For example, what was the average enrollment, and how many different schools are in each borough?
# 
# We can answer these questions by running by adding more columns (namely `dbn`) to our data and using different aggregate functions. In this case we will use `sum`, `count`, `mean`, `min`, and `max`.
# 
# To accomplish this, we call the `agg` function on the results of the groupby and pass in a dictionary
# where the column names are keys, and the aggregate function(s) are the values. If we want only a single agg 
# function, we can use that as the value, but if we want multiple functions, we can set a list of strings
# as the value.

# In[4]:


boros = df[df.ay == 2020]
boros = boros[["boro", "dbn", "total_enrollment"]]
boros = boros.groupby("boro").agg({
    "dbn":"count", 
    "total_enrollment":["sum", "mean", "min", "max"]})
boros


# Resetting the index
# ----------------------------
# In the results above, we say that the aggregate columns do not appear in the same row as the grouped column, boro. Also, there are 2 levels to the aggregate index because we have 4 columns for total_enrollment. Sometimes we want to convert these columnbs back into a flat index. This makes it easier to filter, merge, and sort the data and to access specific Series in the DataFrame. Unfortunately, we can't simply call `reset_index()` like we did above.
# 
# Here after we reset the index, we rename all of the columns with a new list of strings. The length of the new list musth match the number of columns.

# In[5]:


boros = df[df.ay == 2020]
boros = boros[["boro", "dbn", "total_enrollment"]]
table = boros.groupby(by="boro").agg({
    "dbn":"count", 
    "total_enrollment":["sum", "mean", "min", "max"]}).reset_index()

cols = ["Borough", "Num. Schools", "Total Students", "Avg School Size", "Smallest School", "Largest School"]
table.columns = cols
table


# Grouping by Multiple Columns
# --------------------------------------------
# Sometimes we might want to pass in more than one column as the group by index. In this example we will group our data by borough and whether they are a charter school or not.
# 
# Note a couple of things in this short example:
# 
# 1. We call `copy()` on `df` because we are adding a new column and don't want to mess with the original data frame
# 2. We use a lambda function in apply, and we use a special type of if/else statement usually called a "ternary" operation
# 3. Because we're doing several agg functions, we will create them as a dict _before_ we call `agg()`. This is just to make our code easier to read and maintain
# 
# 

# In[19]:


# because we're adding data to our subset, we're going to call copy()
data = df[df.ay == 2020].copy()
data["school type"] = data.district.apply(lambda x: "charter" if x == 84 else "public")
data = data[["boro","school type","dbn","asian_pct","black_pct","hispanic_pct","white_pct"]]
aggs = {
    "dbn": "count",
    "asian_pct": "mean",
    "black_pct": "mean",
    "hispanic_pct": "mean",
    "white_pct": "mean"
}


data.groupby(["boro", "school type"]).agg(aggs).reset_index()

