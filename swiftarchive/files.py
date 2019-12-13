#!/usr/bin/env python

import os
import time
import errno
import hashlib

from swiftarchive.exceptions import LocalFileException


class Files:

    def __init__(self):
        pass

    def get_files(self, path, seconds_since_updated=0):
        """
        :param path: Path to the files
        :param seconds_since_updated: Number of seconds since the file was updated. Default is 0.
        :return: List of files in path
        """
        file_list = []

        for root, dirs, files in os.walk(path):
            for file in files:
                # Construct the full path to the file
                file_path = os.path.join(root, file)

                # If the file is older than seconds_since_updated then add it to file_list
                if self.check_modified_time(file_path, seconds_since_updated):
                    file_list.append(file_path)

        return file_list

    @staticmethod
    def check_modified_time(file_path, seconds_since_updated):
        """
        :param file_path: Path to the file
        :param seconds_since_updated: Number of seconds since the file was updated.
        :return: True if file is older than seconds_since_updated else False
        """
        # Set the default modified time to now
        mtime = time.time()

        # Find the last modified time of the file
        try:
            mtime = os.path.getmtime(file_path)
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                raise LocalFileException("File \"%s\" could not be found" % file_path)
            elif ex.errno == errno.EACCES:
                raise LocalFileException("Permission error with \"%s\"" % file_path)

        # If the file is older than seconds_since_updated then return True
        if time.time() - mtime > seconds_since_updated:
            return True
        else:
            return False

    @staticmethod
    def md5(file_path):
        """
        :param file_path: Path to the file
        :return: md5 hash of file_path
        """
        hash_md5 = hashlib.md5()

        try:
            with open(file_path, "rb") as local:
                for chunk in iter(lambda: local.read(4096), b""):
                    hash_md5.update(chunk)
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                raise LocalFileException("File \"%s\" could not be found" % file_path)
            elif ex.errno == errno.EACCES:
                raise LocalFileException("Permission error with \"%s\"" % file_path)

        return hash_md5.hexdigest()
