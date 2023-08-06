"""ACL database connector for books
:author Josh Harkema
"""
import json
from urllib.request import urlopen

from .tools import replace_spaces

BASE_URL = "https://api.acriticismlab.org/book/"


class Book:
    """Class handles all book related connections to the ACL database."""

    @staticmethod
    def by_id(_id):
        """
        Get a book by its database id.
        :param _id: the database id to retrieve.
        :return: a parsed json response of the book.
        """
        response = urlopen(BASE_URL + "get/" + str(_id))
        return json.load(response)

    @staticmethod
    def by_title(title):
        """
        Get a book by its title (must be an exact match.)
        :param title: the title of the book to find.
        :return: a parsed json response of the book if one is found.
        """
        title = replace_spaces(title)
        response = urlopen(BASE_URL + "get_by_title/" + str(title))
        return json.load(response)

    @staticmethod
    def all():
        """
        :return: a parsed json response with a list of books.
        """
        response = urlopen(BASE_URL + "get_all")
        return json.load(response)

    @staticmethod
    def all_simple():
        """
        :return: a parsed json list with the basic details of all books in the
        database.
        """
        response = urlopen(BASE_URL + "get_all_simple")
        return json.load(response)

    @staticmethod
    def get_characters(book_id):
        """
        :param book_id: the id of the book to get all characters from.
        :return: a parsed json list of the cast of characters in the book.
        """
        response = urlopen(BASE_URL + "get_characters/" + str(book_id))
        return json.load(response)
