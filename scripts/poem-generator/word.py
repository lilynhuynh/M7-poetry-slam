import spacy
from spacy_syllables import SpacySyllables
from spacy.cli import download

import pronouncing

class Word:
    def __init__(self, word, tag):
        self.word = word
        self.tag = tag
        self.num_syllables = 0
        self.syllable_stress = []
        self.count_syllables()

    def count_syllables(self):
        # download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("syllables", after="tagger")
        assert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser",
                                  "attribute_ruler", "lemmatizer", "ner"]
        word = nlp(self.word)
        syllables = [token._.syllables for token in word]
        syllables = syllables[0]
        self.num_syllables = len(syllables)

        # pronunciation = pronouncing.phones_for_word(self.word)
        # stresses = pronouncing.stresses(pronunciation[0])
        # # 1 = stressed, 0 = unstressed
        # for i in range(0, len(syllables)):
        #     syllable_list = [syllables[i], stresses[i]]
        #     self.syllable_stress.append(syllable_list)

# def test():
#     testword = Word("beautiful", False)

#     print(testword.num_syllables)
#     print(testword.syllable_stress)

# test()