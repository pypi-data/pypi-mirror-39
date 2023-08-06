"""OAuth2 handler for admin functions
:author Josh Harkema
"""
import base64

import requests


class Authentication:
    """Class deals with obtaining and storing an OAuth token. """
    AUTH_URL = 'https://api.acriticismlab.org/oauth/authorize'
    TOKEN_URL = 'https://api.acriticismlab.org/oauth/token'
    CLIENT_ID = 'databaseAuthentication'
    CLIENT_SECRET = ''
    ENCODING = 'utf-8'
    SCOPES = []

    def __init__(self, username=None, password=None, proxies=None):
        """
        :param username: valid ACL database username.
        :param password: valid ACL database password.
        :param proxies: leave at default.
        """
        self.access_token = None
        self.refresh_token = None
        self.proxies = proxies if proxies is not None else \
            dict(http='', https='')
        self.username = username
        self.password = password
        self.auth = unbufferize_buffer(
            base64.b64encode(bufferize_string(
                '%s:%s' % (self.CLIENT_ID, self.CLIENT_SECRET))))

    def do_authorization(self):
        """ Handles actual auth request.
        :return: nothing, writes directly to instance vars.
        """
        params = self._grant_password_request(self.username, self.password)
        headers = self._token_request_headers(params['grant_type'])
        headers['Authorization'] = 'Basic %s' % self.auth

        response = requests.post(self.TOKEN_URL,
                                 data=params,
                                 headers=headers,
                                 proxies=self.proxies,
                                 verify=True)

        if response.status_code != 200:
            raise ValueError("Bad Response: %s" % response.status_code)
        else:
            response = response.json()
            self.refresh_token = response['refresh_token']
            self.access_token = response['access_token']
            self.SCOPES = response['scope']

    def _grant_password_request(self, login, password):
        return dict(grant_type='password',
                    username=login,
                    scope=' '.join(self.SCOPES),
                    password=password)

    @staticmethod
    def _token_request_headers(grant_type):
        return dict()


def unbufferize_buffer(content):
    return content.decode('UTF-8')


def bufferize_string(content):
    return bytes(content, 'UTF-8')
