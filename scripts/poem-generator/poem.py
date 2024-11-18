import random

class Poem:
    POSSIBLE_TOPICS = "love", "pain", "youth", "generation", "creative"

    def __init__(self):
        self.secret = ""
        self.key_narrative_elems = []
        self.pattern = ""
        self.num_sentences = 0
        self.sentences = []
        
        self.generate_topic()
        self.generate_pattern()
    
    def generate_topic(self):
        self.secret = random.choice(self.POSSIBLE_TOPICS)
        self.num_sentences = len(self.secret)
        self.generate_narrative_elems()

    def generate_narrative_elems(self):
        

    def generate_pattern(self):
        possible_patterns = ["A", "B", "C", "D", "E"] # to be expanded
        poem_pattern = ""
        for i in range(0, self.num_sentences):
            pattern = random.choice(possible_patterns)
            poem_pattern += pattern
        self.pattern = poem_pattern

    
        

def test():
    test = Poem()

    print(test.pattern)

test()