##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup"""

import os
from setuptools import setup, find_packages


def read(path):
    rnames = path.split('/')
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='z3c.preference',
    version='1.0',
    author="Michael Howitz",
    author_email="zope-dev@zope.org",
    description="UI for zope.preference using z3c.pagelet and z3c.form.",
    long_description='\n\n'.join([
            read('README.rst'),
            '.. contents::',
            read('CHANGES.rst'),
            read('src/z3c/preference/README.rst'),
            read('src/z3c/preference/categories.rst'),
            read('TODO.rst'),
    ]),
    license="ZPL 2.1",
    keywords="zope3 bluebream z3c preference ui",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
    ],
    url='https://github.com/zopefoundation/z3c.preference',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=[
            'zope.app.wsgi >= 3.7',
            'zope.browserresource',
            'zope.login',
            'zope.principalregistry',
            'zope.app.principalannotation',
            'zope.securitypolicy',
            'zope.testbrowser >= 5',
            'zope.testing',
        ],
    ),
    install_requires=[
        'setuptools',
        'z3c.form',
        'z3c.formui',
        'z3c.pagelet',
        'zope.preference',
    ],
    zip_safe=False,
)
