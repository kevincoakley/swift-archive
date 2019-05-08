#!/usr/bin/env python


import unittest
import swiftarchive.exceptions

from swiftarchive.exceptions import AuthException
from swiftarchive.exceptions import SwiftException


class ExceptionsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_auth_exception(self):
        with self.assertRaises(swiftarchive.exceptions.AuthException) as ae:
            raise AuthException("Test Auth Exception")

        the_exception = ae.exception
        self.assertEqual(str(the_exception), "Test Auth Exception")

    def test_swift_exception(self):
        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            raise SwiftException("Test Swift Exception")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Test Swift Exception")
