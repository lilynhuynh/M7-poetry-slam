import spacy
import nltk
import random
# from word import Word
from poem_generator.word import Word
from nltk.corpus import brown
import pronouncing
from nltk import ngrams
from collections import deque
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('brown')

class Sentence:
    MAX_SENTENCE_GRID = 10
    
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


    MAX_SYLLABLES = 10

    def __init__(self, pattern_key, secret_letter, theme, rhyme):
        self.word_list = self.generate_empty_word_list()
        self.pattern_key = pattern_key
        self.secret_letter = secret_letter
        self.theme = theme
        self.relevant_words = [word.lower() for word in brown.words() if word.isalpha()]
        self.rhyme = rhyme
        self.possible_words = deque()
        self.syllable_count = 0
        self.used_words_dict = dict()

        # self.sentence_struct = random.choice(self.SENTENCE_STRUCTS)
        self.sentence_struct = "Simple"

    """
    TODO: Use sudoku solver backtracking method to figure out sentence generation
    - solve method - loops through grid, this case 1D array for sentence
        - for loop, if cur space is 0 (empty), create new word obj that calls next move function
        - if next word invalid, call backtrack, peek deque for move index
        - if next word valid, get word obj value, update word list with new word, push word to deque
    - next move method - checks if word is valid, returns null if not valid, if not valid, call backtrack
        - checks if valid using valid answer method
    - valid answer method -
        - checks if context of word in word list is valid, returns boolean
    - bactrack method - pop the recent word from deque, try a new word from deque, insert into word list
        - if new word also null, call bactrack again
        - if valid, push new move into deque, update word list with new word

    """
    def generate_empty_word_list(self):
        word_list = []
        for i in range(0, self.MAX_SENTENCE_GRID):
            word_list.append("")
        return word_list


    def check_valid_word(self, word, syllables, index):
        # Check if it is first word, does it match the secret letter
        if index == 0:
            first_letter = word[0]
            if first_letter == self.secret_letter:
                print("valid first word:", word)
                return True
            else:
                return False

        else:
        # Since we are parsing through related ngrams, we know it is in context

            # Check if current syllable count + new word does not extend pass MAX_SYLLABLES
            cur_syllable_coount = self.syllable_count
            new_syllables_count = cur_syllable_coount + syllables
            if new_syllables_count < self.MAX_SYLLABLES:
                print("valid word:", word)
                return True
            elif new_syllables_count == self.MAX_SYLLABLES:
                # Check if it is last word, does it rhyme
                print("is last word")
                if self.rhyme != "":
                    rhymes = pronouncing.rhymes(self.rhyme)
                    if word not in rhymes:
                        return False
                else:
                    print("no rhyme recorded")
                    return True
            else:
                print("max syllables exceeded")
                return False
            

    def get_next_word(self, index):
        # Check if it finds word list context
        # Generate list of ngram words based on current word and trigram word list
        ngrams = []
        if index == 0: # First word, check if first given word is valid
            ngrams = [word for word in self.relevant_words if word[0] == self.secret_letter]
        elif index <= 2:
            clause = self.word_list[:3]
            print(clause)
            ngrams = self.find_n_gram_words(clause)
        else:
            clause = self.word_list[index-3:index]
            print(clause)
            ngrams = self.find_n_gram_words(clause)
        # print("ngrams:", ngrams)

        ngram_len = len(ngrams)
        i = 0
        while i < ngram_len:
            ngram = random.choice(ngrams)
            new_word = Word(ngram, index)
            if new_word.num_syllables != 0:
                if self.check_valid_word(new_word.word, new_word.num_syllables, index) == True:
                # Check if able to count syllables
                    return new_word
            i += 1
        return None


    def find_n_gram_words(self, word_list):
        clean_words = [word.lower() for word in word_list if word != ""]

        # Get current len of word list, remove blanks
        n = len(clean_words)

        ngram_words = list(ngrams(self.relevant_words, n+1))
        clean_ngrams = []
        for ngram in ngram_words:
            clean = []
            for word in ngram:
                clean.append(word.lower())
            clean_ngrams.append(clean)
        # clean_ngrams = [tuple(word.lower(), tag) for word, tag in ngrams]
        # print(clean_ngrams[:10])
        next_words = []
        for ngram in clean_ngrams:
            if ngram[:n] == clean_words:
                all_alnum = True
                for word in ngram:
                    if word.isalnum() == False:
                        all_alnum = False
                if all_alnum == True:
                    if ngram[-1] not in next_words:
                        next_words.append(ngram[-1])

        return list(next_words)


    def backtrack(self):
        print("IN BACKTRACKING")
        print("current word list while in backtracking:", self.word_list)
        print("current syllable count while backtracking:", self.syllable_count)

        # Base case, if no more possible words left
        if not self.possible_words:
            print("Base case, reached the beginning, no more possible moves")
            self.syllable_count = 0
            self.word_list = self.generate_empty_word_list()
            return
        
        print("Checking the deque in backtracking")
        for move in self.possible_words:
            print(move)

        recent_word = self.possible_words.popleft() # get recent move
        i = recent_word.index
        word = recent_word.word
        syllables = recent_word.num_syllables
        print("Recent Move:", word, i, syllables)

        self.word_list[i] = ""
        self.syllable_count -= syllables

        self.update_used_words(i, word)

        try_word = self.get_next_word(i)
        print("dict:", self.used_words_dict[i])

        if try_word is not None:

            if try_word.word not in self.used_words_dict[i]:
            # Check if word has already been used, don't decrement if already used
                print("New valid word", try_word.word, "in backtracking at index", i)
                self.possible_words.appendleft(try_word)
                self.word_list[i] = word
                    # self.syllable_count = self.syllable_count + try_word.num_syllables
                    # self.update_used_words(i, try_word.word)
                    # print("updated word list, finished backtracking:", self.word_list)
                    # print("returned index for new try_word:", try_word.index)
                    # print("new syllable count after backtrack:", self.syllable_count)
                return

        self.backtrack()


    def generate_sentence(self):
        i = 0
        stop = 0
        while i < self.MAX_SENTENCE_GRID:
            if stop == 50:
                print("stuck in while loop, break")
                break
            print("cur sentence:",self.word_list)
            print("cur syllables:", self.syllable_count)
            print("cur index:", i)
            # Check if already reached max syllable count
            if self.syllable_count == self.MAX_SYLLABLES:
                break
            
            if self.word_list[i] == "":
                # random_word = random.choice(self.relevant_words).lower()
                # print(random_word)
                word = self.get_next_word(i)
                was_backtracking = False
                if word is None:
                    self.backtrack()
                    print("finished back tracking")
                    word = self.possible_words[0] # peek
                    print("previous word sentence index", i)
                    i = word.index # update index
                    print("peeked at new word:", word.word, i)
                    was_backtracking = True

                new_word = word
                print("new word at index:", new_word.word, new_word.index, new_word.num_syllables)
                self.update_used_words(i, new_word.word)
                self.word_list[i] = new_word.word
                print("previous syllables count:", self.syllable_count)
                self.syllable_count += new_word.num_syllables
                print("updated syllables count:", self.syllable_count)
                if was_backtracking is False:
                    self.possible_words.appendleft(new_word)
                i += 1
            stop += 1


    def update_used_words(self, index, word):
        if index not in self.used_words_dict:
            print("added index", index)
            self.used_words_dict[index] = set()
        # else:
        #     print("added word in for index", word, index)
        #     self.used_words_dict[index].append(word)
        self.used_words_dict[index].add(word)



    def clean_sentence(self):
        cleaned_sentence = []
        for word in self.word_list:
            if word != "":
                cleaned_sentence.append(word)
        self.word_list = cleaned_sentence


    def create_relevant_words(self):
        words = brown.words()
        valid_english_words = set(
                word.lower() for word in words
                if word.isalpha() and
                (len(word) > 1 or word.lower() in {"a", "i"})
            )
        

        return valid_english_words


    def generate_sentence2(self):
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

                    if len(clause) == 0:
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
        given_relevant_words = relevant_words
        # relevant_word_pairs = set()

        # SYLLABLES COUNTER
        MAX_SYLLABLES = 10
        syllables_count = 0

        while end_sentence == False: # change this
            print("current clause", clause)
            print("possible firsts:", len(possible_firsts))
            if is_first:
                set_empty = False
                while set_empty == False:
                    for word in relevant_words:
                        word = word.lower()
                        if word[0] == self.secret_letter:
                        # if word.isalpha() or word.isalnum():
                            possible_firsts.append(word)
                    if len(possible_firsts) != 0:
                        set_empty = True
                    else:
                        struct_list.remove(clause_choice)
                        clause_choice = random.choice(struct_list)
                        clause_struct = self.IND_CLAUSE_STRUCTS[clause_choice]
                
                while syllables_count == 0:
                    add_first = random.choice(list(possible_firsts))
                    first_word = self.define_new_word(add_first)
                    if first_word.num_syllables != 0:
                        syllables_count += first_word.num_syllables
                        clause.append(add_first)
                        break

                clause_index += 1
                is_first = False
            # generated list of possible first words
            clean_possible_first = set(possible_firsts)
            possible_firsts = list(clean_possible_first)
            while syllables_count <= MAX_SYLLABLES or len(possible_firsts) != 0:
                print("clause", clause)
                print("syllables count:", syllables_count)

                if clause_index <= 3:
                    print(f"looking at clause from [0:{clause_index}] - {clause}")
                    relevant_ngram_words = self.find_n_gram_words(clause, self.relevant_words)
                else:
                    print(f"looking at clause from [{clause_index-3}:{len(clause)+1}] - {clause[clause_index-3:]}")
                    relevant_ngram_words = self.find_n_gram_words(clause[clause_index-3:], self.relevant_words)

                # if relevant n grams empty, go back 1 or if first again, change first
                if len(relevant_ngram_words) == 0:
                    print("no relevant words")
                    clause_index -= 1
                    if len(clause) == 0:
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
                is_valid_word = False
                while is_valid_word == False:
                    print("in valid words check, relevant ngrams", len(relevant_ngram_words))
                    if syllables_count > 7 and self.rhyme != "": #last word
                        print("Found last word")
                        rhymes = pronouncing.rhymes(self.rhyme)
                        rand_rhyme = random.choice(rhymes)
                        print("NEW WORD:", rand_rhyme)
                        # syllables_count += new_word.num_syllables
                        syllables_count = MAX_SYLLABLES
                        clause.append(rand_rhyme)
                        clause_index += 1
                        is_valid_word = True
                        break

                    if len(relevant_ngram_words) == 0:
                        is_valid_word = True
                        break
                    random_next_word = random.choice(relevant_ngram_words)
                    new_word = self.define_new_word(random_next_word)

                    # Check if valid word less than syllable count
                    new_word_syllables = new_word.num_syllables

                    if syllables_count > 7 and self.rhyme == "":
                        new_word_syllables = 1 # defaulting some rand number just to pass as last word, change later

                    if new_word_syllables != 0:
                        print("NEW WORD:", random_next_word)
                        syllables_count += new_word.num_syllables
                        clause.append(random_next_word)
                        clause_index += 1
                        is_valid_word = True
                        prev_relevant_ngram_words = relevant_ngram_words
                    else:
                        print("unable to count syllables of", random_next_word)
                        relevant_ngram_words.remove(random_next_word)
                
                if syllables_count >= MAX_SYLLABLES:
                    end_sentence = True
                    break
                
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

    
    def find_n_gram_words3(self, word, word_list):
        clean_words = [word.lower() for word in word_list]
        # print(clean_words)
        n = len(word_list)
        ngrams = list(nltk.ngrams(self.relevant_words, n+1))
        clean_ngrams = []
        for ngram in ngrams:
            clean = []
            for word in ngram:
                clean.append(word.lower())
            clean_ngrams.append(tuple(clean))
        # clean_ngrams = [tuple(word.lower(), tag) for word, tag in ngrams]
        # print(clean_ngrams[:10])
        next_words = [ngram[-1] for ngram in clean_ngrams if list(ngram[:-1]) == clean_words and list(ngram[:-1].isalnum())]
        return next_words


        # next_words = list(nltk.bigrams(relevant_words))
        # tag_anteceders = [
        #     next for (prev, next) in word_tag_pairs if prev == tag_word
        #     and next[1] == desired_tag
        # ]
        # print(tag_word, desired_tag)
        
        # return(tag_anteceders)


    def define_new_word(self, word):
        new_word = Word(word, "")
        new_word.count_syllables()

        return new_word
    

    def __str__(self):
        print("CrEATING SENTENCE")
        sentence = []
        for word in self.word_list:
            print(str(word))
            sentence.append(str(word))
        the_str = " ".join(sentence)
        print("CONCAT:", the_str.capitalize())
        return f"{the_str.capitalize()}"
    


# def test():
    # test = Sentence("ABA", "r", "romance", "time")
    
    # print(test.find_word_pairs(("feels", "VBZ"),"CC"))
    # print(test.relevant_words)

    # seek = []
    # for tag_words in test.relevant_words:
    #     if tag_words[1] == "JJ"

    # trigrams = test.find_word_trigrams(["the","dog"], test.relevant_words)
    # print(trigrams)

    # bigrams = test.find_word_bigrams("dog", test.relevant_words)
    # print(bigrams)

    # words = test.find_n_gram_words(["the", "great"], test.relevant_words)
    # print(words)
    # for word in words:
    #     print(word)

# test()

