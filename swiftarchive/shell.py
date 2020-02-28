#!/usr/bin/env python

import sys
import logging
import swiftarchive.arguments as arguments


def main():

    args = arguments.parse_arguments(sys.argv[1:])

    log_level = logging.INFO

    if args.debug is True:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
                        handlers=[logging.StreamHandler()])

    logging.debug("os_username: %s", args.os_username)
    logging.debug("os_password: %s", args.os_password)
    logging.debug("os_project_name: %s", args.os_project_name)
    logging.debug("os_auth_url: %s", args.os_auth_url)
    logging.debug("container: %s", args.container)
    logging.debug("archive_path: %s", args.archive_path)
    logging.debug("seconds_since_updated: %s", args.seconds_since_updated)

    if args.os_username is None or args.os_password is None or \
        args.os_project_name is None or args.os_auth_url is None or \
            args.container is None or args.archive_path is None:
        return ('''
swift-archive requires OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME,
OS_AUTH_URL, CONTAINER, and ARCHIVE_PATH to be set or overridden with
--os-username, --os-password, --os-project-name, --os-auth-url,
--container, or --archive-path.''')

    return 0
