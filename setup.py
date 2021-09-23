from distutils.core import setup

setup(
    name='page-py',
    version='1.0',
    description='Library for dealing with PAGE XML files.',
    requires=['lxml'],
    packages=['page']
)