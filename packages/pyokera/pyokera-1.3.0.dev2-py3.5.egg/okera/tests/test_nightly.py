# Copyright 2017 Okera Inc. All Rights Reserved.
#
# Tests some queries against nightly

import os
import unittest

from okera import context

TEST_LEVEL = 'smoke'
if 'TEST_LEVEL' in os.environ:
    TEST_LEVEL = os.environ['TEST_LEVEL']

ROOT_TOKEN = os.environ['OKERA_HOME'] + '/integration/tokens/cerebro.token'
NIGHTLY_PLANNER = 'ec2-34-215-143-132.us-west-2.compute.amazonaws.com'

class ConnectionErrorsTest(unittest.TestCase):

    @unittest.skipIf(TEST_LEVEL == 'smoke', "Skipping at unit test level.")
    def test_okera_sample_users(self):
        ctx = context()
        ctx.enable_token_auth(token_file=ROOT_TOKEN)
        with ctx.connect(NIGHTLY_PLANNER) as conn:
            json_data = conn.scan_as_json('okera_sample.users')
            self.assertEqual(38455, len(json_data))
            json_data = conn.scan_as_json('okera_sample.users', max_records=200)
            self.assertEqual(200, len(json_data))
            json_data = conn.scan_as_json('okera_sample.users', max_records=40000)
            self.assertEqual(38455, len(json_data))

            json_data = conn.scan_as_json('okera_sample.users',
                                          max_records=200,
                                          max_client_process_count=2)
            self.assertEqual(200, len(json_data))
            pd = conn.scan_as_pandas('okera_sample.users')
            self.assertEqual(38455, len(pd))
            pd = conn.scan_as_pandas('okera_sample.users', max_records=200)
            self.assertEqual(200, len(pd))
            pd = conn.scan_as_pandas('okera_sample.users', max_records=40000)
            self.assertEqual(38455, len(pd))
            pd = conn.scan_as_pandas('okera_sample.users',
                                     max_records=200,
                                     max_client_process_count=2)
            self.assertEqual(200, len(pd))

if __name__ == "__main__":
    unittest.main()
