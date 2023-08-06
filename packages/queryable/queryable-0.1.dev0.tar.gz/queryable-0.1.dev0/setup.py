"""*MemDB* SQLite in-memory database without the boilerplate

If you know would like to work with a SQL-based data structure
in memory, this module makes your life as easy as possible
"""

from setuptools import setup


__author__ = 'Kurt Rose'
__version__ = '0.1dev'
__contact__ = 'kurt@kurtrose.com'
__url__ = 'https://github.com/kurtbrose/queryable'
__license__ = 'BSD'


setup(
    name='queryable',
    version=__version__,
    description='SQLite in memory without boiler plate',
    long_description=__doc__,
    author=__author__,
    author_email=__contact__,
    url=__url__,
    packages=['queryable'],
    install_requires=[],
    extras_require={},
    license=__license__,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6']
)
