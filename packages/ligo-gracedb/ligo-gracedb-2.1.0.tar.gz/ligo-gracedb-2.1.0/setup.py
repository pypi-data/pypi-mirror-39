# -*- coding: utf-8 -*-
# Copyright (C) Brian Moe, Branson Stephens (2015)
#
# This file is part of gracedb
#
# gracedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gracedb.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
from setuptools import setup, find_packages


def parse_version(path):
    """Extract the `__version__` string from the given file
    """
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Required packages for tests
tests_require = []
if sys.version_info.major < 3:
    tests_require.append('mock')

setup(
  name = "ligo-gracedb",
  version = parse_version(os.path.join('ligo', 'gracedb', 'version.py')),
  maintainer = "Tanner Prestegard, Alexander Pace",
  maintainer_email = "tanner.prestegard@ligo.org, alexander.pace@ligo.org",
  description = "Gravitational Wave Candidate Event Database",
  long_description = "The gravitational wave candidate event database (GraceDB) is a system to organize candidate events from gravitational wave searches and to provide an environment to record information about follow-ups. A simple client tool is provided to submit a candidate event to the database.",

  url = "https://wiki.ligo.org/DASWG/GraceDB",
  license = 'GPLv2+',
  namespace_packages = ['ligo'],
  #provides = ['ligo.gracedb'],
  packages = find_packages(),

  install_requires = ['future', 'six'],
  tests_require = tests_require,

  package_data = { 'ligo.gracedb.test' : ['data/*', 'test.sh', 'README'] },
  entry_points={
      'console_scripts': [
          'gracedb=ligo.gracedb.cli:main',
      ],
  }

)
