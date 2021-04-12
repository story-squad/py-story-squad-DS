

class TextModeration:
    """Class that filters content with self.check_words(word: str) against a
    list of known inappropriate words"""

    def __init__(self, wordlist_file: str):
        """Arguments:
        `wordlist_file` str - path to file containing flag words for
        filtering content"""
        self._words = self.open_words(wordlist_file)

    def open_words(self, file_name: str) -> set:
        """function that opens a .csv file containing one column of flag words
        returns a set of words to use in comparison method
        self.check_word(word: str)

        Arguments:
        `file_name` str - name of file containing flag words for filtering
        **Note** - at this time the only type/format of file supported is .csv with one column of flag words.

        Returns:
        `set` - unique tokenized words contained in open(`file_name`)"""

        with open(file_name, "rt") as word_file:
            data = set(word_file.read().split(",\n")[1:])
        return data

    def check_word(self, word: str) -> bool:
        """Function that checks membership of word in self._words set
        Arguments:
        `word` str - word in sample that is being checked for moderation

        Returns:
        bool: True if the word passed is a member of self._words set,
        otherwise False"""

        return word in self._words
