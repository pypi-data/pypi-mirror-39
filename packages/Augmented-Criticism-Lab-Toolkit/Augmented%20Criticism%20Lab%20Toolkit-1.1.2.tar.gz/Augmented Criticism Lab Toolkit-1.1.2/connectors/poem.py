"""ACL database connector for poems
:author Josh Harkema
"""
import json
from urllib.request import urlopen

from .tools import replace_spaces

BASE_URL = "https://api.acriticismlab.org/poems/"


class Poem:
    """Class handles connections for all poem related endpoints for the ACL
    database.
    """

    @staticmethod
    def by_id(_id):
        """
        Get a specific poem by its database ID.
        :param _id: the id of the poem.
        :return: a parsed json response of the poem.
        """
        response = urlopen(BASE_URL + "by_id/" + str(_id))
        return json.load(response)

    @staticmethod
    def by_ids(_ids):
        """
        Returns a list of poems by their database ID.
        :param _ids: a comma-separated list of poem IDs.
        :return: a parsed json response of the poem.
        """
        response = urlopen(BASE_URL + "by_ids/" + str(_ids))
        return json.load(response)

    @staticmethod
    def all():
        """
        Get all poems in the database.
        :return: a parsed json response with a list of results.
        """
        response = urlopen(BASE_URL + "all")
        return json.load(response)

    @staticmethod
    def by_form(form):
        """
        Gets all poems matching a specific form (i.e. 'sonnet')
        :param form: the form to get.
        :return: a parsed json response with a list of results.
        """
        form = replace_spaces(form)
        response = urlopen(BASE_URL + "by_form/" + form)
        return json.load(response)

    @staticmethod
    def by_author_last_name(last_name):
        """
        Gets all poems by a specific author.
        :param last_name: the author's last name.
        :return: a parsed json response with a list of results.
        """
        last_name = replace_spaces(last_name)
        response = urlopen(BASE_URL + "search/by_last_name/" + last_name)
        return json.load(response)
