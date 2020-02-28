#!/usr/bin/env python

import os
import sys
import unittest
from mock import patch
import swiftarchive.shell as shell


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

    def test_main(self):
        # Test that SystemExit is raised when the required args are not passed
        with self.assertRaises(SystemExit):
            with patch.object(sys, 'argv', ["swift-archive", "--container", "test"]):
                shell.main()

        # Test with command line arguments
        with patch.object(sys, 'argv', ["swift-archive",
                                        "--os-username", "test",
                                        "--os-password", "test",
                                        "--os-project-name", "test",
                                        "--os-auth-url", "test",
                                        "--container", "test",
                                        "--archive-path", "test"]):
            shell.main()

        # Test with environment variables
        os.environ["OS_USERNAME"] = "test"
        os.environ["OS_PASSWORD"] = "test"
        os.environ["OS_PROJECT_NAME"] = "test"
        os.environ["OS_AUTH_URL"] = "test"
        os.environ["CONTAINER"] = "test"
        os.environ["ARCHIVE_PATH"] = "test"

        with patch.object(sys, 'argv', ["swift-archive"]):
            shell.main()

        # Test the debug command line argument
        with patch.object(sys, 'argv', ["swift-archive", "--debug"]):
            shell.main()
