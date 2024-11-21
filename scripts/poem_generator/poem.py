import random
# from domain_link import Domain
# from sentence import Sentence
from poem_generator.domain_link import Domain
from poem_generator.sentence import Sentence
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import words
import json

class Poem:
    POSSIBLE_TOPICS = "think", "love", "change", "real"

    def __init__(self):
        self.secret = ""
        self.key_narrative_elems = []
        self.pattern = ""
        self.num_sentences = 0
        self.sentences = []
        self.pattern_dict = {}
        
        self.generate_topic()
        self.generate_pattern()
        print(self.num_sentences)
        print(self.pattern)


        for i in range(0, len(self.secret)):
            sent = ""
            if i == 0 or len(self.pattern_dict[self.pattern[i]]) == 0:
                sent = Sentence(self.pattern[i], self.secret[i], self.secret, "")
            else:
                random_rhyme = self.pattern_dict[self.pattern[i]]
                print("matching pattern!", random_rhyme)
                sent = Sentence(self.pattern[i], self.secret[i], self.secret, random.choice(random_rhyme))
            sent.generate_sentence()
            
            self.sentences.append(str(sent))
            # print(sent)
            last_word = str(sent).split(" ")[-1]
            self.update_pattern_dict(self.pattern[i], last_word)

    
    def generate_topic(self):
        self.secret = random.choice(self.POSSIBLE_TOPICS)
        self.num_sentences = len(self.secret)
        # self.generate_narrative_elems(self.secret)

    def generate_narrative_elems(self, topic):
        print(topic)
        domain = Domain(topic)
        word_list = words.words('en')
        self.key_narrative_elems = self.create_tuple_list(word_list)

    def generate_pattern(self):
        possible_patterns = ["A", "B", "C"] # to be expanded
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
    
    def update_pattern_dict(self, pattern_key, pattern_value):
        if len(self.pattern_dict) == 0:
            for i in range(0, len(self.pattern)):
                self.pattern_dict[self.pattern[i]] = []
        
        self.pattern_dict[pattern_key].append(pattern_value)

    def jsonify_sentences(self):
        sentence_dict = {}
        for i in range (0, self.num_sentences):
            sentence_dict[i] = self.sentences[i]
        return sentence_dict

def generate_poem():
    poem = Poem()
    for sentence in poem.sentences:
        print(sentence)
    return Poem()

def test():
    test = Poem()

    # for sentence in test.sentences:
    #     print(test.generate_to_string(sentence))
    for test in test.sentences:
        print(test)

# test()