#!/usr/bin/env python

import unittest
import swiftarchive.exceptions

from swiftarchive.exceptions import AuthException
from swiftarchive.exceptions import SwiftException
from swiftarchive.exceptions import LocalFileException


class ExceptionsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_auth_exception(self):
        with self.assertRaises(swiftarchive.exceptions.AuthException) as ae:
            raise AuthException("Test Auth Exception")

        the_exception = ae.exception
        self.assertEqual(str(the_exception), "Test Auth Exception")

    def test_local_file_exception(self):
        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as se:
            raise LocalFileException("Test Local File Exception")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Test Local File Exception")

    def test_swift_exception(self):
        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            raise SwiftException("Test Swift Exception")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Test Swift Exception")
