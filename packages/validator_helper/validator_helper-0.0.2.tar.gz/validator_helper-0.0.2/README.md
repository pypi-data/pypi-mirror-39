# Validator Helper

[![Build status](https://travis-ci.org/lowandrew/Validator_Helper.svg?master)](https://travis-ci.org/lowandrew)
[![PyPI version](https://badge.fury.io/py/validator_helper.svg)](https://badge.fury.io/py/validator_helper)

Use this package to help validate that CSVs outputted by your pipelines match up with what you think they should.

### Installation

To install, use pip/pip3:

```
pip install validator_helper
```

### Usage

Here's how to use this. Assume we have a list of people, their ages, and their favourite colors in CSV format.
The reference data set looks like this:

```
Name,Age,Color
A,22,Red
B,44,Green
```

You have some sort of pipeline that computes these things and writes the output to another CSV file, and you'd like to make sure that it's giving
you the right outputs. Here's the code that lets you do that.


```python
from validator_helper import validate

# First, create a list of Column objects that you care about that are in both your reference
# and test CSV files.

# These objects need to be initialized with the column name (as it appears in both CSVs).

# If the column is categorical, all you have to do is the following:
column_one = validate.Column(name='Color')

# If the column has a range of acceptable values, set the column_type to range, and set acceptable_range
# to whatever tolerance the range has.
# The following will allow the `Age` column to differ by plus or minus two years.
column_two = validate.Column(name='Age', column_type='Range', acceptable_range=2)

# Now put those columns into a list that will get passed to a Validator object.
column_list = [column_one, column_two]

# To actually validate the data, create a Validator object. Put whatever column is the unique
# identifier (in this case, Name) as identifying_column
validator = validate.Validator(reference_csv='path/to/reference.csv',
                               test_csv='path/to_test.csv',
                               column_list=column_list,
                               identifying_column='Name')
                               
# With the object set up, we can run tests to make sure the data is as it should be.
# All methods will return True if everything is OK, and False if something is wrong.
# Details on what went wrong get printed at the WARNING level using the logging module.

# Check that the reference and test CSV files have the same headers.
headers_are_same = validator.same_columns_in_ref_and_test()

# Check that all the columns in the column_list are in both the reference and test CSV files.
test_columns_present = validator.all_test_columns_in_ref_and_test()

# Check that both test and reference have all the same sample names.
samples_present = validator.check_samples_present()

# Finally, check that Categorical columns are identical for test and reference, and range values
# are within acceptable limits
values_are_ok = validator.check_columns_match()

```