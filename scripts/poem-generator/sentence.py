import spacy
import nltk
import random
from word import Word
from nltk.corpus import brown
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('brown')

class Sentence:
    POPULATION = 10
    SENTENCE_STRUCTS = ["Simple", "Compound", "Complex", "Compound-Complex"]
    IND_CLAUSE_STRUCTS = {
        # PPS and AT best for first
        1 : ["PPS", "VB", "NNS"],
        2 : ["AT", "JJ", "NN", "VBZ", "RB"],
        #3 : ["NN", "VBZ", "NN"],
        3: ["AT", "NN", "WDT", "VBZ", "CC", "VBZ", "CC", "AT", "NN"],
        4 : ["NNS", "RB", "VB", "NN"],
        5 : ["MD", "PRP", "RB", "VB", "AT", "NN", "AT", "NNS"],
        6 : ["AT", "NN", "AT", "NN", "AT", "JJ", "NN"],
        7 : ["CC", "NNS", "PR", "AT", "NN", "PRP", "VB", "VBZ", "RB", "CC", "JJ", "VBZ", "RB", "AT", "NN"],
        8 : ["WP", "VBD", "CC", "VBD", "VBG", "IN", "AT", "NM"]
    }
    DEP_CLAUSE_STRUCTS = {
        1 : ["WDT", "PRP", "VBP", "VBZ", "JJ"],
        2 : ["IN", "DT", "NN", "WDT", "PRP", "VBD"],
        3 : ["IN", "PRP", "VBP", "RB"]
    }
    # to add more later

    def __init__(self, pattern_key, secret_letter, theme):
        self.word_list = []
        self.pattern_key = pattern_key
        self.secret_letter = secret_letter
        self.theme = theme
        self.relevant_words = brown.tagged_words()

        # self.sentence_struct = random.choice(self.SENTENCE_STRUCTS)
        self.sentence_struct = "Simple"

    def generate_sentence(self):
        nlp = spacy.load("en_core_web_sm")
        # relevant_category_words = brown.tagged_words()

        # for tag in relevant_category_words:
        #     if tag[1] == "NNS":
        #         prp.append(tag)
        # print(prp)

        # Create independent clause
        # If more complex, create more ind and or dep clauses, string them together
        if self.sentence_struct == "Simple":
            self.create_simple(self.relevant_words)

        elif self.sentence_struct == "Compound":
            self.create_compound(self.relevant_words)

        elif self.sentence_struct == "Complex":
            self.create_complex(self.relevant_words)
        
        elif self.sentence_struct == "Compound-Complex":
            self.create_compound_complex(self.relevant_words)

    def get_random_word_by_tag(self, words, tag):
        bag_of_words = set()
        for item in words:
            if item[1] == tag:
                bag_of_words.add(item)
        return random.choice(list(bag_of_words))

    def create_simple(self, relevant_words):
        ind_clause = self.generate_independent_clause(relevant_words, True)
        self.create_word_list(ind_clause)
    
    def create_compound(self, relevant_words):
        final = []
        compound_connectors = ["CC", "RB", "RBR", "RBS"]
        connector_choice = [self.get_random_word_by_tag(relevant_words, random.choice(compound_connectors))]
        ind_clause_1 = self.generate_independent_clause(relevant_words, True)
        ind_clause_2 = self.generate_independent_clause(relevant_words, False)
        
        final += ind_clause_1
        final += connector_choice
        final += ind_clause_2
        print(connector_choice)
        print(final)
        self.create_word_list(final)
    
    def create_complex(self, relevant_words):
        return
    
    def create_compound_complex(self, relevant_words):
        return


    def create_word_list(self, clause):
        example = []
        for item in clause:
            new_word = Word(item[0].lower(), item[1])
            self.word_list.append(new_word)
            example.append(item[0].lower())
        example_str = " ".join(example)
        print(example_str.capitalize())
    
    def generate_independent_clause(self, relevant_words, is_first):
        # Check if it contains first letter of sentence
        struct_list = [1, 2, 3, 4, 5, 6, 7, 8]
        clause_choice = random.choice(struct_list)
        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        clause_index = 0
        clause = []

        while len(clause) < len(clause_struct):
            if is_first:
                set_empty = False
                possible_firsts = set()
                while set_empty == False:
                    for tag_word in relevant_words:
                        word = tag_word[0].lower()
                        if word[0] == self.secret_letter:
                        # if word.isalpha() or word.isalnum():
                            if tag_word[1] == clause_struct[clause_index]:
                                possible_firsts.add(tag_word)
                    if len(possible_firsts) != 0:
                        set_empty = True
                    else:
                        struct_list.remove(clause_choice)
                        clause_choice = random.choice(struct_list)
                        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                clause.append(random.choice(list(possible_firsts)))
                clause_index += 1
                is_first = False

            set_empty = False
            struct_tag_words = set()
            while set_empty == False:
                for tag_word in relevant_words:
                    if tag_word[1] == clause_struct[clause_index]:
                        struct_tag_words.add(tag_word)
                if len(struct_tag_words) != 0:
                    set_empty = True
                else:
                    struct_list.remove(clause_choice)
                    clause_choice = random.choice(struct_list)
                    clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                    clause_index = 0
                    clause = []
                    is_first = True
                    break
            if set_empty:
                clause.append(random.choice(list(struct_tag_words)))
                clause_index += 1
            # print(clause)
        # print("final: ", clause)
        return clause

    def generate_dependent_clause(self, relevant_words, is_first):
        return

    def generate_word_pairs(self, tag_type):
        return



    # Baseline sentence check fitness
    def check_proper_sentence(self, sentence, nlp):
        text = nlp(sentence)

        try:
            if text.sents and len(list(text.sents) == 1):
                return
        except:
            return -1
    

def test():
    test = Sentence("ABA", "r", "romance")
    
    for x in test.relevant_words:
        print(x)


