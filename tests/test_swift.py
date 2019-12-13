#!/usr/bin/env python

import os
import errno
import unittest
from mock import patch
import keystoneauth1.exceptions
import swiftarchive.exceptions
import swiftclient.exceptions

from swiftarchive.swift import Swift


class SwiftTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('keystoneauth1.session.Session.get')
    def test_auth(self, mock_keystone):
        mock_keystone.return_value.status_code = 200

        # Test no exceptions
        Swift("username", "password", "project", "https://keystone:5000/v3")

        # Test Unauthorized exception
        mock_keystone.side_effect = keystoneauth1.exceptions.http.Unauthorized()

        with self.assertRaises(swiftarchive.exceptions.AuthException):
            Swift("username", "password", "project", "https://keystone:5000/v3")

        # Test ConnectionFailure exception
        mock_keystone.side_effect = keystoneauth1.exceptions.connection.ConnectFailure()

        with self.assertRaises(swiftarchive.exceptions.AuthException):
            Swift("username", "password", "project", "https://keystone:5000/v3")

    @patch('keystoneauth1.session.Session.get')
    @patch('swiftclient.Connection.head_container')
    def test_stat_container(self, mock_head_container, mock_keystone):
        mock_keystone.return_value.status_code = 200
        mock_head_container.return_value = {"x-container-object-count": "99"}

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        number_objects = swift.head("container")

        self.assertEqual(number_objects, "99")

    @patch('keystoneauth1.session.Session.get')
    @patch('swiftclient.Connection.head_object')
    def test_stat_object(self, mock_head_object, mock_keystone):
        mock_keystone.return_value.status_code = 200
        mock_head_object.return_value = {"etag": "99999999999999999999999999999999"}

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        etag = swift.head("container", "object")

        self.assertEqual(etag, "99999999999999999999999999999999")

        # Test a swiftclient exception
        mock_head_object.side_effect = swiftclient.exceptions.ClientException(msg="")

        response = swift.head("container", "object")

        self.assertEqual(response, None)

    @patch('keystoneauth1.session.Session.get')
    @patch('swiftclient.Connection.put_container')
    def test_put_container(self, mock_put_container, mock_keystone):
        mock_keystone.return_value.status_code = 200

        # Test with no swiftclient exceptions
        mock_put_container.return_value = None

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        response = swift.put_container("script_test")

        self.assertEqual(response, True)

        # Test a swiftclient exception
        mock_put_container.side_effect = swiftclient.exceptions.ClientException(msg="")

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        response = swift.put_container("container")

        self.assertEqual(response, False)

    @patch('keystoneauth1.session.Session.get')
    @patch('os.path.getsize')
    @patch('swiftclient.Connection.head_container')
    @patch('swiftclient.Connection.put_container')
    @patch('swiftarchive.swift.open', create=True)
    @patch('swiftclient.Connection.put_object')
    def test_put_object(self, mock_put_object, mock_open, mock_put_container, mock_head_container,
                        mock_getsize, mock_keystone):
        mock_keystone.return_value.status_code = 200
        mock_getsize.return_value = 100
        mock_head_container.return_value = {"x-container-object-count": "99"}

        #
        # Test automatically creating container before uploading (failing test)
        #
        mock_head_container.side_effect = swiftclient.exceptions.ClientException(msg="")
        mock_put_container.side_effect = swiftclient.exceptions.ClientException(msg="")

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Container \"container\" could not be created")

        # Reset side effects for next tests
        mock_head_container.side_effect = swiftclient.exceptions.ClientException(msg="")
        mock_put_container.side_effect = None

        #
        # Test uploading a small file w/ creating container (passing test)
        #
        mock_put_object.return_value = "99999999999999999999999999999999"

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        etag = swift.put_object("container", "object")

        self.assertEqual(etag, "99999999999999999999999999999999")

        # Reset side effects for next tests
        mock_head_container.side_effect = None
        mock_put_container.side_effect = None

        #
        # Test uploading a small file w/ existing container (passing test)
        #
        mock_put_object.return_value = "99999999999999999999999999999999"

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        etag = swift.put_object("container", "object")

        self.assertEqual(etag, "99999999999999999999999999999999")

        #
        # Test uploading a large file (failing test)
        #
        mock_getsize.return_value = 3600000000

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Upload of \"object\" failed. Files over 3.5GB "
                                             "not supported")

        #
        # Test FileNotFoundError raises SwiftException (failing test)
        #
        mock_getsize.return_value = 100
        mock_open.side_effect = OSError(errno.ENOENT, os.strerror(errno.ENOENT), "object")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "File \"object\" could not be found")

        #
        # Test PermissionError raises SwiftException (failing test)
        #
        mock_open.side_effect = OSError(errno.EACCES, os.strerror(errno.EACCES), "object")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Permission error with \"object\"")

        #
        # Test Swift ClientException raises SwiftException (failing test)
        #
        mock_open.side_effect = swiftclient.exceptions.ClientException(msg="Unknown")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Swift Client Exception with \"object\": Unknown")

        #
        # Test Input/Output Error raises Unknown SwiftException (failing test)
        #
        mock_open.side_effect = OSError(errno.EIO, os.strerror(errno.EIO), "io_error")

        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            swift.put_object("container", "object")

        the_exception = se.exception
        self.assertEqual(str(the_exception), "Unknown error with \"object\": Input/output error")
