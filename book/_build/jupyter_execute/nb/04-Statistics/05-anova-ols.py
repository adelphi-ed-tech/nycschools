#!/usr/bin/env python
# coding: utf-8

# ANOVA and OLS Regression
# ========================
# This notebook combines school demographic data
# and New York State ELA test scores to examine
# the factors that predict test scores. In it we
# run a t-test to test for statistic difference
# in the scores for White students and Black students.
# 
# We then run analysis of variance between the 4
# main ethnic/racial groups to see if there is statistical
# significance in the outcomes. We run an OLS regression
# on these groups with the "All Students" as a baseline
# reference category and display the ANOVA table and regression summary.
# 
# Finally, one run a different OLS regression to examine
# the school demographic factors and their effect on test scores.
# 
# In this notebook:
# 
# - t-test (review)
# - ANOVA (analysis of variance)
# - OLS (ordinary least squares) regression

# In[32]:


# load the demographic data
import pandas as pd
import numpy as np
import scipy as scipy

import pingouin as pg

import statsmodels.api as sm

from IPython.display import Markdown as md

from nycschools import schools, exams


# In[19]:


# load the demographic data and merge it with the ELA data
df = schools.load_school_demographics()

# load the data from the csv file
ela = exams.load_ela()


#drop the rows with NaN (where the pop is too small to report)
ela = ela[ela["mean_scale_score"].notnull()]
df = df.merge(ela, how="inner", on=["dbn", "ay"])

# for this analysis we will only look at grade 8 scores for the 2018-19 (pre-covid) school year
# the last pre-covid year
df = df[df.grade =='8']
df = df[df.ay == 2018]
df = df[df.mean_scale_score.notnull()]

# create 5 groups as independent data frames

all_students = df[df["category"] == "All Students"][["dbn", "mean_scale_score"]]
black = df[df["category"] == "Black"][["dbn", "mean_scale_score"]]
white = df[df["category"] == "White"][["dbn", "mean_scale_score"]]
hispanic = df[df["category"] == "Hispanic"][["dbn", "mean_scale_score"]]
asian = df[df["category"] == "Asian"][["dbn", "mean_scale_score"]]



# t-test: white and black students
# --------------------------------
# Before running the ANOVA and further analysis, we will run a t-test between Black and White students to determine if there is a significant difference between their average test score.

# In[20]:


# calculate the mean test score and standard deviation for each group
mean_std = df.groupby('category').agg(Mean=('mean_scale_score', np.mean), STD=('mean_scale_score', np.std))
display(md("**Mean average and standard deviation of test scores for each group.**"))
display(mean_std)


# run a t-test to see if there is a statistical difference between white and black student scores
t = scipy.stats.ttest_ind(white["mean_scale_score"],black["mean_scale_score"])

display(md(f"""
**T-Test results** comparing school averages of 
White (`n={white["dbn"].count()}`) and Black (`n={black["dbn"].count()}`)
students in 8th grade student ELA scores for 2019-20 academic year.

- White students: M={white["mean_scale_score"].mean():.04f}, SD={white["mean_scale_score"].std():.04f}
- Black students: M={black["mean_scale_score"].mean()}, SD={black["mean_scale_score"].std():.04f}
- T-score: {round(t.statistic, 4)}, p-val: {round(t.pvalue, 4)}

`n` values report the number of schools observed, not the number of test takers. Further analysis
will report on the t-test for weighted means that account for school size.

We see that there is a statistically significance difference in test scores between the groups.
"""))


# ANOVA & f-values
# ----------------
# In the example below we calculate the f-statistic to see if there are significant differences in test scores based on racial/ethnic group of the test takers. We compare the four main groups in NYC Schools: Asian, Black, Hispanic, and White.

# In[22]:


# run a one way anova to test if there is significant difference between the
# average test scores at the school level of 4 different racial/ethnic groups

fvalue, pvalue = scipy.stats.f_oneway(
    asian["mean_scale_score"], 
    black["mean_scale_score"],
    hispanic["mean_scale_score"],
    white["mean_scale_score"])


results = f"""
A **one-way between subjects ANOVA** was conducted to compare the effect of 
racial/ethnic group on the test score for 8th grade NYS ELA exams for
during the 2018-2019 academic year.

The four groups in the test are: Asian (n={len(asian)}), Black (n={len(black)}), Latinx (n={len(hispanic)}),
and White (n={len(white)}) students.

The was a significant effect of racial/ethnic group on test score at
the p<.001 level for the four conditions, [p={pvalue:.04f}, F={fvalue:.04f}].

_`n` values are the number of schools reported, not the number of test takers in each group_
"""
md(results)


# ### Pingouin results
# When we ran the t-test we saw that `pingouin` offers some useful additional features.
# The API (syntax for using) `pingouin` differes from `scipy`. Before we run the test, we
# create a new single dataframe with just the columns we care about. We tell the function which column
# is the dependent variable and which specifies the groups.
# 
# Below we show the [pinguion ANOVA](https://pingouin-stats.org/generated/pingouin.anova.html#pingouin.anova).

# In[25]:


# pg.anova()
data = df.copy()
data = data[data.category.isin(["Asian", "Black", "Hispanic", "White"])]
data[["category", "mean_scale_score"]]

pg.anova(dv='mean_scale_score', between='category', data=data, detailed=True)


# OLS Linear Regression
# ---------------------
# The ANOVA tells us that there is a significant difference in test result based on racial/ethnic group. We can run a regression analysis to help us isolate the impact of different factors on our `mean_scale_score` -- our dependent variable.
# 
# For this analysis we will look at the school demographics to analyze the mean ELA test score for All Students at the school.

# In[46]:


# first choose the "factors" from our data fields that we believe impact mean_scale_score
data = df.copy()
data = data[data.category == "All Students"]
factors = [
       'total_enrollment',
       'female_pct', 
       'asian_pct',  
       'black_pct',
       'hispanic_pct',  
       'white_pct',
       'swd_pct',  
       'ell_pct',  
       'poverty_pct',
       'eni_pct',
       'charter']

y = data['mean_scale_score']
X = data[factors]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

model.summary()


# In[48]:


# we can also pull specific data from the model
# here we create our own table with the factors, coefficients and p-values
params = list(model.params.index.values[1:])
coefs = list(model.params.values[1:],)
pvalues = list(model.pvalues[1:])

table = pd.DataFrame({"factor":params,"coef":coefs,"p-values":pvalues})
table.sort_values(by="coef")

