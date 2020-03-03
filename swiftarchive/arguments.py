#!/usr/bin/env python

import os
import argparse


def parse_arguments(args):
    """
    Parse Commandline Arguments
    :param args: *args positional arguments
    :return: Commandline arguments parsed by argparse
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug',
                        dest="debug",
                        action='store_true')

    parser.add_argument("--os-username",
                        metavar="os_username",
                        dest="os_username",
                        help="OpenStack Keystone Username.",
                        default=os.environ.get('OS_USERNAME', None))

    parser.add_argument("--os-password",
                        metavar="os_password",
                        dest="os_password",
                        help="OpenStack Keystone Password.",
                        default=os.environ.get('OS_PASSWORD', None))

    parser.add_argument("--os-project-name",
                        metavar="os_project_name",
                        dest="os_project_name",
                        help="OpenStack Keystone Project Name.",
                        default=os.environ.get('OS_PROJECT_NAME', None))

    parser.add_argument("--os-auth-url",
                        metavar="os_auth_url",
                        dest="os_auth_url",
                        help="OpenStack Keystone Auth URL.",
                        default=os.environ.get('OS_AUTH_URL', None))

    parser.add_argument("--container",
                        metavar="container",
                        dest="container",
                        help="OpenStack Swift Container.",
                        default=os.environ.get('CONTAINER', None))

    parser.add_argument("--archive-path",
                        metavar="archive_path",
                        dest="archive_path",
                        help="Local Path to Archive to OpenStack Swift.",
                        default=os.environ.get('ARCHIVE_PATH', None))

    parser.add_argument('--delete',
                        dest="delete",
                        help="Delete Local Files Once Uploaded to Swift.",
                        action='store_false',
                        default=os.environ.get('LOCAL_DELETE', False))

    parser.add_argument("--seconds-since-updated",
                        metavar="seconds_since_updated",
                        dest="seconds_since_updated",
                        help="Archive All Files That Haven't Been Updated Since in Seconds.",
                        default=os.environ.get('SECONDS_SINCE_UPDATED', 0))

    return parser.parse_args(args)
