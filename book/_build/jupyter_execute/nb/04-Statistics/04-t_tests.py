#!/usr/bin/env python
# coding: utf-8

# T Tests
# =======

# In[1]:


import scipy
from IPython.display import Markdown as md

from nycschools import schools, exams


# In[4]:


demo = schools.load_school_demographics()
df = exams.load_math_ela_long()
df = df[df["mean_scale_score"].notnull()]
df = df.merge(demo, how="inner", on=["dbn", "ay"])

df.head()


# In[5]:


# let's look at charter schools vs non-charter schools 
df["charter"] = df.district == 84
# get the schools in the range of 1-32 and district 84 (excludes other special districts)
data = df[df.district.isin(list(range(1,33)) + [84])]

# just get all students
data = data[data.category=="All Students"]

# remove null data
data = data[data["mean_scale_score"].notnull()]

# show the correlation between chater and test score
data = df[["mean_scale_score", "charter"]]
data.corr()


# In[10]:


# split the data into two groups for the t test
charter = data[data.charter == True]
community = data[data.charter == False]
# run a t-test to see if there is a statistical difference between charter and non-charter test results
t = scipy.stats.ttest_ind(charter.mean_scale_score, community.mean_scale_score)

# the scipy results include the t-value and the p-value
# t is the score of the test, and p is the probability that the difference is the result of chance
t


# In[20]:


# when reporting the results we care about these variables too

# population size
n_charter = len(charter)
n_community = len(community)

# mean average
M_charter = charter.mean_scale_score.mean()
M_community = community.mean_scale_score.mean()

# standard deviation 
sd_charter = charter.mean_scale_score.std()
sd_community = community.mean_scale_score.std()


display(md(f"""
**T-Test results** comparing school averages of 
Charter School Test Results (`n={n_charter}`) and Community School Test Results (`n={n_community}`)
students in 3-8th grade student ELA and Math scores.

- Charter test results: M={M_charter:.02f}, SD={sd_charter:.02f}
- Community test results: M={M_community:.02f}, SD={sd_community:.02f}
- T-score: {t.statistic:.04f}, p-val: {t.pvalue:.04f}

`n` values report the number of school average test results observed, not the number of test takers. 
"""))


# `pingouin` stats wrapper
# ------------------------
# The [`pingouin` library](https://pingouin-stats.org/index.html) has a number of functions that "wrap" standard python stats functions to include additional information and nicer formatting out of the box. `ttest` is one of these functions. We can see in the output below that we get the t value, p value (like `scipy.stats`), but we also get degrees of freedom, confidence intervals, and more, without having to calculate these independently for each test.

# In[27]:


import pingouin as pg
pg.ttest(charter.mean_scale_score, community.mean_scale_score, correction=False)

