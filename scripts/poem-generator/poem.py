import random
from domain_link import Domain
from sentence import Sentence
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import words

class Poem:
    POSSIBLE_TOPICS = "romance", ""

    def __init__(self):
        self.secret = "think"
        self.key_narrative_elems = []
        self.pattern = ""
        self.num_sentences = 0
        self.sentences = []
        
        self.generate_topic()
        self.generate_pattern()
        print(self.num_sentences)
        print(self.pattern)


        for i in range(0, len(self.secret)):
            sent = Sentence(self.pattern[i], self.secret[i], self.secret)
            new_sentence = sent.generate_sentence()
    
    def generate_topic(self):
        # self.secret = random.choice(self.POSSIBLE_TOPICS)
        self.num_sentences = len(self.secret)
        # self.generate_narrative_elems(self.secret)

    def generate_narrative_elems(self, topic):
        print(topic)
        domain = Domain(topic)
        word_list = words.words('en')
        self.key_narrative_elems = self.create_tuple_list(word_list)

    def generate_pattern(self):
        possible_patterns = ["A", "B", "C", "D", "E"] # to be expanded
        poem_pattern = ""
        for i in range(0, self.num_sentences):
            pattern = random.choice(possible_patterns)
            poem_pattern += pattern
        self.pattern = poem_pattern

    def create_tuple_list(self, list):
        tuple_list = []
        for word in list:
            token = word_tokenize(word)
            tag = pos_tag(token)
            tuple = (word, tag)
            tuple_list.append(tuple)
        return tuple_list
    
    def generate_to_string(self, word_list):
        example_str = " ".join(word_list)
        return example_str.capitalize()

def test():
    test = Poem()

    # for sentence in test.sentences:
    #     print(test.generate_to_string(sentence))

test()