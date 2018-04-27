#!/usr/bin/env python


class FakeSession(object):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_endpoint(*args, **kwargs):
        pass

    @staticmethod
    def get_token(*args, **kwargs):
        pass

    @staticmethod
    def get(*args, **kwargs):
        pass
