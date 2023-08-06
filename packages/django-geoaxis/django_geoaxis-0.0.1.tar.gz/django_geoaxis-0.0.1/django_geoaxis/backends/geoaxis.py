# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import base64

from social_core.backends.oauth import BaseOAuth2

from django.conf import settings


class GeoAxisOAuth2(BaseOAuth2):
    """
    GeoAxis OAuth2 backend:
    """
    name = 'geoaxis'
    HOST = getattr(settings, 'SOCIAL_AUTH_GEOAXIS_HOST', 'localhost')
    CLIENT_KEY = getattr(settings, 'SOCIAL_AUTH_GEOAXIS_KEY', '')
    CLIENT_SECRET = getattr(settings, 'SOCIAL_AUTH_GEOAXIS_SECRET', '')
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://{0}/ms_oauth/oauth2/endpoints/' \
                        'oauthservice/authorize'.format(HOST)
    ACCESS_TOKEN_URL = 'https://{0}/ms_oauth/oauth2/endpoints/' \
                       'oauthservice/tokens'.format(HOST)
    DEFAULT_SCOPE = getattr(settings, 'SOCIAL_AUTH_GEOAXIS_SCOPE', '')
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'

    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('personatypecode', 'personatypecode'),
        ('DN', 'DN'),
        ('uri', 'uri')
    ]

    def auth_headers(self):
        b64Val = base64.b64encode('{}:{}'.format(
            self.CLIENT_KEY, self.CLIENT_SECRET))
        return {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': "Basic %s" % b64Val}

    def get_user_id(self, details, response):
        return details['uid']

    def get_user_details(self, response):
        """Return user details from GeoAxis account"""
        fullname, first_name, last_name = self.get_user_names(
            '', response.get('firstname'), response.get('lastname'))
        return {'username': response.get('username').lower(),
                'email': response.get('email').lower(),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name,
                'uid': response.get('uid').lower()}

    def user_data(self, access_token, *args, **kwargs):
        """Grab user profile information from GeoAxis.

        Response:

        {
            "uid": "testuser",
            "mail": "testuser@gxis.org",
            "username": "testuser",
            "DN": "cn=testuser, OU=People, OU=Unit, OU=DD, O=Example, C=US",
            "email": "testuser@gxis.org",
            "ID": "testuser",
            "lastname": "testuser",
            "login": "testuser",
            "commonname": "testuser",
            "firstname": "testuser",
            "personatypecode": "AAA",
            "uri": "\/ms_oauth\/resources\/userprofile\/me\/testuser"
        }


        """
        response = self.get_json(
            'https://' + self.HOST + '/ms_oauth/resources/userprofile/me',
            params={'access_token': access_token},
            headers={'Authorization': access_token})
        return response
