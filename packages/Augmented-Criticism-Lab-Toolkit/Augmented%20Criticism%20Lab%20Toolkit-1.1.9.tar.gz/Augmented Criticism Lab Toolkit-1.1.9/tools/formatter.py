""" Helper class with methods for dealing with text.
:author Josh Harkema
"""
import os
import string

# Load the outliers file from the module path.
package_directory = os.path.dirname(os.path.abspath(__file__))
STOP_WORDS_FILENAME = os.path.join(package_directory, 'STOPWORDS.txt')
PUNCTUATION_TRANSLATOR = str.maketrans('', '', string.punctuation)


class Formatter:
    """ Deals with text formatting misc tasks (tokenizing, removing stop words,
    etc.)
    """
    stop_words = []

    def __init__(self):
        if len(self.stop_words) == 0:
            with open(STOP_WORDS_FILENAME, "r") as f:
                for line in f:
                    self.stop_words.append(line.strip().lower())

    @staticmethod
    def array_to_string(text_array):
        """ Converts a list of strings into a single string.
        :param text_array: the array to convert to a string.
        :return: a string.
        """
        out = ""
        for line in text_array:
            out += line.strip()
            out += " "

        return out

    @staticmethod
    def string_to_array(text, delimiter='\\n'):
        """ Converts a string to an array of string.
        :param text: the text to convert to an array.
        :param delimiter: the character marking where to split the string.
        :return: an array.
        """
        return text.split(delimiter)

    @staticmethod
    def tokenize_words(text, remove_punctuation=True, lower_case=True):
        """ Tokenize a string into an array of word tokens.
        :param text: the text to tokenize.
        :param remove_punctuation: should all punctuation be removed?
        :param lower_case: should all chars be converted to lower case?
        :return: an array of tokens.
        """
        tokens = []
        if remove_punctuation:
            text = text.replace("-", " ")
            text = text.replace("—", " ")
            text = text.replace("\n", " ")
            text = text.translate(PUNCTUATION_TRANSLATOR)

        for word in text.split(" "):
            if lower_case:
                word = word.lower()
            tokens.append(word)

        return tokens

    @staticmethod
    def tokenize_lines(text, delimiter='\\n', remove_punctuation=True):
        """ Tokenize a string into an array of line tokens.
        :param text: the text to tokenize.
        :param delimiter: the character marking the end of each line.
        :param remove_punctuation: should all punctuation be removed.
        :return: an array of tokens.
        """
        tokens = []
        if remove_punctuation:
            text = text.replace("-", " ")
            text = text.replace("—", " ")
            text = text.strip().translate(PUNCTUATION_TRANSLATOR)

        for line in text.split(delimiter):
            tokens.append(line)

        return tokens

    def remove_stop_words(self, word_tokens):
        """
        :param word_tokens: list of word tokens to filter.
        :return: a list of word tokens with the stop words removed.
        """
        filtered_list = []
        for word in word_tokens:
            word = word.strip().lower()
            if word not in self.stop_words:
                filtered_list.append(word)
        return filtered_list

    def add_words_to_stop_words(self, words):
        """ Add custom words to list of stop words.
        :param words: an array of words.
        :return: nothing.
        """
        for word in words:
            self.stop_words.append(word.strip().lower())

    def add_word_to_stop_words(self, word):
        """ Add single word to list of stop words.
        :param word: the words to add.
        :return: nothing.
        """
        self.stop_words.append(word)

    def del_words_from_stop_words(self, words):
        """ Remove words from the list of stop words.
        :param words: an array of words.
        :return: nothing.
        """
        self.stop_words = list(
            filter(lambda word: word not in words, self.stop_words))

    def print_stop_words(self):
        """
        :return: prints the list of stop words to console.
        """
        print(self.stop_words)
