# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Main module of python-gvm.
"""
from .utils import get_version_string

VERSION = (1, 0, 0, 'beta', 2)
"""
Current Version of python-gvm as a tuple
"""

def get_version():
    """Returns the version of python-gvm as a string in `PEP440`_ compliant format.

    Returns:
        str: Current version of python-gvm

    .. _PEP440:
       https://www.python.org/dev/peps/pep-0440
    """
    return get_version_string(VERSION)
