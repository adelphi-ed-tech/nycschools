New York Schools Open Data Project
==================================

The mission of the NYC Schools Open Data Project is to make open data regarding public schools in New York available to everyone interested in improving our schools, regardless of their technical background or familiarity with data analysis. We believe that fighting for educational equity requires us to broaden the audience of who can use and analyze data. Accordingly, we want to make educational data more accessible, train people to use it, and demystify and remove the barriers to access.

Our goal is to build platform where any motivated individual or groups can evaluate available school data, interpret it to help understand issues they care about, and employ data as part of larger arguments in our conversations about schools in New York.


Open data sets currently available:
-----------------------------------
Our goal is to maintain the most current as well as historical record for each of these data sets.

1. [School Demographic Snapshot](https://data.cityofnewyork.us/Education/2020-2021-Demographic-Snapshot-School/vmmu-wj3w)
2. [NYC English Language Arts (ELA) State Test Results (non-charter)](https://data.cityofnewyork.us/Education/2013-2019-New-York-State-ELA-Exam/hvdr-xc2s)
3. [NYC Math State Test Results (non-charter)](https://data.cityofnewyork.us/Education/2013-2019-New-York-State-MATH-Exam/365g-7jtb)
4. [NYSED 3-8 ELA & Math Assessment Data (statewide, only source for charter schools with demographic categories)](https://data.nysed.gov/downloads.php)
5. [Charter School English Language Arts (ELA) Test Results](https://data.cityofnewyork.us/Education/2013-2019-English-Language-Arts-ELA-Test-Results-C/sgjd-xi99)
6. [Charter School Math Test Results](https://data.cityofnewyork.us/Education/2013-2019-Math-Test-Results-Charter-School/3xsw-bpuy)
7. [Regents Exam Results](https://data.cityofnewyork.us/Education/2014-15-2018-19-NYC-Regents-Exam-Public/2h3w-9uj9)
8. [School Point Locations](https://data.cityofnewyork.us/Education/2019-2020-School-Point-Locations/a3nt-yts4)
9. [School Locations](https://data.cityofnewyork.us/Education/2019-2020-School-Locations/wg9x-4ke6)
10. [GIS data: Boundaries of School Districts](https://data.cityofnewyork.us/Education/School-Districts/r8nu-ymqj)

- _not yet integrated into API or unit tests_
  - [High School Directory](https://data.cityofnewyork.us/Education/2021-DOE-High-School-Directory/8b6c-7uty)
    - [High School Admissions Selection Criteria](https://data.cityofnewyork.us/Education/Selection-Criteria-for-Fall-2021-High-School-Admis/9gs9-zhxw)
    - [NYSED School Demographics & Enrollment](https://data.nysed.gov/files/enrollment/20-21/enrollment_2021.zip)

Notebook example files
----------------------
In addition to the core python library, the project includes a set of Jupyter
Notebooks that demonstrate key `pandas` and data analysis approaches, and model
some possible uses for the key school data that's released as part of the New
York City Open Data Portal.

Here's a brief list of topics covered:

1. Pandas Basics
2. Merging and Aggregating Data
   - group by and aggregates (count, sum, avg, etc)
   - loading data not included in `nycschools`
   - combining data sets (merge/join)
   - concatenating data sets
   - pivots / reshaping data
   - wide and long data formats
3. Statistical Analysis
   - R coefficients
   - quantiles
   - z-scores
   - T Tests
   - Anova / F Tests
   - Ordinary Least Square (OLS) regressions
   - Partial Least Square (PLS) regressions
   - predictive statistics (r-squared, mean squared error)
4. Graphs and Charts
   - tables
   - bar charts
   - stacked bar charts
   - line graphs
   - scatter plots
   - color maps
   - network graphs
5. Maps and GIS data
   - Choropleth Maps (colored regions based on data)
   - map overlays with multiple data sets
   - interactive maps
