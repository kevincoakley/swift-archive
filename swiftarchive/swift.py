#!/usr/bin/env python

from keystoneauth1 import session
from keystoneauth1.identity import v3
from swiftclient import Connection

from swiftarchive.exceptions import AuthException

import keystoneauth1.exceptions
import swiftclient.exceptions


class Swift:

    def __init__(self, os_username, os_password, os_project_name, os_auth_url):
        """
        :param os_username: OpenStack username
        :param os_password: OpenStack password
        :param os_project_name: OpenStack project name
        :param os_auth_url: Keystone v3 auth url
        """
        self.keystone_session = None

        try:
            auth = v3.Password(auth_url=os_auth_url,
                               username=os_username,
                               password=os_password,
                               project_name=os_project_name,
                               user_domain_name='default',
                               project_domain_name='default')
            self.keystone_session = session.Session(auth=auth)

            # Test that the credentials are valid
            self.keystone_session.get(os_auth_url)

        except keystoneauth1.exceptions.http.Unauthorized:
            raise AuthException("Unauthorized")
        except keystoneauth1.exceptions.connection.ConnectFailure:
            raise AuthException("Unable to establish connection")

    def head(self, os_container, os_object=None):
        """
        Get header information for container or object
        :param os_container: container name
        :param os_object: object name (if None then the container will be head'ed)
        :return: If only the container is specified then the number of objects in the container
                 will be returned. If an object is specified then the etag (md5 hash) will be
                 returned. If the container or object isn't found then None is returned.
        """
        swift_conn = Connection(session=self.keystone_session)

        try:
            if os_object is None:
                return swift_conn.head_container(os_container)["x-container-object-count"]
            else:
                return swift_conn.head_object(os_container, os_object)["etag"]
        except swiftclient.exceptions.ClientException:
            return None
