"""Admin tools for adding, modifying, and deleting books.
:author Josh Harkema
"""
import json
from urllib.request import urlopen, Request

BASE_URL = "https://api.acriticismlab.org/secure/book/"
ENCODING = "utf8"


class Book:
    """Class handles all admin functions for books. A valid auth
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

    def add(self, author_id, title, publication_year, publication_stmt,
            source_desc, period, category, _type):
        """
        :param author_id: an author's db id.
        :param title: the poem's title.
        :param publication_year: poem's year of publication (if known).
        :param publication_stmt: copyrighted or public domain.
        :param source_desc: MLA citation of poem's source.
        :param period: poem's period of initial publication.
        :param category: the book's category (i.e. fiction).
        :param _type: the book's type.
        :return: the response.
        """

        book = {
            "authorId": author_id,
            "title": title,
            "publicationYear": publication_year,
            "publicationStmt": publication_stmt,
            "sourceDesc": source_desc,
            "period": period,
            "category": category,
            "type": _type
        }

        request = Request(BASE_URL + 'add',
                          data=bytes(json.dumps(book), encoding=ENCODING),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def modify(self, _id, author_id, title, publication_year, publication_stmt,
               source_desc, period, category, _type):
        """
        :param _id: the book's database id.
        :param author_id: an author's db id.
        :param title: the poem's title.
        :param publication_year: poem's year of publication (if known).
        :param publication_stmt: copyrighted or public domain.
        :param source_desc: MLA citation of poem's source.
        :param period: poem's period of initial publication.
        :param category: the book's category (i.e. fiction).
        :param _type: the book's type.
        :return: the response.
        """

        book = {
            "id": _id,
            "authorId": author_id,
            "title": title,
            "publicationYear": publication_year,
            "publicationStmt": publication_stmt,
            "sourceDesc": source_desc,
            "period": period,
            "category": category,
            "type": _type
        }

        request = Request(BASE_URL + 'modify',
                          data=bytes(json.dumps(book), encoding=ENCODING),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)

    def delete(self, _id):
        """
        :param _id: the id of the book to delete.
        :return: the response.
        """

        request = Request(BASE_URL + 'delete/' + str(_id),
                          headers=self.headers)
        response = urlopen(request)
        return json.load(response)
