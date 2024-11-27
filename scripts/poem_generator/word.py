"""
CSCI 3725 Computational Creativity
M7 Poetry Slam

This file consists of the Word class where it takes the given word value
and index of the word within the word list. Whenever a Word is initialized,
it also calls for its count_syllables() function to use spacy to count the
number syllables of the initialized word.

Authors: Lily Huynh
Last Updated: November 26, 2024

Bugs:
- No known bugs at the moment
"""

import spacy

class Word:
    """
    Word represents the word object when called upon. Word needs a word value
    and index within word list to be defined.
    """
    def __init__(self, word, index):
        self.word = word
        self.num_syllables = self.count_syllables()
        self.index = index

    def count_syllables(self):
        """Uses spacy and tokenizes the word value to count its number of
        syllables. If spacy is unable to count its syllables, it returns 0."""
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("syllables", after="tagger")
        assert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser",
                                  "attribute_ruler", "lemmatizer", "ner"]
        word = nlp(self.word)
        try:
            syllables = [token._.syllables for token in word]
            syllables = syllables[0]
            return len(syllables)
        except:
            return 0

    def __str__(self):
        """Returns a string representation of only the word value."""
        return f"{self.word}"
    
    def __repr__(self):
        """Returns an unambiguous representation of the Word."""
        return f"Word('{self.word}', '{self.index}')"