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
Module for GVM errors
"""


class GvmError(Exception):
    """An exception for gvm errors

    Base class for all exceptions originating in python-gvm.
    """
    pass


class InvalidArgument(GvmError):
    """Raised if an invalid argument/parameter is passed

    Derives from :py:class:`GvmError`
    """

class RequiredArgument(GvmError):
    """Raised if a required argument/parameter is missing

    Derives from :py:class:`GvmError`
    """
