#!/usr/bin/env python
# coding: utf-8

# Predictive Statistics
# =====================
# This notebook uses the `sklearn` library to run some machine learning
# predictions using regression analysis. It has examples of both
# Ordinary Least Square and Partial Least Square Regression.
# 
# We look at school demographics to see how well we can use those factors
# to predict mean_scale_score. We look at the grades 3-8 NYS math exams
# for the most recent academic year in our data set.
# 
# 

# In[1]:


import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import scale 
from sklearn.cross_decomposition import PLSRegression
from sklearn.feature_selection import chi2

import statsmodels.api as sm

import matplotlib.pyplot as plt
import seaborn as sns
import math

from IPython.display import Markdown as md

from nycschools import schools, ui, exams


# In[2]:


# load the demographic data and merge it with the math data
df = schools.load_school_demographics()

math_df = exams.load_math()

math_df = df.merge(math_df, how="inner", on=["dbn", "ay"])
math_df = math_df[math_df["mean_scale_score"].notnull()]
math_df.head()


# Predicting test scores
# -------------------------------
# Using OLS regression we will see how well we can predict mean_scale_score for the
# "All Students" category. We will run this with several variations of factors
# to see which factors have the strongest prediction.
# 
# The basic ideas of a predictive model is that we will use some of our data to
# "train" the model and use the other portion to "test" the model. Once we
# calculate a coeefficient for each factor, we can use those values to
# adjust the data sets mean score for a particular case.
# 
# These examples will use two statistical measures to compare our models:
# 
# - r-squared is a number between 0 and 1 that will tell us how closely our predictions
#   match the actual recorded score (1 is perfect, 0 is no matches)
# - mean squared error (`rmse`) tells us the mean distance between predictions and recorded scores
#   in the same scale as our exam; so an rmse of 10 means that, on average, our predictions were
#   10 points away from the actual score
# 
# 
# ### Correlation table
# First, let's see how the factors correlate with each other, and with our
# dependent variable. This table uses a "coolwarm" color map. Darker red
# indicates a strong positive correlation and darker blue a strong negative correlation.
# 

# In[3]:


# get just the 2019 test results for All Students
# this will be the dependent variable in our regression
data = math_df.query(f"ay == {math_df.ay.max()} and category == 'All Students'")
# calculate coefficients for these factors
factors = ['total_enrollment', 'asian_pct','black_pct', 
       'hispanic_pct',  'white_pct','swd_pct', 'ell_pct',  
       'poverty_pct', 'charter', "eni_pct", "geo_district"]


dv_stats = data.mean_scale_score.describe()
display(md("**Descriptive statistics for mean scale score**"))

display(pd.DataFrame(dv_stats))


# In[4]:


data = data[["mean_scale_score"] + factors]
data.charter = data.charter.apply(lambda x: 1 if x else 0)
corr = data.corr().sort_values(by="mean_scale_score")
corr = corr.style.background_gradient(cmap=plt.cm.coolwarm)
display(md("**Correlation table between factors and mean scale score**"))
display(corr)

display(md("**Scatter plots of correlations showing covariance of factors**"))

sns.pairplot(data[factors])
plt.show()


# OLS Linear Regression with different factors
# ---------------------------------------------
# 
# We're going to run a linear regression prediction with several different sets of factors to
# see which combination creates the strongest predictive model.
# 
# Because the training and testing sets are randomized we will get slightly different results
# each time we run the code in this cell. It appears that the factors that total enrollment has
# no predictive power and that including poverty_pct without eni_pct produces slightly
# better predictions.

# In[5]:


model = LinearRegression()

# shuffle our data frame so test, train are randomized, but the same across runs
data = data.sample(frac=1).reset_index(drop=True)

# make a small function so that we can report r2 and mse for different factors

def show_predict(factors, title):
    X = data[factors]
    y = data['mean_scale_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, train_size=0.3)

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    report = f"""
**{title}**

- factors: {factors}
- r2: {r2}
- rmse: {rmse}
"""
    display(md(report))

factors = ['total_enrollment', 'asian_pct','black_pct', 
           'hispanic_pct',  'white_pct','swd_pct', 'ell_pct',
           'poverty_pct', 'charter']
show_predict(factors, "With total enrollment")

factors = ['asian_pct','black_pct', 
       'hispanic_pct',  'white_pct','swd_pct', 'ell_pct',  'poverty_pct', 'charter']
show_predict(factors, "Without total enrollment")

factors = ['asian_pct','black_pct', 
       'hispanic_pct',  'white_pct','swd_pct', 'ell_pct',  'poverty_pct', 'eni_pct', 'charter']
show_predict(factors, "Adding ENI" )


factors = ['asian_pct','black_pct', 
       'hispanic_pct',  'white_pct','swd_pct', 'ell_pct', 'eni_pct', 'charter']
show_predict(factors, "ENI without Poverty %" )


# Partial Least Squares
# ===================

# In[6]:


factors = ['total_enrollment', 'asian_pct','black_pct', 
           'hispanic_pct',  'white_pct','swd_pct', 'ell_pct',
           'poverty_pct', 'charter']

X = data[factors]
y = data['mean_scale_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size=0.3)

pls = PLSRegression(n_components=len(factors))
pls.fit(X_train, y_train)


predictions = pls.predict(X_test)
r2 = r2_score(y_test, predictions)
rmse = mean_squared_error(y_test, predictions, squared=False)
md(f"""
**PLS predict**

- factors: {factors}
- r2: {r2}
- rmse: {rmse}
""")


# In[7]:


# fit both models with the full data and show the correlations
ols_fit = model.fit(X, y)
pls_fit = pls.fit(X, y)

coef_table = pd.DataFrame(columns=["factor", "pls-coef", "ols-coef"])

coef_table.factor = factors

coef_table["pls-coef"] = [x[0] for x in pls.coef_]
coef_table["ols-coef"] = [x for x in model.coef_]

# coef_table.join(ols_df, on="factor")
coef_table


# In[8]:


# compare sklearn and statsmodel OLS
y = data['mean_scale_score']

X = data[factors]
X = sm.add_constant(X)
sm_ols = sm.OLS(y, X).fit()

params = list(sm_ols.params.index.values[1:])
coefs = list(sm_ols.params.values[1:],)
pvalues = list(sm_ols.pvalues[1:])
len(params), len(coefs), len(pvalues)
pvalues
ols_df = pd.DataFrame({"factor":params,"sm-coef":coefs,"p-values":pvalues})
# ols_df
coef_table.merge(ols_df,on="factor", how="inner")


# In[9]:


# let's get p-values for the sklearn models
pls_intercept = y_intercept = pls_fit._y_mean - np.dot(pls_fit._x_mean , pls_fit.coef_)
pls_intercept = pls_intercept[0]
pls_intercept
pls_coef = [x[0] for x in pls.coef_]
X = data[factors]
y = data['mean_scale_score']
n = len(data)


beta_hat = [pls_intercept] + pls_coef
beta_hat


from scipy.stats import t
X1 = np.column_stack((np.ones(n), X))
# standard deviation of the noise.
sigma_hat = np.sqrt(np.sum(np.square(y - X1@beta_hat)) / (n - X1.shape[1]))
# estimate the covariance matrix for beta 
beta_cov = np.linalg.inv(X1.T@X1)
# the t-test statistic for each variable from the formula from above figure
t_vals = beta_hat / (sigma_hat * np.sqrt(np.diagonal(beta_cov)))
# compute 2-sided p-values.
p_vals = t.sf(np.abs(t_vals), n-X1.shape[1])*2 
t_vals
# array([ 0.37424023, -2.36373529,  3.57930174])
p_vals



# In[10]:


display(md("### Graph of PLS coefficients"))
coefs = [x[0] for x in pls.coef_]
ui.network_map("mean_scale_score", factors, coefs , None)

display(md("### Graph of OLS coefficients"))
coefs = [x for x in model.coef_]
ui.network_map("mean_scale_score", factors, coefs , None)

