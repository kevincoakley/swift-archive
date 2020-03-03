#!/usr/bin/env python

import os
import time
import errno
import unittest
from mock import patch
import swiftarchive.exceptions
import swiftarchive.files


def side_effect_islink(file_path):
    if file_path == "/tmp/symlink":
        return True
    else:
        return False


class FilesTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('swiftarchive.files.check_modified_time')
    @patch('os.path.islink')
    @patch('os.walk')
    def test_get_files(self, mock_walk, mock_islink, mock_modified):
        #
        # Test get_files when check_modified_time is always True
        #
        mock_modified.return_value = True

        mock_walk.return_value = [
            ('/tmp', ('backup',), ('20190101-00.gz', '20190101-01.gz', '20190101-02.gz', 'a.txt', 'b.txt', 'symlink')),
            ('/tmp/backup', (), ('20190101-00.gz', '20190101-01.gz', '20190101-02.gz')),
        ]

        mock_islink.side_effect = side_effect_islink

        tmp = swiftarchive.files.get_files("/tmp/")

        self.assertEqual(tmp, [
            '/tmp/20190101-00.gz',
            '/tmp/20190101-01.gz',
            '/tmp/20190101-02.gz',
            '/tmp/a.txt',
            '/tmp/b.txt',
            '/tmp/backup/20190101-00.gz',
            '/tmp/backup/20190101-01.gz',
            '/tmp/backup/20190101-02.gz'
        ])

        #
        # Test get_files when check_modified_time is always False
        #
        mock_modified.return_value = False

        tmp = swiftarchive.files.get_files("/tmp/")

        self.assertEqual(tmp, [])

    @patch('os.path.getmtime')
    def test_check_modified_time(self, mock_mtime):
        #
        # Test a file modified 600 seconds ago returns True when seconds_since_updated is 300
        #
        mock_mtime.return_value = time.time() - 600

        self.assertEqual(swiftarchive.files.check_modified_time("old_file", 300), True)

        #
        # Test a file modified 10 seconds ago returns False when seconds_since_updated is 300
        #
        mock_mtime.return_value = time.time() - 10

        self.assertEqual(swiftarchive.files.check_modified_time("new_file", 300), False)

        #
        # Test FileNotFoundError raises LocalFileException (failing test)
        #
        mock_mtime.side_effect = OSError(errno.ENOENT, os.strerror(errno.ENOENT), "missing_file")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.check_modified_time("missing_file", 300)

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "File \"missing_file\" could not be found")

        #
        # Test PermissionError raises LocalFileException (failing test)
        #
        mock_mtime.side_effect = OSError(errno.EACCES, os.strerror(errno.EACCES), "permission_file")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.check_modified_time("permission_file", 300)

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Permission error with \"permission_file\"")

        #
        # Test Input/Output Error raises Unknown LocalFileException (failing test)
        #
        mock_mtime.side_effect = OSError(errno.EIO, os.strerror(errno.EIO), "io_error")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.check_modified_time("io_error", 300)

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Unknown error with \"io_error\": Input/output error")

        #
        # Test a string seconds_since_updated value raises LocalFileException (failing test)
        #
        mock_mtime.side_effect = None

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.check_modified_time("string_seconds_since_updated", "string")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Invalid seconds_since_updated: string")

    def test_md5_hash(self):
        # Test the md5 hash calculation on an actual file
        calculated_md5_hash = "0d8591aa95f4d56cd91d58d92a700a18"

        computed_md5_hash = swiftarchive.files.md5("./tests/test_files/md5_check")

        self.assertEqual(calculated_md5_hash, computed_md5_hash)

    @patch('swiftarchive.files.open', create=True)
    def test_md5_hash_mock(self, mock_open):
        mock_open.mock_open(read_data=b'aaa')

        #
        # Test FileNotFoundError raises LocalFileException (failing test)
        #
        mock_open.side_effect = OSError(errno.ENOENT, os.strerror(errno.ENOENT), "md5_not_found")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.md5("md5_not_found")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "File \"md5_not_found\" could not be found")

        #
        # Test PermissionError raises LocalFileException (failing test)
        #
        mock_open.side_effect = OSError(errno.EACCES, os.strerror(errno.EACCES), "md5_permission")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.md5("md5_permission")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Permission error with \"md5_permission\"")

        #
        # Test Input/Output Error raises Unknown LocalFileException (failing test)
        #
        mock_open.side_effect = OSError(errno.EIO, os.strerror(errno.EIO), "io_error")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.md5("io_error")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Unknown error with \"io_error\": Input/output error")

    @patch('os.remove')
    def test_delete(self, mock_remove):
        #
        # Test IsADirectoryError raises LocalFileException (failing test)
        #
        mock_remove.side_effect = OSError(errno.EISDIR, os.strerror(errno.EISDIR), "delete_directory")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.delete("delete_directory")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Path \"delete_directory\" is a directory and will not be deleted")

        #
        # Test FileNotFoundError raises LocalFileException (failing test)
        #
        mock_remove.side_effect = OSError(errno.ENOENT, os.strerror(errno.ENOENT), "delete_not_found")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.delete("delete_not_found")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "File \"delete_not_found\" could not be found")

        #
        # Test PermissionError raises LocalFileException (failing test)
        #
        mock_remove.side_effect = OSError(errno.EACCES, os.strerror(errno.EACCES), "delete_permission")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.delete("delete_permission")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Permission error with \"delete_permission\"")

        #
        # Test Input/Output Error raises Unknown LocalFileException (failing test)
        #
        mock_remove.side_effect = OSError(errno.EIO, os.strerror(errno.EIO), "io_error")

        with self.assertRaises(swiftarchive.exceptions.LocalFileException) as lfe:
            swiftarchive.files.delete("io_error")

        the_exception = lfe.exception
        self.assertEqual(str(the_exception), "Unknown error with \"io_error\": Input/output error")
