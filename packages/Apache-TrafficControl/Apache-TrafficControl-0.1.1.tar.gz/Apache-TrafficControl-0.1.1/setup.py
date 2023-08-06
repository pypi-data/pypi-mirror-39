#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys

from setuptools import setup

version = ''
for line in open('trafficops/__init__.py').readlines():
    if '__version__' in line:
        version = line.split('=')[-1].strip().strip("'")
        break

setup(
    name='Apache-TrafficControl',
    version=version,
    author='Apache Software foundation',
    author_email='dev@trafficcontrol.apache.org',
    packages=['common', 'trafficops'],
    url='http://trafficcontrol.apache.org/',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description='Python API Client for Traffic Ops',
    long_description=open('README.txt').read(),
    install_requires=[
        "future>=0.16.0",
        "requests>=2.13.0",
        "munch>=2.1.1",
    ],
)

if ((sys.version_info[0] == 2 and sys.version_info < (2, 7))
   or (sys.version_info[0] == 3 and sys.version_info < (3, 6))):
    msg = ('WARNING: This library may not work properly with Python {0}, '
           'as it is untested for this version.')
    print(msg.format(sys.version.split(' ', 1)[0]))
