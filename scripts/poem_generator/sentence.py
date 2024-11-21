import spacy
import nltk
import random
# from word import Word
from poem_generator.word import Word
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
        self.relevant_words = brown.tagged_words(tagset='brown')
        self.rhyme = rhyme

        # self.sentence_struct = random.choice(self.SENTENCE_STRUCTS)
        self.sentence_struct = "Simple"

    def generate_relevant_words(self):
        brown_word_list = brown.tagged_words(tagset='brown')

        updated_brown_alpha = {}
        for word, tag in brown_word_list:
            # if word not in updated_brown_alpha and word.isalpha():
            if word not in updated_brown_alpha:
                updated_brown_alpha[word] = tag

        unique_brown_list = [(word, tag) for word, tag in updated_brown_alpha.items()]

        return unique_brown_list


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
            print("calling sentence generation", len(self.relevant_words))
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
        ind_clause = self.generate_independent_clause4(relevant_words, True)
        print("GENERATED:", ind_clause)
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
        MAX_SYLLABLES = 10
        syllables_cur = 0
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

        while syllables_cur < MAX_SYLLABLES: # change this
            print("current clause", clause)
            if is_first:
                set_empty = False
                while set_empty == False:
                    for tag_word in relevant_words:
                        word = tag_word[0].lower()
                        if word[0] == self.secret_letter:
                        # if word.isalpha() or word.isalnum():
                            if tag_word[1] == clause_struct[clause_index]:
                                # create into word class, get num syllables
                                new_word = Word(word, "") # TODO: change word param later
                                new_word.count_syllables()

                                if new_word.num_syllables != 0:
                                    # print("VALID WORD:", word)
                                    possible_firsts.append((new_word, word))
                        print("Cur saved firsts:", len(possible_firsts))
                    if len(possible_firsts) != 0:
                        set_empty = True
                    else:
                        struct_list.remove(clause_choice)
                        clause_choice = random.choice(struct_list)
                        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]

                first_word_choice = random.choice(list(possible_firsts))
                clause.append(first_word_choice[1])
                clause_index += 1
                syllables_cur += first_word_choice[0].num_syllables
                is_first = False
            
            # generated list of possible first words
            clean_possible_first = set(possible_firsts)
            possible_firsts = list(clean_possible_first)
            print("GENERATED FIRSTS", len(possible_firsts))

            while len(possible_firsts) != 0:
                print("clause", clause)
                print("cur syllable count", syllables_cur)
                relevant_ngram_words = self.find_n_gram_words(clause, self.relevant_words)
                print("FOUND RELEVANT", len(relevant_ngram_words))
                # if relevant n grams empty, go back 1 or if first again, change first
                if len(relevant_ngram_words) == 0:
                    print("no relevant words")
                    clause_index -= 1

                    if len(clause_index) == 0:
                        # remove current first from possible first and from clause array
                        to_remove = clause[clause_index]
                        possible_firsts = [tuple for tuple in possible_firsts if tuple[1] != to_remove]
                        print("no available after first, removed",clause[clause_index], len(possible_firsts))
                        clause.pop()
                        if len(possible_firsts) == 0: # if no more possible firsts, choose new struct
                            struct_list.remove(clause_choice)
                            clause_choice = random.choice(struct_list)
                            clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                            is_first = True
                            print("no available firsts left, new struct")
                        else: # choose a new possible first
                            new_first = random.choice(list(possible_firsts))
                            clause.append(new_first[1])
                            syllables_cur = new_first[0].num_syllables
                            print("new first", clause)
                            clause_index += 1
                            break
                    else:
                        new_valid_word = False
                        while new_valid_word == False:
                            # if clause is not 1, remove current word from prev list
                            prev_relevant_ngram_words.remove(clause[clause_index])
                            # choose a random word from prev ngrams list
                            new_word_from_prev = random.choice(prev_relevant_ngram_words)
                            new_word = Word(new_word_from_prev, "")
                            new_word.count_syllables()
                            if new_word.num_syllables != 0:
                                syllables_cur += new_word.num_syllables
                                clause.append(new_word_from_prev)
                                new_valid_word = True
                        break
                
                # list of relevant words available
                print("List of relevant words available!")
                print("relevant ngrams", len(relevant_ngram_words))


                # choose random word from list of ngrams

                found_valid = False
                while found_valid == False:
                    random_next_word = random.choice(relevant_ngram_words)

                    new_word_obj = Word(random_next_word, "")
                    new_word_obj.count_syllables()

                    if new_word_obj.num_syllables == 0:
                        if len(relevant_ngram_words) == 0:
                            clause_index -= 1
                            clause.pop()
                        else:
                            relevant_ngram_words.remove(random_next_word)
                    else:
                        # check how many syllables left
                        if new_word_obj.num_syllables + syllables_cur < MAX_SYLLABLES:
                            clause.append(random_next_word)
                            syllables_cur += new_word_obj.num_syllables
                            found_valid = True
                        # elif new_word_obj.num_syllables + syllables_cur == MAX_SYLLABLES:
                        #     # WE NEED TO APPEND THE NEW WORD AND SAVE THIS AS A COMPLETE LINE
                        #     clause.append(random_next_word)
                        #     syllables_cur == MAX_SYLLABLES
                        #     found_valid = True
                        # # else:
                            # REROLL THE WORD
                prev_relevant_ngram_words = relevant_ngram_words




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
    
    def generate_independent_clause3(self, relevant_words):
        MAX_SYLLABLES = 10
        syllables_cur = 0

        struct_list = [1,2,3,4,5,6,7,8]
        clause_choice = random.choice(struct_list)
        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
        clause_index = 0
        clause = []

        possible_firsts = []
        bigrams_from_first = []
        cur_trigrams = []

        while syllables_cur < MAX_SYLLABLES:
            print("current index:", clause_index)
            # Find all possible first words
            if clause_index == 0:
                set_empty = True
                while set_empty:
                    # look through brown tagged words for matching secret and matches clause struct
                    print("cur clause struct", clause_struct)
                    for tag_word in relevant_words:
                        word = tag_word[0].lower()
                        # check if matches secret letter
                        if word[0] == self.secret_letter:
                            # check if first word matches cur struct
                            if tag_word[1] == clause_struct[clause_index]:
                                # create a new word instance to count num syllables
                                new_word = Word(word, "")
                                new_word.count_syllables()

                                # check if created word has syllables
                                if new_word.num_syllables != 0:
                                    # add word object, since if we need new first, have its syllables saved
                                    possible_firsts.append((new_word, word))
                            else:
                                continue
                            
                    print("finish generating firsts", len(possible_firsts))

                    # See if possible first words is populated, if not, try a new struct
                    if len(possible_firsts) != 0:
                        set_empty = False
                        # will break while loop for set_empty
                    else:
                        struct_list.remove(clause_choice)
                        clause_choice = random.choice(struct_list)
                        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                        print("new clause struct", clause_struct)
                
                # Choose random first word from possible firsts
                first_word_choice = random.choice(list(possible_firsts))
                # Add chosen first word to clause, only the word, not object
                clause.append(first_word_choice[1])
                print(first_word_choice[0].word, first_word_choice[0].num_syllables)
                syllables_cur += first_word_choice[0].num_syllables
                clause_index += 1

                # We are currently on the words past the first word
                # Want to remove all duplicate first words from possible firsts
                clean_possible_first = set(possible_firsts)
                possible_firsts = list(clean_possible_first)
                
            elif clause_index == 1:
                print("Number of available first words:", len(possible_firsts))
                # While we still have first words available, try to generate more words after
                found_new_word = False

                while len(possible_firsts) != 0 or found_new_word == True:
                    print("clause:", clause)
                    print("syllable count:", syllables_cur)

                    # We want to find the relevant bigrams
                    # returns a list of lists of bigrams [[x, y], [x, z], ...]
                    bigrams_from_first = self.find_word_bigrams(clause[0], relevant_words)

                    while len(bigrams_from_first) > 0:
                        if found_new_word == True:
                            print("already new word but still have bigrams")
                            break
                        # choose a random bigram and check if the new word is able to count syllables
                        while found_new_word == False:
                            new_bigram = random.choice(bigrams_from_first)
                            new_word_from_bigram = new_bigram[-1]
                            # create as word object to check syllables
                            new_word = Word(new_word_from_bigram, "")
                            new_word.count_syllables()
                            if new_word.num_syllables != 0:
                                print(new_word.word, new_word.num_syllables)
                                syllables_cur += new_word.num_syllables
                                clause.append(new_word_from_bigram)
                                clause_index += 1
                                found_new_word = True
                        

                    # check if bigrams are populated
                    if len(bigrams_from_first) == 0:
                        clause_index -= 1
                        # no relevant words from first
                        # delete current first word from possible firsts
                        to_remove = clause[clause_index]
                        possible_firsts = [tuple for tuple in possible_firsts if tuple[1] != to_remove]

                        # choose a new first and update clause and syllables with new first
                        new_first = random.choice(list(possible_firsts))
                        clause[clause_index] = new_first[1]
                        syllables_cur = new_first[0].num_syllables
                        print("New first", clause)
                        clause_index += 1
                        # want to regenerate new bigrams
                    # NOTE - will handle if no more possible firsts later!!!                        

            # Entering trigram zone
            # If the word is of length = 2
            elif clause_index == 2:
                print("Number of bigrams available:", len(bigrams_from_first))
                # Loop through available bigrams
                while len(bigrams_from_first) != 0 or clause_index > 2:
                    print("clause:", clause)
                    print("syllable count:", syllables_cur)

                    cur_trigrams = self.find_word_trigrams(clause, relevant_words)

                    while len(cur_trigrams) > 0:
                    # We do have a available list of trigrams
                        # want to choose new bigram if exhausted current trigrams
                        # Choose a random trigram and check if new word is able to count
                        found_new_word = False
                        while found_new_word == False:
                            new_trigram = random.choice(cur_trigrams)
                            new_word_from_trigram = new_trigram[-1]
                            # create new word object
                            new_word = Word(new_word_from_trigram, "")
                            new_word.count_syllables()
                            if new_word.num_syllables != 0:
                                print(new_word.word, new_word.num_syllables)
                                syllables_cur += new_word.num_syllables
                                clause.append(new_word_from_trigram)
                                clause_index += 1
                                found_new_word = True
                            else:
                                cur_trigrams.remove(new_trigram)
                        if found_new_word == True:
                            break

                    # check if trigrams populated
                    if len(cur_trigrams) == 0:
                        # if no relevant trigrams, remove current bigram
                        # remember to remove the cur word syllables from cur_syllables
                        clause_index -= 1

                        cur_bigram_word = clause[clause_index]
                        cur_bigram_word_obj = Word(cur_bigram_word, "")
                        cur_bigram_word_obj.count_syllables()
                        syllables_cur -= cur_bigram_word_obj.num_syllables

                        bigrams_from_first.remove(clause)

                        # choose a new bigram from the list
                        new_bigram = random.choice(bigrams_from_first)
                        
                        # set the new next word in bigram to next word in clause
                        # update the syllables_cur with new word
                        clause[clause_index] = new_bigram[-1]

                        new_bigram_word = Word(new_bigram[-1], "")
                        new_bigram_word.count_syllables()
                        print(new_bigram_word.word, new_bigram_word.num_syllables)
                        syllables_cur += new_bigram_word.num_syllables
                        clause += 1

            # Word is length >= 3
            else:
                print("Number of trigrams available:", len(cur_trigrams))
                # same idea but now we generate new trigrams by past trios
                while len(cur_trigrams) != 0:
                    print("clause:", clause)
                    print("syllable count", syllables_cur)

                    phrase_trigrams = self.find_word_trigrams(clause[clause_index-2:-1], relevant_words)

                    while len(phrase_trigrams) > 0:
                        found_new_word = False
                        while found_new_word == False:
                            new_trigram = random.choice(phrase_trigrams)
                            new_word_from_trigram = new_trigram[-1]
                            # create new word object
                            new_word = Word(new_word_from_trigram, "")
                            new_word.count_syllables()
                            if new_word.num_syllables != 0:
                                print(new_word.word, new_word.num_syllables)
                                syllables_cur += new_word.num_syllables
                                clause.append(new_word_from_trigram)
                                clause_index += 1
                                found_new_word = True
                            else:
                                phrase_trigrams.remove(new_trigram)
                        if found_new_word == True:
                            cur_trigrams = phrase_trigrams
                            break
                    
                    # No more available trigrams for this phrase
                    if len(phrase_trigrams) == 0:
                        # remove this current trigram and try again
                        cur_trigrams.remove(clause[clause_index-2:-1])


            # No more saved trigrams? reset the clause back t
            # if len(cur_trigrams) == 0:

        return clause

    def generate_dependent_clause(self, relevant_words):
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
    

    def find_word_bigrams(self, word, relevant_words):
        word_tag_pairs = list(nltk.bigrams(relevant_words))

        possible_pairs = [[prev[0].lower(), next[0].lower()] for (prev, next) in word_tag_pairs if prev[0] == word]

        return possible_pairs
    
    def find_word_trigrams(self, list_of_words, relevant_words):
        clean_words = [word.lower() for word in list_of_words]
        print(clean_words)
        word_tag_trigrams = list(nltk.trigrams(relevant_words))
        clean_trigrams = []
        for trigram in word_tag_trigrams:
            clean = []
            for word in trigram:
                word = list(word)[0]
                clean.append(word.lower())
            clean_trigrams.append(clean)
        next_words = [trigram for trigram in clean_trigrams if list(trigram[:-1]) == clean_words]
        return next_words

    def generate_independent_clause4(self, relevant_words, is_first):
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

    trigrams = test.find_word_trigrams(["the","dog"], test.relevant_words)
    print(trigrams)

    bigrams = test.find_word_bigrams("dog", test.relevant_words)
    print(bigrams)

    # words = test.find_n_gram_words(["the", "great"], test.relevant_words)
    # print(words)
    # for word in words:
    #     print(word)


# test()

