"""ACL database connector for book sections
:author Josh Harkema
"""
import json
from urllib.request import urlopen

from .tools import replace_spaces

BASE_URL = "https://api.acriticismlab.org/section/"


class Section:
    """Class handles all book based connections to the ACL database."""

    @staticmethod
    def by_id(_id):
        """
        :param _id: the database id of the desired section.
        :return: a parsed json object of the book.
        """
        response = urlopen(BASE_URL + "get/" + str(_id))
        return json.load(response)

    @staticmethod
    def all():
        """
        :return: a parsed json list of all sections in the database.
        """
        response = urlopen(BASE_URL + "get_all")
        return json.load(response)

    @staticmethod
    def all_from_book(book_id):
        """
        :param book_id: the database id of the book to get all sections from.
        :return: a parsed json list of all sections contained in the book.
        """
        response = urlopen(BASE_URL + "from_book/" + str(book_id))
        return json.load(response)

    @staticmethod
    def all_from_book_simple(book_id):
        """
        :param book_id: the database id of the book to get all sections from.
        :return: a parsed json list of the basic details of all sections from
        the book.
        """
        response = urlopen(BASE_URL + "from_book_simple/" + str(book_id))
        return json.load(response)

    @staticmethod
    def by_author_last_name(last_name):
        """
        :param last_name: the author last name to search for.
        :return: a parsed json list of all book sections by the author (if any
        exist)
        """
        last_name = replace_spaces(last_name)
        response = urlopen(BASE_URL + "search/by_last_name/" + last_name)
        return json.load(response)
