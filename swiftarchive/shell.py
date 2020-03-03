#!/usr/bin/env python

import sys
import logging
import swiftarchive.arguments
import swiftarchive.files
import swiftarchive.swift
from swiftarchive.exceptions import SwiftException


def main():
    """
    :return: 0 if successful otherwise return an error message as a string
    """
    args = swiftarchive.arguments.parse_arguments(sys.argv[1:])

    log_level = logging.INFO

    if args.debug is True:
        log_level = logging.DEBUG

    logger = logging.getLogger('swiftarchive')
    logger.setLevel(level=log_level)
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    logger.debug("os_username: %s", args.os_username)
    logger.debug("os_password: %s", args.os_password)
    logger.debug("os_project_name: %s", args.os_project_name)
    logger.debug("os_auth_url: %s", args.os_auth_url)
    logger.debug("container: %s", args.container)
    logger.debug("archive_path: %s", args.archive_path)
    logger.debug("delete: %s", args.delete)
    logger.debug("seconds_since_updated: %s", args.seconds_since_updated)

    if args.os_username is None or args.os_password is None or \
        args.os_project_name is None or args.os_auth_url is None or \
            args.container is None or args.archive_path is None:
        return ('''
swift-archive requires OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME,
OS_AUTH_URL, CONTAINER, and ARCHIVE_PATH to be set or overridden with
--os-username, --os-password, --os-project-name, --os-auth-url,
--container, or --archive-path.''')

    # Create the Swift object and authenticate to the server
    swift = swiftarchive.swift.Swift(args.os_username, args.os_password, args.os_project_name, args.os_auth_url)

    # Create the Files object and get the list of files to upload to Swift
    file_list = swiftarchive.files.get_files(args.archive_path, seconds_since_updated=args.seconds_since_updated)
    logger.debug("\n".join("{}: {}".format(*k) for k in enumerate(file_list)))

    # Upload files in file_list
    for file_path in file_list:
        logger.debug("file: %s", file_path)

        # Calculate the md5 sum for file_path
        file_md5 = swiftarchive.files.md5(file_path)
        logger.debug(" file md5: %s", file_md5)

        # Upload file_path to Swift
        swift_md5 = swift.put_object(args.container, file_path, args.archive_path)
        logger.debug("swift md5: %s", swift_md5)

        if file_md5 == swift_md5:
            if str(args.delete).lower() == "true":
                logger.debug("deleting: %s", file_path)
                swiftarchive.files.delete(file_path)
        else:
            raise SwiftException("md5 sum does not match for file \"%s\" file: %s swift: %s" %
                                 (file_path, file_md5, swift_md5)) from None

    return 0
