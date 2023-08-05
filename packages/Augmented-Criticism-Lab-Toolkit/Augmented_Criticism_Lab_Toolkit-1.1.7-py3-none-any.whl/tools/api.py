"""Connectors for API based tools hosted on the ACL
:author Josh Harkema
"""
import json
from urllib.request import urlopen, Request

BASE_URL = "https://api.acriticismlab.org/tools/"
ENCODING = "utf8"


class Tools:
    """Class handles all POST type connections to the ACL toolkit."""

    @staticmethod
    def lemmatize(text):
        """
        :param text: the text to run through the lemmatizer.
        :return: a parsed json object of the response.
        """
        text = {"text": text}
        request = Request(BASE_URL + "text/lemmatize",
                          data=bytes(json.dumps(text), encoding=ENCODING))
        request.add_header("Content-Type", "application/json")
        response = urlopen(request)
        return json.load(response)

    @staticmethod
    def pos_tag(text):
        """
        :param text: the text to run through the pos tagger.
        :return: a parsed json object of the response.
        """
        text = {"text": text}
        request = Request(BASE_URL + "text/simple_tagger",
                          data=bytes(json.dumps(text), encoding=ENCODING))
        request.add_header("Content-Type", "application/json")
        response = urlopen(request)
        return json.load(response)

    @staticmethod
    def topic_model(text, number_of_topics=20):
        """
        :param text: the text to run through the topic modeler.
        :param number_of_topics: the number of topics to return.
        :return: a parsed json object of the response.
        """
        text = {
            "text": text,
            "numberOfTopics": number_of_topics
        }
        request = Request(BASE_URL + "text/topic_model",
                          data=bytes(json.dumps(text), encoding=ENCODING))
        request.add_header("Content-Type", "application/json")
        response = urlopen(request)
        return json.load(response)
