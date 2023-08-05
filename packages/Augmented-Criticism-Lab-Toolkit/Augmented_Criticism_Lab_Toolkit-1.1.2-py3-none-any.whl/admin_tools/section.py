"""Admin tools for adding, modifying, and deleting sections.
:author Josh Harkema
"""
import json
from urllib.request import urlopen, Request

BASE_URL = "https://api.acriticismlab.org/secure/section/"
ENCODING = "utf8"


class Section:
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

    def add(self, title, text, description, book_id, author_id):
        """
        :param title: the section's title.
        :param text: the section's text.
        :param description: an optional description.
        :param book_id: the id of the book the section is from.
        :param author_id: the author's id.
        :return: the response.
        """
        section = {
            "title": title,
            "text": text,
            "description": description,
            "bookId": book_id,
            "authorId": author_id
        }

        request = Request(BASE_URL + 'add',
                          data=bytes(json.dumps(section), encoding=ENCODING),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def modify(self, _id, title, text, description, book_id, author_id):
        """
        :param _id: the database id of the section.
        :param title: the section's title.
        :param text: the section's text.
        :param description: an optional description.
        :param book_id: the id of the book the section is from.
        :param author_id: the author's id.
        :return: the response.
        """
        section = {
            "id": _id,
            "title": title,
            "text": text,
            "description": description,
            "bookId": book_id,
            "authorId": author_id
        }

        request = Request(BASE_URL + 'modify',
                          data=bytes(json.dumps(section), encoding=ENCODING),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def delete(self, _id):
        """
        :param _id: the id of the section to delete.
        :return: the response.
        """

        request = Request(BASE_URL + 'delete/' + str(_id),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)
