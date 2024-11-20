import spacy
import nltk
import random
from word import Word
from nltk.corpus import brown
import pronouncing
from collections import Counter
from nltk import ngrams
import string
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
        5 : ["MD", "PPSS", "RB", "VB", "AT", "NN", "AT", "NNS"],
        6 : ["AT", "NN", "AT", "NN", "AT", "JJ", "NN"],
        7 : ["CC", "NNS", "PR", "AT", "NN", "PPSS", "VB", "VBZ", "RB", "CC", "JJ", "VBZ", "RB", "AT", "NN"],
        8 : ["WP", "VBD", "CC", "VBD", "VBG", "IN", "AT", "NM"]
    }
    DEP_CLAUSE_STRUCTS = {
        1 : ["WDT", "PPSS", "VBP", "VBZ", "JJ"],
        2 : ["IN", "DT", "NN", "WDT", "PPSS", "VBD"],
        3 : ["IN", "PPSS", "VBP", "RB"]
    }
    # to add more later

    def __init__(self, pattern_key, secret_letter, theme, rhyme):
        self.word_list = []
        self.pattern_key = pattern_key
        self.secret_letter = secret_letter
        self.theme = theme
        self.relevant_words = brown.tagged_words(tagset="brown")
        self.rhyme = rhyme

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
        ind_clause = self.generate_independent_clause2(relevant_words, True)
        self.dummy_create_word_list(ind_clause)
        # self.create_word_list(ind_clause)

    def dummy_create_word_list(self, clause):
        for word in clause:
            new_word = Word(word, "")
            self.word_list.append(new_word)
    
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
        for item in clause:
            new_word = Word(item[0].lower(), item[1])
            self.word_list.append(new_word)
            
    
    def generate_independent_clause(self, relevant_words, is_first):
        generated = []
        # Check if it contains first letter of sentence
        struct_list = [1, 2, 3, 4, 5, 6, 7, 8]
        clause_choice = random.choice(struct_list)
        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        clause_index = 0
        clause = []

        possible_firsts = set()
        # relevant_word_pairs = set()

        while len(clause) < len(clause_struct):
            print("current clause", clause)
            if is_first:
                set_empty = False
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
                rhymes = []
                if clause_index == len(clause_struct)-1:
                    rhymes = pronouncing.rhymes(self.rhyme)

                for tag_word in self.find_word_pairs(clause[-1], clause_struct[clause_index], self.relevant_words):
                    if len(rhymes) != 0:
                        if tag_word[0] in rhymes:
                            struct_tag_words.add(tag_word)
                    else:
                        struct_tag_words.add(tag_word)
                print("relevant words:",len(struct_tag_words))
                if len(struct_tag_words) != 0:
                    set_empty = True

                # check if enough relevant struct words
                else:
                    # struct_list.remove(clause_choice)
                    # clause_choice = random.choice(struct_list)
                    # clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                    # if len(relevant_struct_words) <= 20:
                    #     break
                    # else:
                    #     relevant_struct_words.remove(clause[clause_index])

                    # relevant struct tags empty, want to go back one
                    clause_index -= 1
                    if clause_index == 0:
                        possible_firsts.remove(clause[clause_index])
                        clause.pop()
                        if len(possible_firsts) == 0:
                            struct_list.remove(clause_choice)
                            clause_choice = random.choice(struct_list)
                            clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                            is_first = True
                            print("no available firsts left, new struct")
                        else:
                            clause.append(random.choice(list(possible_firsts)))
                            print("new first", clause)
                            clause_index += 1
                    else:
                        clause.pop()
                break
            if set_empty:
                new_clause = clause.append(random.choice(list(struct_tag_words)))
                if new_clause not in generated:
                    clause_index += 1
                else:
                    clause_index -= 1
                    clause.pop()
            # print(clause)
        # print("final: ", clause)
        return clause
    
    def generate_independent_clause2(self, relevant_words, is_first):
        generated = []
        # Check if it contains first letter of sentence
        struct_list = [1, 2, 3, 4, 5, 6, 7, 8]
        clause_choice = random.choice(struct_list)
        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        clause_index = 0
        clause = []

        prev_relevant_ngram_words = []
        relevant_ngram_words = []

        possible_firsts = []
        # generate all possible first words in sentence

        end_sentence = False
        # relevant_word_pairs = set()

        while end_sentence == False: # change this
            print("current clause", clause)
            print("possible firsts:", len(possible_firsts))
            if is_first:
                set_empty = False
                while set_empty == False:
                    for tag_word in relevant_words:
                        word = tag_word[0].lower()
                        if word[0] == self.secret_letter:
                        # if word.isalpha() or word.isalnum():
                            if tag_word[1] == clause_struct[clause_index]:
                                possible_firsts.append(word)
                    if len(possible_firsts) != 0:
                        set_empty = True
                    else:
                        struct_list.remove(clause_choice)
                        clause_choice = random.choice(struct_list)
                        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                clause.append(random.choice(list(possible_firsts)))
                clause_index += 1
                is_first = False
            # generated list of possible first words
            clean_possible_first = set(possible_firsts)
            possible_firsts = list(clean_possible_first)

            while len(possible_firsts) != 0:
                print("clause", clause)
                relevant_ngram_words = self.find_n_gram_words(clause, self.relevant_words)
                # if relevant n grams empty, go back 1 or if first again, change first
                if len(relevant_ngram_words) == 0:
                    print("no relevant words")
                    clause_index -= 1

                    if len(clause_index) == 0:
                        # remove current first from possible first and from clause array
                        possible_firsts.remove(clause[clause_index])
                        print("no available after first, removed",clause[clause_index], len(possible_firsts))
                        clause.pop()
                        if len(possible_firsts) == 0: # if no more possible firsts, choose new struct
                            struct_list.remove(clause_choice)
                            clause_choice = random.choice(struct_list)
                            clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                            is_first = True
                            print("no available firsts left, new struct")
                        else: # choose a new possile first
                            clause.append(random.choice(list(possible_firsts)))
                            print("new first", clause)
                            clause_index += 1
                            break
                    else:
                        # if clause is not 1, remove current word from prev list
                        prev_relevant_ngram_words.remove(clause[clause_index])
                        # choose a random word from prev ngrams list
                        clause.append(random.choice(prev_relevant_ngram_words))
                        break
                
                # list of relevant words available
                print("List of relevant words available!")
                print("relevant ngrams", len(relevant_ngram_words))

                # choose random word from list of ngrams
                random_next_word = random.choice(relevant_ngram_words)
                prev_relevant_ngram_words = relevant_ngram_words

                print("NEW WORD:", random_next_word)
                if random_next_word in string.punctuation:
                    print("found punctuation", random_next_word)
                    end_sentence = True
                    break
                else:
                    clause.append(random_next_word)

                



        #     struct_tag_words = set()
        #     while set_empty == False:
        #         rhymes = []
        #         if clause_index == len(clause_struct)-1:
        #             rhymes = pronouncing.rhymes(self.rhyme)

        #         # look through possible words after next sentence
        #         for tag_word in self.find_n_gram_words(clause, self.relevant_words):
        #             if len(rhymes) != 0:
        #                 if tag_word[0] in rhymes:
        #                     struct_tag_words.add(word)
        #             else:
        #                 struct_tag_words.add(tag_word)
        #         print("relevant words:",len(struct_tag_words))
        #         if len(struct_tag_words) != 0:
        #             set_empty = True

        #         # check if enough relevant struct words
        #         else:
        #             # struct_list.remove(clause_choice)
        #             # clause_choice = random.choice(struct_list)
        #             # clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        #             # if len(relevant_struct_words) <= 20:
        #             #     break
        #             # else:
        #             #     relevant_struct_words.remove(clause[clause_index])

        #             # relevant struct tags empty, want to go back one
        #             clause_index -= 1
        #             if clause_index == 0:
        #                 possible_firsts.remove(clause[clause_index])
        #                 clause.pop()
        #                 if len(possible_firsts) == 0:
        #                     struct_list.remove(clause_choice)
        #                     clause_choice = random.choice(struct_list)
        #                     clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        #                     is_first = True
        #                     print("no available firsts left, new struct")
        #                 else:
        #                     clause.append(random.choice(list(possible_firsts)))
        #                     print("new first", clause)
        #                     clause_index += 1
        #             else:
        #                 clause.pop()
        #         break
        #     if set_empty:
        #         new_clause = clause.append(random.choice(list(struct_tag_words)))
        #         if new_clause not in generated:
        #             clause_index += 1
        #         else:
        #             clause_index -= 1
        #             clause.pop()
        #     # print(clause)
        # # print("final: ", clause)
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
    

    def find_word_pairs(self, tag_word, desired_tag, relevant_words):
        word_tag_pairs = list(nltk.bigrams(relevant_words))
        tag_anteceders = [
            next for (prev, next) in word_tag_pairs if prev == tag_word
            and next[1] == desired_tag
        ]
        print(tag_word, desired_tag)
        
        return(tag_anteceders)
    
    def find_n_gram_words(self, list_of_words, relevant_words):
        clean_words = [word.lower() for word in list_of_words]
        # print(clean_words)
        rel_words = [word for word, tag in relevant_words]
        n = len(list_of_words)
        ngrams = list(nltk.ngrams(rel_words, n+1))
        clean_ngrams = []
        for ngram in ngrams:
            clean = []
            for word in ngram:
                clean.append(word.lower())
            clean_ngrams.append(tuple(clean))

        # clean_ngrams = [tuple(word.lower(), tag) for word, tag in ngrams]
        # print(clean_ngrams[:10])

        next_words = [ngram[-1] for ngram in clean_ngrams if list(ngram[:-1]) == clean_words]
        return next_words


        # next_words = list(nltk.bigrams(relevant_words))
        # tag_anteceders = [
        #     next for (prev, next) in word_tag_pairs if prev == tag_word
        #     and next[1] == desired_tag
        # ]
        # print(tag_word, desired_tag)
        
        # return(tag_anteceders)



    def __str__(self):
        print("CrEATING SENTENCE")
        sentence = []
        for word in self.word_list:
            print(str(word))
            sentence.append(str(word))
        the_str = " ".join(sentence)
        print("CONCAT:", the_str.capitalize())
        return f"{the_str.capitalize()}"
    


def test():
    test = Sentence("ABA", "r", "romance", "time")
    
    # print(test.find_word_pairs(("feels", "VBZ"),"CC"))
    # print(test.relevant_words)

    # seek = []
    # for tag_words in test.relevant_words:
    #     if tag_words[1] == "JJ"

    words = test.find_n_gram_words(["the", "great"], test.relevant_words)
    print(words)
    for word in words:
        print(word)


# test()

