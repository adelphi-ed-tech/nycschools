#!/usr/bin/env python
# coding: utf-8

# Calculating New Columns
# =======================
# 
# `pandas` makes it easy to calculate new fields based on
# existing data. This Notebook looks at the _easy_ cases
# and then takes on some more advanced cases using our 
# schooldemographcs data set.
# 
# Topics in this notebook:
# 
# - calculating columns with _vectorization_
# - calculating columns with `apply()` on a series
# - lambda functions
# - use `copy()` to make a (shallow) copy of a data frame

# In[1]:


from nycschools import schools

df = schools.load_school_demographics()


# In[2]:


# with "vectorization"
# ---------------------

# calculate a new fields for the pct of school that is black or hispanic
df["black_hispanic_n"] = df.black_n + df.hispanic_n

# now calculate that as a pct of the total enrollment
df["black_hispanic_pct"] = df.black_hispanic_n / df.total_enrollment

df[ ["dbn","school_name","total_enrollment", "black_hispanic_n", "black_hispanic_pct"] ]


# In[3]:


# we can also use boolean expressions -- let's mark all of the schools not in districts 1-32 as "special_district"
df["special_district"] = df.district > 32
df[["dbn", "district", "special_district"]]


# In[4]:


# vectorization is the best way to create cols based on calculations but can't handle more advanced logic
# here we use apply() to format total enrollment to make it easier to read
# we'll call the new field total_enrollment_pp -- pp: pretty print

# create a function that we will "apply" to that columns
def fmt_enroll(n):
    return f"{n:,}"

df["total_enrollment_pp"] = df.total_enrollment.apply(fmt_enroll)
big_schools = df.sort_values(by="total_enrollment", ascending=False)[0:20]
big_schools[["dbn","total_enrollment", "total_enrollment_pp"]].head()
    


# In[5]:


# since our function is so simple, it's a good candidate for a lambda function
# lambdas in python are anonymous functions that have a reduced syntax
# see examples here:
# https://www.freecodecamp.org/news/python-lambda-function-explained/

# make a copy of our data
data = df.copy()

# use lambda to format the percentages
# we use the f-string syntax to round the number to a 2 decimal float
data["black_pct_pp"] = data.black_pct.apply(lambda x: f"{x*100:.02f}%")
data["black_pct_pp"]


# In[6]:


# we can put the whole thing in a loop, too
# here we replace the original value with the formatted value
data = df.copy()
for c in data.columns:
    if c.endswith("_pct"):
        data[c] = data[c].apply(lambda x: f"{x*100:.02f}%")


data[["dbn", "asian_pct", "black_pct", "hispanic_pct", "white_pct"]].head()

