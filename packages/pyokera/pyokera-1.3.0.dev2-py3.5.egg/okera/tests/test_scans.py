# Copyright 2017 Okera Inc. All Rights Reserved.
#
# Tests that should run on any configuration. The server auth can be specified
# as an environment variables before running this test.

import unittest

import numpy

from okera.tests import pycerebro_test_common as common

class BasicTest(unittest.TestCase):
    def test_sparse_data(self):
        with common.get_planner() as planner:
            df = planner.scan_as_pandas("rs.sparsedata")
            self.assertEqual(96, len(df), msg=df)
            self.assertEqual(68, df['age'].count(), msg=df)
            self.assertEqual(10.0, df['age'].min(), msg=df)
            self.assertEqual(96.0, df['age'].max(), msg=df)
            self.assertEqual(b'sjc', df['defaultcity'].max(), msg=df)
            self.assertEqual(86, df['description'].count(), msg=df)

    def test_nulls(self):
        with common.get_planner() as planner:
            df = planner.scan_as_pandas("select string_col from rs.alltypes_null")
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['string_col'][0]), msg=df)

            df = planner.scan_as_pandas(
                "select length(string_col) as c from rs.alltypes_null")
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['c'][0]), msg=df)

    def test_timestamp_functions(self):
        with common.get_planner() as planner:
            json = planner.scan_as_json("""
                select date_add('2009-01-01', 10) as c from okera_sample.sample""")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('2009-01-11 00:00:00+00:00', str(json[0]['c']), msg=json)
            self.assertEqual('2009-01-11 00:00:00+00:00', str(json[1]['c']), msg=json)

    def test_scan_as_json_max_records(self):
        sql = "select * from okera_sample.sample"
        with common.get_planner() as planner:
            json = planner.scan_as_json(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(json) == 1, msg='max_records not respected')
            json = planner.scan_as_json(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(json) == 2, msg='max_records not respected')

    def test_scan_as_pandas_max_records(self):
        sql = "select * from okera_sample.sample"
        with common.get_planner() as planner:
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 1, msg='max_records not respected')
            pd = planner.scan_as_pandas(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 2, msg='max_records not respected')

if __name__ == "__main__":
    unittest.main()
