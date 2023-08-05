"""Class to count the number of syllables in a word or a poem from the ACL
database.
:author Josh Harkema
"""
import csv
import os
import string

# Load the outliers file from the module path.
package_directory = os.path.dirname(os.path.abspath(__file__))
OUTLIERS_FILENAME = os.path.join(package_directory, 'OUTLIERS.csv')

PUNCTUATION_TRANSLATOR = str.maketrans('', '', string.punctuation)

VOWELS = ["a", "e", "i", "o", "u", "y"]

CONSONANTS = [
    "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r",
    "s", "t", "v", "w", "x", "z"
]

DISYLLABIC_COMBINATIONS = [
    "ea", "ii", "io", "ua", "uo"
]

TWO_LETTER_IGNORED_SUFFIXES = [
    "es"
]

TWO_LETTER_ONE_SYL_SUFFIXES = [
    "éd"
]

THREE_LETTER_ONE_SYL_SUFFIXES = [
    "ion", "ely", "ful", "ead"
]

THREE_LETTER_TWO_SYL_SUFFIXES = [
    "ier", "ial", "ium", "ism"
]

FOUR_LETTER_ONE_SYL_SUFFIXES = [
    "less", "ious", "aire", "ions", "eace"
]

FOUR_LETTER_TWO_SYL_SUFFIXES = [
    "able", "ally", "eace", "eful", "iful", "iums"
]

FIVE_LETTER_ONE_SYL_SUFFIXES = [
    "reign", "esque", "neath"
]

FIVE_LETTER_TWO_SYL_SUFFIXES = [
    "ion’s"
]

SIX_LETTER_TWO_SYL_SUFFIXES = [
    "liness"
]

ES_ENDING_FOUR_LETTER_IGNORED = [
    'thes'
]

ES_ENDING_FOUR_LETTER_SINGLE_SYL = [
    'ines', 'ates', 'oves', "ides", 'opes', 'ones', 'ties', 'ches'
]

END_TRIPLES = [
    'eed', 'ied'
]

OUTLIERS = {
}

SINGLE_SYLLABLE = [
    "ere", "lea", "ear", "qua", "qui", "ease", "hea", "rea"
]

DOUBLE_SYLLABLE = [
    "semi", "homo"
]


class SyllableCounter:
    counts = []

    def __init__(self):
        self.load_outliers()

    @staticmethod
    def ed_endings(word, count):
        """
        Deals with the convoluted logic that is the English "ed" ending.
        :param word: the word to test.
        :param count: the current count.
        :return: the word sans a 4 / 2 letter slice off the end, and a count + 1
        or count depending on the logic below.
        """
        end_slice = word[-4:]

        if end_slice[-3:] in END_TRIPLES:
            return word[:-3], count + 1

        if end_slice == "rred":
            return word[:-4], count

        if end_slice[-3] == "r":
            if end_slice[-4] in CONSONANTS or \
                    end_slice[-4] in VOWELS and end_slice[-4] != "r":
                if end_slice[-4] == 'e' or 'u':
                    return word[:-4], count + 1
                return word[:-2], count + 1
        if end_slice[-3] == "l":
            if end_slice[-4] in CONSONANTS or \
                    end_slice[-4] in VOWELS and end_slice[-4] != "l":
                return word[:-2], count + 1
        if end_slice[-3] == "t":
            return word[:-3], count + 1
        if end_slice[-3] == "d":
            return word[:-3], count + 1

        return word[:-2], count

    @staticmethod
    def es_endings(word, count):
        """
        Logic for dealing with words that end in 'es'.
        :param word: the word with an es ending to count.
        :param count: the current count.
        :return: a chopped down word with a variable count (see logic).
        """
        if word[-4:] in ES_ENDING_FOUR_LETTER_IGNORED:
            word = word[:-4]
        elif word[-4:] in ES_ENDING_FOUR_LETTER_SINGLE_SYL:
            word = word[:-4]
            count += 1
        elif word[-3] == 'l' and word[-4] in VOWELS:
            word = word[:-4]
            count += count + 1
        elif word[-3] in CONSONANTS or word[-3] == 'e':
            word = word[:-2]
            count += 1
        elif word[-3] == 'o':
            word = word[:-3]
            count += 1
        else:
            word = word[:-2]

        return word, count

    @staticmethod
    def ness_endings(word, count):
        """
        Logic for dealing with words that end in 'ness'.
        :param word: the word with a 'ness' ending.
        :param count: the current syl count.
        :return: updated word and syl count.
        """
        if word[-8:] == "iousness":
            word = word[:-8]
            count += 2

        if word[-6:] == "liness":
            word = word[:-6]
            count += 2

        if word[-4:] == "ness":
            word = word[:-4]
            count += 1

        return word, count

    def count_syllables_by_line(self, line):
        """
        Counts syllables in pre-formatted lines of arbitrary text.
        :param line: a string of text.
        :return: the number of syllables in the text.
        """
        syllable_count = 0
        line = line.replace("-", " ")
        line = line.replace("—", " ")
        line = line.strip().translate(PUNCTUATION_TRANSLATOR)
        if line == "":
            return syllable_count
        for word in line.split(" "):
            syllable_count += self.count_syllables_word(word)

        return syllable_count

    def count_syllables_poem(self, poem):
        """
        This is just a timing and formatting method for counting syllables from
        poems in the ACL database. It keeps the string formatting logic out
        of the syllable counter actual.
        :param poem: the poem to run a syllable count on.
        :return: a string of the poem's details formatted with the syllable
        counts.
        """
        output_string = "Title: " + poem['title'] + "\n"
        output_string += "Id: " + str(poem['id']) + "\n"
        output_string += "Author: " + poem['first_name'] + " " + \
                         poem['last_name'] + "\n"

        for line in poem['text'].split('\\n'):
            syllable_count = 0
            line = line.replace("-", " ")
            line = line.replace("—", " ")
            line = line.strip().translate(PUNCTUATION_TRANSLATOR)
            if line == "":
                return output_string
            output_string += "\t"
            for word in line.split(" "):
                count = self.count_syllables_word(word)
                if count is not None:
                    output_string += word + "(" + str(count) + ") "
                    syllable_count += count

            self.counts.append(syllable_count)
            output_string += "--" + str(syllable_count) + "\n"

        return output_string

    def count_syllables_word(self, word, count=0):
        """
        This demonic recursive script is used to count syllables in words.

        :param word: the word to count syllables of.
        :param count: the syllable count.
        :return: the count as an int.
        """
        # print(count, word)
        word = word.lower()

        # Catch the end of the recursion and return the count.
        if len(word) == 0:
            return count

        if word in OUTLIERS:
            return OUTLIERS[word]

        # Handle rules that can only run on the first pass.
        if count == 0:
            # count words with fewer than 4 letters as one syllable.
            if len(word) < 4:
                return count + 1

            # Catches a lot of metrical contractions.
            if '’' in word and word[-2:] != "’s":
                return self.count_syllables_word(word, count - 1)

            # ALL THIS DEALS WITH SUFFIXES.
            if word[-4:] == 'ness':
                word, count = self.ness_endings(word, count)
                return self.count_syllables_word(word, count)

            if word[-2:] == 'ed':
                word, count = self.ed_endings(word, count)
                if len(word) == 0:
                    return count

            if word[-2:] == 'le':
                if word[-3] not in VOWELS:
                    return self.count_syllables_word(word[:-3], count + 1)
                else:
                    return self.count_syllables_word(word[:-2], count)

            if word[-2:] == 'es':
                word, count = self.es_endings(word, count)
                return self.count_syllables_word(word, count)

            if word[-3:] == 'est':
                return self.count_syllables_word(word[:-3], count + 1)

            if word[-2:] in TWO_LETTER_IGNORED_SUFFIXES and \
                    word[-3] != 'l':
                return self.count_syllables_word(word[:-2], count)

            if word[-2:] in TWO_LETTER_ONE_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-2], count + 1)

            if word[-3:] in THREE_LETTER_ONE_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-3], count + 1)

            if word[-3:] in THREE_LETTER_TWO_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-3], count + 2)

            if word[-4:] in FOUR_LETTER_ONE_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-4], count + 1)

            if word[-4:] in FOUR_LETTER_TWO_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-4], count + 2)

            if word[-5:] in FIVE_LETTER_ONE_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-5], count + 1)

            if word[-5:] in FIVE_LETTER_TWO_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-5], count + 2)

            if word[-6:] in SIX_LETTER_TWO_SYL_SUFFIXES:
                return self.count_syllables_word(word[:-6], count + 2)

        # If the last letter is an e, don't count it.
        if len(word) == 1 and word == "e":
            return count

        # This catches weird four letter, single syllable combos.
        if word[:4] in SINGLE_SYLLABLE:
            return self.count_syllables_word(word[4:], count + 1)

        # This catches weird three letter, single syllable combos.
        if word[:3] in SINGLE_SYLLABLE:
            return self.count_syllables_word(word[3:], count + 1)

        if word[:4] in DOUBLE_SYLLABLE:
            return self.count_syllables_word(word[4:], count + 2)

        # If the first letter is a vowel.
        if word[0] in VOWELS:
            # If the first two letters are a disyllabic combination count two.
            if word[0:2] in DISYLLABIC_COMBINATIONS:
                return self.count_syllables_word(word[2:], count + 2)

            # This strips out 2+ letter vowel groupings and counts them as one.
            counter = 0
            while counter < len(word):
                # print(counter, len(word), word[counter])
                if counter == len(word) - 1 and word[counter] in VOWELS:
                    return count + 1
                if word[counter] in VOWELS:
                    counter += 1
                else:
                    return self.count_syllables_word(word[counter + 1:],
                                                     count + 1)

            return self.count_syllables_word(word[1:], count + 1)

        # If the first letter is a consonant, remove it and add nothing to the
        # count.
        else:
            return self.count_syllables_word(word[1:], count)

    @staticmethod
    def load_outliers():
        """
        Loads OUTLIERS.csv into OUTLIERS dict.

        :return: nothing, writes to object and file.
        """
        with open(OUTLIERS_FILENAME, newline='') as f:
            raw_csv = csv.reader(f, delimiter=',')
            sorted_csv = sorted(raw_csv, key=lambda _row: _row[0])
            with open(OUTLIERS_FILENAME, newline='', mode='w') as w:
                csv_writer = csv.writer(w, delimiter=',')
                for row in sorted_csv:
                    csv_writer.writerow(row)
                    OUTLIERS[row[0]] = int(row[1])
