Combining Data
==============
The examples in this section demonstrate ways to bring different data sets together. There are a few key concepts covered:

- **aggregating data:** we do this when we want to group rows together based on a shared value that we _group_ the data on. For example we might _group_ all of our schools by the borough and then _aggregate_ the `total_enrollment` with a `sum` function in order to find all of the students in each borough.
- **merge:** let's us take two data sets and combine them into one data set based on a shared key value or values. We will look at how we can merge the school demographics data with the test score data so that we can use demographics to gain insight into test results
- **concatenating:** allows us to either add new rows to an exsiting data set (assuming both sets have the same data) or add new columns to a data set, assuming that each row of the new columns relates to the same row in the existing data set. Concatenating is useful when we are gathering raw data into a common format or when we want to create our own tables for a better display.
