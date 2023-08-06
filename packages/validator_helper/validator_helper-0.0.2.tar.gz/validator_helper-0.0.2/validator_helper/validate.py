#!/usr/bin/env python

import pandas as pd
import logging


class Column(object):

    def __init__(self, name, column_type='Categorical', acceptable_range=None):
        self.name = name
        self.column_type = column_type
        self.acceptable_range = acceptable_range


class Validator(object):
    def __init__(self, reference_csv, test_csv, column_list, identifying_column):
        self.identifying_column = identifying_column
        self.reference_csv_df = pd.read_csv(reference_csv)
        self.test_csv_df = pd.read_csv(test_csv)
        self.column_list = column_list
        self.reference_headers = list(self.reference_csv_df.columns)
        self.test_headers = list(self.test_csv_df.columns)

    def same_columns_in_ref_and_test(self):
        if set(self.reference_headers) != set(self.test_headers):
            return False
        else:
            return True

    def all_test_columns_in_ref_and_test(self):
        all_columns_present = True
        for column in self.column_list:
            if column.name not in self.reference_headers:
                logging.warning('{} was not found in Reference CSV.'.format(column.name))
                all_columns_present = False
            if column.name not in self.test_headers:
                logging.warning('{} was not found in Test CSV.'.format(column.name))
                all_columns_present = False
        return all_columns_present

    def check_samples_present(self):
        samples_in_ref = set(self.reference_csv_df[self.identifying_column])
        samples_in_test = set(self.test_csv_df[self.identifying_column])
        if samples_in_ref != samples_in_test:
            logging.warning('Not all samples in Test set are found in Reference set.')
            logging.warning('Samples in Test but not Reference: {}'.format(samples_in_test.difference(samples_in_ref)))
            logging.warning('Samples in Reference but not Test: {}'.format(samples_in_ref.difference(samples_in_test)))
            return False
        else:
            return True

    def check_columns_match(self):
        columns_match = True
        for testindex, testrow in self.test_csv_df.iterrows():
            for refindex, refrow in self.reference_csv_df.iterrows():
                if testrow[self.identifying_column] == refrow[self.identifying_column]:
                    for column in self.column_list:
                        if pd.isna(testrow[column.name]) and pd.isna(refrow[column.name]):
                            pass  # Equality doesn't work for na values in pandas, so have to check this first.
                        elif column.column_type == 'Categorical':
                            if testrow[column.name] != refrow[column.name]:
                                logging.warning('Attribute {} does not match for sample {}'.format(column.name,
                                                                                                   testrow[self.identifying_column]))
                                columns_match = False
                        elif column.column_type == 'Range':
                            lower_bound = float(refrow[column.name]) - column.acceptable_range
                            upper_bound = float(refrow[column.name]) + column.acceptable_range
                            if not lower_bound <= float(testrow[column.name]) <= upper_bound:
                                logging.warning('Attribute {} is out of range for sample {}'.format(column.name,
                                                                                                    testrow[self.identifying_column]))
                                columns_match = False
        return columns_match



