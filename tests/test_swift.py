#!/usr/bin/env python

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
    @patch('builtins.open', create=True)
    @patch('swiftclient.Connection.put_object')
    def test_put_object(self, mock_put_object, mock_open, mock_head_container, mock_getsize, mock_keystone):
        mock_keystone.return_value.status_code = 200
        mock_getsize.return_value = 100
        mock_head_container.return_value = {"x-container-object-count": "99"}

        # Test uploading a small file
        mock_put_object.return_value = "99999999999999999999999999999999"

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        etag = swift.put_object("container", "object")

        self.assertEqual(etag, "99999999999999999999999999999999")

        # Test uploading a large file
        mock_getsize.return_value = 3600000000

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")

        with self.assertRaises(swiftarchive.exceptions.SwiftException):
            swift.put_object("container", "object")

        mock_getsize.return_value = 100
        mock_open.side_effect = FileNotFoundError

        etag = swift.put_object("container", "object")
        self.assertEquals(etag, None)


