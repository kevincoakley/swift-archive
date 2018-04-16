#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(install_requires=[
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
      version="0.0.1",
      description="OpenStack Swift Bulk Delete CLI",
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
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
      ],
      **extra
      )
