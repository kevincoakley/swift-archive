#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(install_requires=[
        "python-swiftclient>=3.8.0",
        "keystoneauth1>=3.18.0",
    ],
        include_package_data=True,
        test_suite="tests.suite.load_tests",
    )
except ImportError:
    from distutils.core import setup
    extra = {}


def readme():
    with open("README.md") as f:
        return f.read()


setup(name="openstack-swift-archive",
      version="0.1.0",
      description="",
      long_description=readme(),
      author="Kevin Coakley",
      author_email="kcoakley@sdsc.edu",
      scripts=[
          "bin/swift-archive",
      ],
      url="",
      packages=[
          "swiftarchive",
      ],
      package_data={
      },
      platforms="Posix; MacOS X",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      **extra
      )
