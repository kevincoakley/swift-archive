#!/usr/bin/env python

import os
import sys
import unittest
from mock import patch
import swiftarchive.shell as shell
import swiftarchive.exceptions
import swiftarchive.files

from swiftarchive.swift import Swift


class ShellTestCase(unittest.TestCase):

    def setUp(self):
        if "OS_USERNAME" in os.environ:
            del os.environ["OS_USERNAME"]
        if "OS_PASSWORD" in os.environ:
            del os.environ["OS_PASSWORD"]
        if "OS_PROJECT_NAME" in os.environ:
            del os.environ["OS_PROJECT_NAME"]
        if "OS_AUTH_URL" in os.environ:
            del os.environ["OS_AUTH_URL"]
        if "CONTAINER" in os.environ:
            del os.environ["CONTAINER"]
        if "ARCHIVE_PATH" in os.environ:
            del os.environ["ARCHIVE_PATH"]

    @patch('swiftarchive.files.md5')
    @patch.object(Swift, 'put_object')
    @patch('swiftarchive.files.get_files')
    @patch.object(Swift, '__init__')
    def test_main(self, mock_swift_init, mock_get_files, mock_put_object, mock_md5):

        mock_swift_init.return_value = None

        #
        # Test that SystemExit is raised when the required args are not passed
        #
        with patch.object(sys, 'argv', ["swift-archive", "--container", "test"]):
            self.assertRegex(shell.main(), "^\nswift-archive requires")

        #
        # Test with command line arguments
        #
        with patch.object(sys, 'argv', ["swift-archive",
                                        "--os-username", "test",
                                        "--os-password", "test",
                                        "--os-project-name", "test",
                                        "--os-auth-url", "test",
                                        "--container", "test",
                                        "--archive-path", "test"]):
            shell.main()

        #
        # Test with environment variables
        #
        os.environ["OS_USERNAME"] = "test"
        os.environ["OS_PASSWORD"] = "test"
        os.environ["OS_PROJECT_NAME"] = "test"
        os.environ["OS_AUTH_URL"] = "test"
        os.environ["CONTAINER"] = "test"
        os.environ["ARCHIVE_PATH"] = "test"

        with patch.object(sys, 'argv', ["swift-archive"]):
            shell.main()

        #
        # Test the debug command line argument
        #
        with patch.object(sys, 'argv', ["swift-archive", "--debug"]):
            shell.main()

        #
        # Test with one file
        #
        with patch.object(sys, 'argv', ["swift-archive"]):
            mock_get_files.return_value = ['/tmp/mock.txt']
            mock_put_object.return_value = "abcdefghijklmnopqrstuvwxyz123456"
            mock_md5.return_value = "abcdefghijklmnopqrstuvwxyz123456"

            shell.main()

        #
        # Test with one file but Swift md5 does not match File md5
        #
        with self.assertRaises(swiftarchive.exceptions.SwiftException) as se:
            with patch.object(sys, 'argv', ["swift-archive"]):
                mock_get_files.return_value = ['/tmp/mock.txt']
                mock_put_object.return_value = "abcdefghijklmnopqrstuvwxyz123456"
                mock_md5.return_value = "123456abcdefghijklmnopqrstuvwxyz"

                shell.main()

            the_exception = se.exception
            self.assertEqual(str(the_exception), "md5 sum does not match for file \"/tmp/mock.txt\" file: "
                                                 "123456abcdefghijklmnopqrstuvwxyz swift: "
                                                 "abcdefghijklmnopqrstuvwxyz123456")
