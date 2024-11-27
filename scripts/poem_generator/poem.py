"""
CSCI 3725 Computational Creativity
M7 Poetry Slam

This file contains the Poem class that calls to generate a poem by randomly
intializing a topic (secret word) for the acrostic poem and a pattern rhyme
scheme for the poem to follow. The initialized secret word constrains the
number of sentences to generate as well as its first letter in each sentence.
Poem continues to call on the Sentence class until the total number of
sentences to be generated has been fulfilled. The file also allows for
the Flask app in __init__.py to interact with the class functions and local
testing within the python file.

Authors: Lily Huynh
Last Updated: November 26, 2024

Bugs:
- Currently does not generate key narrative elements since the domain_link.py
  is currently not being used within sentence generation
- No evaluation function has been implemented at the time of last update so
  sentences can not be evaluated on if it is on theme or not yet
"""

import random
from poem_generator.sentence import Sentence

class Poem:
    """
    Poem represents the list of sentences, rhyme pattern scheme, random
    secret word chosen to create the acrostic poem, and more.
    """
    POSSIBLE_TOPICS = "love", "time"

    def __init__(self):
        self.secret = ""
        self.key_narrative_elems = []
        self.pattern = ""
        self.num_sentences = 0
        self.sentences = []
        self.pattern_dict = {}
        self.generate_topic()
        self.generate_pattern()

        print(f"Number of sentences to be generated: {self.num_sentences}")
        print(f"Generated pattern: {self.pattern}")

        for i in range(0, self.num_sentences):
            gen_sentence = ""
            
            # If first sentence in list or first rhyme pattern seen
            if i == 0 or len(self.pattern_dict[self.pattern[i]]) == 0:
                gen_sentence = Sentence(self.secret[i], self.secret, "")
            else:
                random_rhyme = self.pattern_dict[self.pattern[i]]
                print(f"Matching rhyme! {random_rhyme}")
                gen_sentence = Sentence(self.secret[i],
                                        self.secret,
                                        random.choice(random_rhyme))
                
            # Generates and cleans the generated sentence
            gen_sentence.generate_sentence()
            gen_sentence.clean_sentence()
            
            # Append to sentence list and save last word to rhyme dictionary
            self.sentences.append(str(gen_sentence))
            last_word = str(gen_sentence).split(" ")[-1]
            self.update_pattern_dict(self.pattern[i], last_word)

    def generate_topic(self):
        """Chooses a random topic for secret word and updates number of sentences
        to be generated in poem based on secret word length"""
        self.secret = random.choice(self.POSSIBLE_TOPICS)
        self.num_sentences = len(self.secret)

    def generate_pattern(self):
        """Generates a random rhyme scheme pattern"""
        possible_patterns = ["A", "B", "C"]
        poem_pattern = ""
        for i in range(0, self.num_sentences):
            pattern = random.choice(possible_patterns)
            poem_pattern += pattern
        self.pattern = poem_pattern
    
    def generate_to_string(self, word_list):
        """Joins the given word list array and creates a string sentence"""
        example_str = " ".join(word_list)
        return example_str.capitalize()
    
    def update_pattern_dict(self, pattern_key, pattern_value):
        """Updates the pattern dictionary based on given pattern key (letter)
        and the word associated with that rhyme scheme"""
        if len(self.pattern_dict) == 0:
            for i in range(0, len(self.pattern)):
                self.pattern_dict[self.pattern[i]] = []
        self.pattern_dict[pattern_key].append(pattern_value)

    def jsonify_sentences(self):
        """Returns a dictionary version of the sentence list to create be
        converted into a json to be read by text-to-screen-and-speech.js"""
        sentence_dict = {}
        for i in range (0, self.num_sentences):
            sentence_dict[i] = self.sentences[i]
        return sentence_dict

def generate_poem():
    """Called in __init__.py to interact with poem.py"""
    return Poem()

def local_test():
    """Local testing of poem generation within Terminal (refer to
    README on detailed instructions of local testing)"""
    poem = Poem()
    for sentence in poem.sentences:
        print(poem.generate_to_string(sentence))

# local_test()