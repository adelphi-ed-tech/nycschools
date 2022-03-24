New York Schools Open Data Portal
=================================

New York City Open Data Law: [read the law](https://www1.nyc.gov/site/doitt/initiatives/open-data-law.page)

> The council hereby finds and declares that it is in the best interest of New
> York city that its agencies and departments make their data available online
> using open standards. Making city data available online using open standards
> will make the operation of city government more transparent, effective and
> accountable to the public. It will streamline intra-governmental and
> inter-governmental communication and interoperability, permit the public to
> assist in identifying efficient solutions for government, promote innovative
> strategies for social progress, and create economic opportunities.


Open data sets:
---------------
- **NYC Open Data Portal** [Education Category](https://data.cityofnewyork.us/browse?category=Education)
  - [2020-2021 School Demographic Snapshot](https://data.cityofnewyork.us/Education/2020-2021-Demographic-Snapshot-School/vmmu-wj3w)
  - [2021 High School Directory](https://data.cityofnewyork.us/Education/2021-DOE-High-School-Directory/8b6c-7uty)
  - [2021 High School Admissions Selection Criteria](https://data.cityofnewyork.us/Education/Selection-Criteria-for-Fall-2021-High-School-Admis/9gs9-zhxw)
  - [2013-2019 Math Test Results Schools](https://data.cityofnewyork.us/Education/2013-2019-Math-Test-Results-School-SWD-Ethnicity-G/74ah-8ukf)
  - [2013-2019 ELA Test Results Schools](https://data.cityofnewyork.us/Education/2013-2019-English-Language-Arts-ELA-Test-Results-S/gu76-8i7h)
  - [2013-2019 Math Test Results Charter Schools](https://data.cityofnewyork.us/Education/2013-2019-Math-Test-Results-Charter-School/3xsw-bpuy)
  - [2013-2019 ELA Test Results Charter Schools](https://data.cityofnewyork.us/Education/2013-2019-English-Language-Arts-ELA-Test-Results-C/sgjd-xi99)
- **NYSED Data** [Downloads](https://data.nysed.gov/downloads.php)
  - [3-8 Assessment Data](https://data.nysed.gov/files/assessment/20-21/3-8-2020-21.zip)
  - [School Demographics & Enrollment](https://data.nysed.gov/files/enrollment/20-21/enrollment_2021.zip)

Notebook files
--------------
These Jupyter Notebooks demonstrate core `pandas` and data analysis
approaches, and model some possible uses for the key school data
that's released as part of the New York City Open Data Portal.

Here's a brief list of the notebooks and main ideas in each:

1. [pandas-basics](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/panda-basics.ipynb):
   - creating `DataFrames` from an API
   - working with `Series` (columns)
   - running aggregate functions
   - data dictionary of the school demographics data set
2. [clean-query](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/clean-query.ipynb)
   - selecting rows from a `DataFrame`
   - creating new `Series` based on calculations
   - pandas `apply()` function
   - python `lambda` functions
   - sorting data
3. [math-ela-merge](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/math-ela-merge.ipynb)
   - (more) cleaning data
   - renaming columns
   - combinging `DataFrames` by joining them with `merge()`
   - dropping columns with `del`
4. [correlations](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/correlations.ipynb)
   - Pearson correlation with `numpy`, `scipy`, and `pingouin`
   - **concatenating** multiple `DataFrames` into a single data set for
     reporting and analysis
   - calculating p-values, power, and confidence intervals
   - running analysis of covariance (ancova)
5. [load-excel-test-data](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/load-excel-test-data.ipynb)
   - reading Excel workbooks with `pandas`
   - reading sheets from Excel into `DataFrames`
   - concatenating `DataFrames`
   - importing custom Python modules that we write into Jupyter
   - using the custom `schools.py` module
6. [ela-pivot](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/ela-pivot.ipynb)
   - convert "long" data to "wide" data
   - use `pandas` `pivot()` function
   - load our custom data saved as .csv from the file system (to avoid long-running code)
 7. [school-demographics](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/school-demographics.ipynb)
    - loading .py files with autoreload
    - schools.py updates
    - ui.py utility package
    - aggregate functions
      - appending a row of totals/sub-totals
    - data dictionary example (reading from csv)
    - formatting output of dataframes
      - using `display()`
      - mixing markdown and code by importing `Markdown`
      - using f-strings with format strings for numbers (rounding floats, commas for large numbers, as percentages)
    - complex `apply()` functions that track changes across rows
 8. [anova](https://github.com/adelphi-ed-tech/school-data-portal/blob/main/nb/anova.ipynb)
    - t-test
    - anova
    - OLS regression
    - categorical data (dummies)
    - aggregates for mean and standard deviation
    - reporting results in markdown
