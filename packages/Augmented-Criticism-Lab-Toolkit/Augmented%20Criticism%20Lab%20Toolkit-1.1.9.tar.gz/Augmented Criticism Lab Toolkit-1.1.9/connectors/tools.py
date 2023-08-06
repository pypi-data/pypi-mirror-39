"""Common functions for connectors.
:author Josh Harkema
"""


def replace_spaces(text):
    """
    Replaces all the spaces in a string with underscores.
    :param text: the text to replace.
    :return: an replaced string.
    """
    return text.replace(" ", "_")
