#   Copyright 2015 Dan Smith (dsmith+uvc@danplanet.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging
import socket

# Python3 compatibility
try:
    import httplib
except ImportError:
    from http import client as httplib
try:
    import urlparse
    import urllib
except ImportError:
    import urllib.parse as urlparse


class CameraConnectError(Exception):
    pass


class CameraAuthError(Exception):
    pass


class UVCCameraClient(object):
    def __init__(self, host, username, password, port=80):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._cookie = ''
        self._log = logging.getLogger('UVCCamera(%s)' % self._host)

    def _safe_request(self, *args, **kwargs):
        try:
            conn = httplib.HTTPConnection(self._host, self._port)
            conn.request(*args, **kwargs)
            return conn.getresponse()
        except (socket.error, OSError):
            raise CameraConnectError('Unable to contact camera')
        except httplib.HTTPException as ex:
            raise CameraConnectError('Error connecting to camera: %s' % (
                str(ex)))

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': self._username,
                           'password': self._password})
        resp = self._safe_request('POST', '/api/1.1/login', data,
                                  headers=headers)
        if resp.status != 200:
            raise CameraAuthError('Failed to login: %s' % resp.reason)
        headers = dict(resp.getheaders())
        try:
            self._cookie = headers['Set-Cookie']
        except KeyError:
            self._cookie = headers['set-cookie']

    def _cfgwrite(self, setting, value):
        headers = {'Cookie': self._cookie}
        resp = self._safe_request(
            'GET', '/cfgwrite.cgi?%s=%s' % (setting, value),
            headers=headers)
        self._log.debug('Setting %s=%s: %s %s' % (setting, value,
                                                  resp.status,
                                                  resp.reason))
        return resp.status == 200

    def set_led(self, enabled):
        return self._cfgwrite('led.front.status', int(enabled))

    def get_snapshot(self):
        conn = httplib.HTTPConnection(self._host, self._port)
        headers = {'Cookie': self._cookie}
        resp = self._safe_request('GET', '/snap.jpeg',
                                  headers=headers)
        if resp.status in (401, 403, 302):
            raise CameraAuthError('Not logged in')
        elif resp.status != 200:
            raise CameraConnectError(
                'Snapshot failed: %s' % resp.status)
        return resp.read()
