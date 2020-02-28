#!/usr/bin/env python

import unittest
import swiftarchive.arguments as arguments


class ArgumentsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_arguments(self):
        args = arguments.parse_arguments(["--debug"])
        self.assertTrue(args.debug)
