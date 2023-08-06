"""Class uses the pronouncing library to detect rhymes in lines of poetry.
:author Josh Harkema
"""
import string

import pronouncing


class Rhyme:
    end_words = []
    PUNCTUATION_TRANSLATOR = str.maketrans('', '', string.punctuation)

    def __init__(self, text, delimiter='\\n'):
        """
        :param text: a single poem from the ACL database API.
        """
        self.text = text
        self.delimiter = delimiter
        self.end_words = []
        self.strip_lines()

    def strip_lines(self):
        """
        Breaks text into lines, and strips out the end words into
        self.end_words.
        :return: nothing.
        """
        for line in self.text.split(self.delimiter):
            line = line.strip()
            last_word = line.split(" ")[-1]
            last_word = last_word.translate(self.PUNCTUATION_TRANSLATOR)
            last_word = last_word.strip()
            if last_word:
                self.end_words.append(last_word)

    def find_rhyme_scheme(self):
        """
        Iterates through self.end_words to find rhymes.
        :return: a list of the rhyme scheme detected.
        """
        current_line = 0
        current_letter = str("a")
        rhyme_scheme = ['x'] * len(self.end_words)

        while current_line < len(self.end_words) - 1:
            for j in range(current_line + 1, len(self.end_words)):
                if self.do_words_rhyme(self.end_words[current_line],
                                       self.end_words[j]):
                    if rhyme_scheme[current_line] == 'x':
                        rhyme_scheme[current_line] = current_letter
                        rhyme_scheme[j] = current_letter
                        current_letter = chr(ord(current_letter) + 1)
            current_line += 1

        return rhyme_scheme

    @staticmethod
    def do_words_rhyme(word1, word2):
        """
        Compares two words to see if they rhyme. Uses every possible
        pronunciation from the CMU dictionary to find matches. This makes it
        very likely that if words rhyme in any English dialect, this method
        will return True.

        :param word1: the root word.
        :param word2: the word for comparison.
        :return: true if words rhyme.
        """

        # Init as None to catch words without a phoneme match.
        phones_word1 = None
        phones_word2 = None

        # Get all possible pronunciations for each word and push them to
        # their respective phones_ array.
        if pronouncing.phones_for_word(word1):
            phones_word1 = pronouncing.phones_for_word(word1)
        if pronouncing.phones_for_word(word2):
            phones_word2 = pronouncing.phones_for_word(word2)

        if phones_word1 is not None and phones_word2 is not None:
            # First both words are placed into an array of possible matches
            # on the rhyming part of the word (i.e. the part after the last
            # stress.) The pronouncing package does most of the heavy lifting.
            possible_word1 = []
            possible_word2 = []
            for phones in phones_word1:
                possible_word1.append(pronouncing.rhyming_part(phones))
            for phones in phones_word2:
                possible_word2.append(pronouncing.rhyming_part(phones))

            for possible in possible_word1:
                if possible in possible_word2:
                    return True

        return False


def classify_sonnet(rhyme_scheme):
    p1 = 0
    p2 = 0
    p3 = 0
    sh = 0
    sp = 0

    if check_match(0, 3, rhyme_scheme):
        p1 += 0.14
        p2 += 0.14
        p3 += 0.14

    if check_match(1, 2, rhyme_scheme):
        p1 += 0.14
        p2 += 0.14
        p3 += 0.14

    if check_match(4, 7, rhyme_scheme):
        p1 += 0.14
        p2 += 0.14
        p3 += 0.14

    if check_match(5, 6, rhyme_scheme):
        p1 += 0.14
        p2 += 0.14
        p3 += 0.14

    if check_match(8, 10, rhyme_scheme):
        p1 += 0.14
        p3 += 0.14
        sh += 0.14
        sp += 0.14

    if check_match(9, 11, rhyme_scheme):
        p1 += 0.14
        sh += 0.14
        sp += 0.14

    if check_match(12, 13, rhyme_scheme):
        p1 += 0.14
        sh += 0.14
        sp += 0.14

    if check_match(8, 11, rhyme_scheme):
        p2 += 0.14
        p3 += 0.14

    if check_match(9, 12, rhyme_scheme):
        p2 += 0.14
        p3 += 0.14

    if check_match(10, 13, rhyme_scheme):
        p2 += 0.14
        p3 += 0.14

    if check_match(11, 13, rhyme_scheme):
        p3 += 0.14

    if check_match(0, 2, rhyme_scheme):
        sh += 0.14
        sp += 0.14

    if check_match(1, 3, rhyme_scheme):
        sh += 0.14
        sp += 0.14

    if check_match(4, 6, rhyme_scheme):
        sh += 0.14
        sp += 0.14

    if check_match(5, 7, rhyme_scheme):
        sh += 0.14
        sp += 0.14

    if rhyme_scheme[1] and rhyme_scheme[3] and rhyme_scheme[4] and \
            rhyme_scheme[6] != 'x':
        if rhyme_scheme[1] == rhyme_scheme[3] == rhyme_scheme[4] == \
                rhyme_scheme[6]:
            sp += 0.29

    if rhyme_scheme[5] and rhyme_scheme[7] and rhyme_scheme[8] and \
            rhyme_scheme[10] != 'x':
        if rhyme_scheme[5] == rhyme_scheme[7] == rhyme_scheme[8] == \
                rhyme_scheme[10]:
            sp += 0.29

    return p1, p2, p3, sh, sp


def check_match(first, second, rhyme_scheme):
    if rhyme_scheme[first] and rhyme_scheme[second] != 'x':
        if rhyme_scheme[first] == rhyme_scheme[second]:
            return True

    return False
