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

class GvmProtocol:
    """Base class for different GVM protocols

    Attributes:
        connection (:class:`gvm.connections.GvmConnection`): Connection to use
            to talk with the remote daemon. See :mod:`gvm.connections` for
            possible connection types.
        transform (`callable`_, optional): Optional transform callable to
            convert response data. After each request the callable gets passed
            the plain response data which can be used to check the data and/or
            conversion into different representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.
    """

    def __init__(self, connection, *, transform=None):
        self._connection = connection

        self._connected = False

        self._transform_callable = transform

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _read(self):
        """Read a command response from gvmd

        Returns:
            str: Response from server.
        """
        return self._connection.read()

    def _send(self, data):
        """Send a command to the server

        Args:
            data (str): Data to be send over the connection to the server
        """
        self.connect()
        self._connection.send(data)

    def _transform(self, data):
        transform = self._transform_callable
        if transform is None:
            return data
        return transform(data)

    def _send_xml_command(self, xmlcmd):
        """Send a xml command to the remote server

        Arguments:
            xmlcmd (gvm.xml.XmlCommand): XmlCommand instance to send
        """
        return self.send_command(xmlcmd.to_string())

    def is_connected(self):
        """Status of the current connection

        Returns:
            bool: True if a connection to the remote server has been
                  established.
        """
        return self._connected

    def connect(self):
        """Initiates a protocol connection

        Normally connect isn't called directly. Either it's called automatically
        when sending a protocol command or when using a `with statement`_.

        .. _with statement:
            https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
        """
        if not self.is_connected():
            self._connection.connect()
            self._connected = True

    def disconnect(self):
        """Disconnect the connection

        Ends and closes the connection.
        """
        if self.is_connected():
            self._connection.disconnect()
            self._connected = False

    def send_command(self, cmd):
        """Send a command to the remote server

        If the class isn't connected to the server yet the connection will be
        established automatically.

        Arguments:
            cmd (str): Command as string to be send over the connection to
                the server.

        Returns:
            any: The actual returned type depends on the set transform.

            Per default - if no transform is set explicitly - the response is
            returned as string.
        """
        try:
            self._send(cmd)
            response = self._read()
        except Exception as e:
            self.disconnect()
            raise e

        return self._transform(response)
