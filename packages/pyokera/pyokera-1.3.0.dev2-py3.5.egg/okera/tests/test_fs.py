# Copyright 2017 Okera Inc. All Rights Reserved.
#
# Tests that should run on any configuration. The server auth can be specified
# as an environment variables before running this test.

# pylint: disable=no-member
# pylint: disable=no-self-use
# pylint: disable=protected-access
# pylint: disable=too-many-public-methods

import unittest

from okera import context, _thrift_api
from okera.tests import pycerebro_test_common as common

class FsTest(unittest.TestCase):
    def test_ls(self):
        planner = common.get_planner()
        result = planner.ls('s3://cerebrodata-test/sample/')
        self.assertEqual(['s3://cerebrodata-test/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/sample')
        self.assertEqual(['s3://cerebrodata-test/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/sample/sample.txt')
        self.assertEqual(['s3://cerebrodata-test/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/sample/sample.txt2')
        self.assertEqual([], result)
        planner.close()

    def test_cat(self):
        planner = common.get_planner()
        result = planner.cat('s3://cerebrodata-test/sample/sample.txt')
        self.assertEqual('This is a sample test file.\nIt should consist of two lines.',
                         result)
        planner.close()

    def test_errors(self):
        planner = common.get_planner()
        with self.assertRaises(ValueError):
            planner.cat('s3://cerebrodata-test/sample/not-a-file')
        planner.close()

    def test_as_testuser(self):
        ctx = context()
        ctx.enable_token_auth(token_str='testuser')
        planner = ctx.connect()

        # Test user has access to this directory by URI
        result = planner.ls('s3://cerebrodata-test/sample/')
        self.assertEqual(['s3://cerebrodata-test/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/sample/sample.txt')
        self.assertEqual(['s3://cerebrodata-test/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/sample/sample.txt2')
        self.assertEqual([], result)

        # Test user does not have access to this directory
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            result = planner.ls('s3://cerebro-datasets/transactions/')

class RegisteredTest(unittest.TestCase):
    def test_basic(self):
        planner = common.get_planner()
        result = planner.get_catalog_objects_at('file:/opt/data/users')
        self.assertTrue('file:/opt/data/users' in result)
        self.assertTrue('okera_sample.users' in result['file:/opt/data/users'])
        self.assertTrue('cerebro_sample.users' in result['file:/opt/data/users'])

        result = planner.get_catalog_objects_at('file:/opt/data/')
        self.assertTrue('file:/opt/data/sample' in result)
        self.assertTrue('file:/opt/data/users' in result)

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))

        # Two datasets registered here
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(2, len(datasets))

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')
        self.assertEqual(1, len(result))

        planner.close()

    def test_as_testuser(self):
        ctx = context()
        ctx.enable_token_auth(token_str='testuser')
        planner = ctx.connect()

        result = planner.get_catalog_objects_at('file:/opt/data/')
        self.assertTrue('file:/opt/data/sample' in result)
        self.assertTrue('file:/opt/data/users' in result)

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))

        # Two datasets registered here, but this user only has one. Make sure it is
        # ACLed correctly.
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(1, len(datasets))
        self.assertEqual('demo_test.transactions_schemaed', datasets[0])

        # Test user does not have access to this directory
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')

if __name__ == "__main__":
    unittest.main()
