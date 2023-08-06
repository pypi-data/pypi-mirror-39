# coding=utf-8
import json
import sys
from contextlib import contextmanager
from unittest import TestCase
from StringIO import StringIO

import os

from mongolog.logger import MongoLogger


class PyLoggerTests(TestCase):
    def setUp(self):
        connection_string = 'mongodb://tester:tester@localhost:27017/test'
        self.logger = MongoLogger(connection_string, collection_name='unittests')

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_write_debug_log(self):
        with self.captured_output() as (out, err):
            self.logger.debug('hello from unittest')
        error = err.getvalue().strip()
        self.assertEqual(error, '', msg='Error output was not empty, some error occurred')

    def test_write_debug_with_extra(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'data', 'json_1.json')
        json_data = json.loads(open(path).read())
        with self.captured_output() as (out, err):
            self.logger.debug('json extra', extra={'PitBoss Log': json_data})
        error = err.getvalue().strip()
        self.assertEqual(error, '', msg='Error output was not empty, some error occurred')
