"""Admin tools for adding, deleting, and getting users.
:author Josh Harkema
"""
import json
from urllib.request import urlopen, Request

BASE_URL = "https://api.acriticismlab.org/secure/user/"
ENCODING = "utf8"


class User:
    """ Class handles all admin functions for the ACL database. A valid auth
    token must be passed, or a ValueError will be raised.
    """

    def __init__(self, access_token):
        """
        :param access_token: a valid access token from the
        authentication_handler.Authentication class.
        """
        if access_token is None:
            raise ValueError("Access token cannot be null.")

        self.headers = {
            'Authorization': 'Bearer %s' % access_token,
            'Content-Type': 'application/json'
        }

    def add(self, email, required_sonnets=0, is_admin=False):
        """
        :param email: the new user's email.
        :param required_sonnets: optional value.
        :param is_admin: defaults to False.
        :return: the response.
        """
        username = email.split("@")[0]
        details = {
            "username": username,
            "email": email,
            "requiredSonnets": required_sonnets,
            "isAdmin": is_admin
        }

        request = Request(BASE_URL + 'add',
                          data=bytes(json.dumps(details), encoding=ENCODING),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def delete(self, username):
        """
        :param username: the username of the user to delete.
        :return: the response.
        """
        request = Request(BASE_URL + 'delete/' + username,
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def get_all(self):
        """
        :return: a parsed json list of all users.
        """
        request = Request(BASE_URL + 'all',
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)
