# Copyright (c) 2018 Gabriele Baldoni.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: Apache-2.0
#
# Contributors: Gabriele Baldoni MVar implementation in Python

#!/usr/bin/env python3

from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mvar',
    version='0.0.1',
    author='Gabriele Baldoni',
    description='Python implementation of Haskell\'s Control.Concurrent.MVar',
    long_description=read('README.md'),
    packages=['mvar'],
    url='https://github.com/gabrik/mvar-python',
    authon_email='gabriele.baldoni@gmai.com',
    license='Apache 2.O',
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only'
    ],
    include_package_data=True
)
