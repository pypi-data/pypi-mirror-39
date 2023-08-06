# -*- coding: utf-8 -*-
import os.path
import re
import warnings
import sys

from setuptools import setup, find_packages
from beltway import __version__ as version

REQUIRED_PACKAGES = [
    "six",
    "structlog",
    "ws4py",
]

#
# news = os.path.join(os.path.dirname(__file__), 'docs', 'news.rst')
# news = open(news).read()
# parts = re.split(r'([0-9\.]+)\s*\n\r?-+\n\r?', news)
# found_news = ''
# for i in range(len(parts) - 1):
#     if parts[i] == version:
#         found_news = parts[i + i]
#         break
# if not found_news:
#     warnings.warn('No news for this version found.')

long_description = """
Beltway is a threaded WAMP client (a loose port of Autobahn).
"""

# if found_news:
#     title = 'Changes in %s' % version
#     long_description += '\n%s\n%s\n' % (title, '-' * len(title))
#     long_description += found_news

setup(
    name='beltway',
    version=version,
    author='Unspecified',
    url='https://github.com/matthewh/beltway',
    license='MIT',
    description='Threaded WAMP client',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    setup_requires=['nose>=1.0'],
    tests_require=['nose>=1.0.3'],
    test_suite='nose.collector',
    zip_safe=False
)
