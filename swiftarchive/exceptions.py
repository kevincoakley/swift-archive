#!/usr/bin/env python


class AuthException(Exception):

    def __init__(self, arg):
        self.msg = arg

    def __str__(self):
        return self.msg


class LocalFileException(Exception):

    def __init__(self, arg):
        self.msg = arg

    def __str__(self):
        return self.msg


class SwiftException(Exception):

    def __init__(self, arg):
        self.msg = arg

    def __str__(self):
        return self.msg
