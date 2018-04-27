#!/usr/bin/env python

import unittest
from mock import patch

from tests import fake_keystoneauth1

from swiftarchive.swift import Swift


class SwiftTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('keystoneauth1.session.Session', fake_keystoneauth1.FakeSession)
    @patch('swiftclient.Connection.head_container')
    def test_stat_container(self, mock_head_container):
        mock_head_container.return_value = {"x-container-object-count": "99"}

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        number_objects = swift.head("container")

        self.assertEqual(number_objects, "99")

    @patch('keystoneauth1.session.Session', fake_keystoneauth1.FakeSession)
    @patch('swiftclient.Connection.head_object')
    def test_stat_object(self, mock_head_object):
        mock_head_object.return_value = {"etag": "99999999999999999999999999999999"}

        swift = Swift("username", "password", "project", "https://keystone:5000/v3")
        etag = swift.head("ISOS", "SW_DVD9_SA_Win_Ent_8.1_64BIT_English_-2_MLF_X19-49847.ISO")

        self.assertEqual(etag, "99999999999999999999999999999999")
