from setuptools import setup

setup(
    name='page-py',
    version='1.0',
    description='Library for dealing with PAGE XML files.',
    install_requires=['lxml>=4.6.0', 'python-dateutil>=2.8.0'],
    tests_require=['rstr>=3.0.0'],
    test_suite='page.test',
    packages=[
        'page',
        'page.elements'
    ]
)
