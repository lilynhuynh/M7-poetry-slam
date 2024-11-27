"""
CSCI 3725 Computational Creativity
M7 Poetry Slam

This file consists of the Sentence class where it generates a sentence based
on the given parameters and uses these parameters to build a coherent sentence.
The classes includes functions like checking if a given word is valid based
on the current syllables and its current word index, backtracking, and more.

Authors: Lily Huynh
Last Updated: November 26, 2024

Bugs:
- Backtracking function and syllables counter not properly working
  (e.g. the syllable_count can be negative), this is addressed within the
  README in more detail
"""

import random
from poem_generator.word import Word
from nltk.corpus import brown
import pronouncing
from nltk import ngrams
from collections import deque

class Sentence:
    """
    Sentence represents the sentence object in which it keeps track of its
    current word list and syllables to generate a coherent sentence based on
    the given constraints (i.e. secret letter, theme, and rhyme).
    """

    # Global variables
    MAX_SENTENCE_GRID = 10 # Max number of words allowed in a sentence
    MAX_SYLLABLES = 10 # Max number of syllables in a sentence

    def __init__(self, secret_letter, theme, rhyme):
        self.word_list = self.generate_empty_word_list()
        self.secret_letter = secret_letter
        self.theme = theme
        self.relevant_words = [word.lower() for word in brown.words()
                               if word.isalpha()]
        self.rhyme = rhyme
        self.possible_words = deque()
        self.syllable_count = 0
        self.used_words_dict = dict()

    def generate_empty_word_list(self):
        """Initializes word list of 10 empty strings."""
        word_list = []
        for i in range(0, self.MAX_SENTENCE_GRID):
            word_list.append("")
        return word_list

    def check_valid_word(self, word, syllables, index):
        """Checks if the given word is valid based on the following criteria:
        1. If first word, does its first letter match the secret letter
        2. If not first word, will adding it exceed the MAX syllables
        3. If last word, does it rhyme with given rhyme (if given)"""
        # Check if it is first word, does it match the secret letter
        if index == 0:
            first_letter = word[0]
            if first_letter == self.secret_letter:
                print("Found valid FIRST word")
                return True
            else:
                return False

        else:
            cur_syllable_coount = self.syllable_count
            new_syllables_count = cur_syllable_coount + syllables

            # If not first word, is it less than MAX_SYLLABLES
            if new_syllables_count < self.MAX_SYLLABLES:
                print("Found valid word less than MAX syllables")
                return True
            elif new_syllables_count == self.MAX_SYLLABLES:
                
                # If last word, does it rhyme (if given rhyme)
                if self.rhyme != "":
                    rhymes = pronouncing.rhymes(self.rhyme)
                    if word not in rhymes:
                        return False
                    else:
                        print("Found valid LAST word that rhymes")
                        return True
                else:
                    print("Found valid last word")
                    return True
            else:
                return False
            
    def get_next_word(self, index):
        """
        Chooses a random next word based on the generated ngrams next word by
        given index and checks if this random next word is valid. If valid,
        it returns the new word object, else it returns None.
        """
        # Generates the ngram releted next words
        print("Getting next word in sentence")
        ngrams = []
        if index == 0: # If first word
            ngrams = [word for word in self.relevant_words
                      if word[0] == self.secret_letter]
        elif index <= 2: # If less than or equal to 3 words in word list
            clause = self.word_list[:3]
            print(f"Current clause for ngrams: {clause}")
            ngrams = self.find_n_gram_words(clause)
        else: # If greater than 3 words in word list
            clause = self.word_list[index-3:index]
            print(f"Current clause for ngrams: {clause}")
            ngrams = self.find_n_gram_words(clause)

        ngram_len = len(ngrams)
        i = 0
        print(f"Found {ngram_len} related next words!")
        
        # While ngram next words available, check if valid
        while i < ngram_len:
            ngram = random.choice(ngrams)
            new_word = Word(ngram, index)
            val = new_word.word
            syl = new_word.num_syllables
            if new_word.num_syllables != 0:
                if self.check_valid_word(val, syl, index) is True:
                    return new_word
            i += 1
        return None

    def find_n_gram_words(self, clause):
        """Generates related next words based on the ngram clause given"""
        clean_words = [word.lower() for word in clause if word != ""]
        n = len(clean_words)

        ngram_words = list(ngrams(self.relevant_words, n+1))
        clean_ngrams = []
        for ngram in ngram_words:
            clean = []
            for word in ngram:
                clean.append(word.lower())
            clean_ngrams.append(clean)

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
        """Backtracking function that pops the most recent word used from the
        deque and trys a new word at that given index. If the tried word
        was already used, it backtracks again until a new valid word
        is given."""
        # Print statements for responsiveness within Terminal
        print("IN BACKTRACKING")
        print(f"Current word list while in backtracking: {self.word_list}")
        print(f"Current syllables while backtracking: {self.syllable_count}")

        # Base case, if no more possible words left
        if not self.possible_words:
            print("Base case, reached the beginning, no more possible moves")
            self.syllable_count = 0
            self.word_list = self.generate_empty_word_list()
            return
        
        # Pops from deque to get most recent word information
        recent_word = self.possible_words.popleft()
        i = recent_word.index
        word = recent_word.word
        syllables = recent_word.num_syllables
        print(f"Recent Word (Word, Idx, Syllables): {word} {i} {syllables}")

        # Resets word list and syllable count from before recent word
        self.word_list[i] = ""
        self.syllable_count -= syllables

        # Updates used word dictionary at current index with recent word
        self.update_used_words(i, word)

        try_word = self.get_next_word(i)
        print(f"Used words: {self.used_words_dict[i]}")

        # Checks if tried word is valid and has not been used before
        if try_word is not None:
            if try_word.word not in self.used_words_dict[i]:
                print(f"New word {try_word.word} in backtracking at idx {i}")
                self.possible_words.appendleft(try_word)
                self.word_list[i] = word
                return

        self.backtrack()

    def generate_sentence(self):
        """Main parent function used to build the sentence. Calls on get next
        word based on current sentence index and backtracks if next word is
        invalid. Updates the sentence index and syllable count based on
        status. Also has a STOP measure to prevent super long sentence
        generations."""
        i = 0
        stop = 0
        while i < self.MAX_SENTENCE_GRID:
            if stop == 50:
                print("Stuck in while loop, break sentence generation")
                break
            print(f"Current sentence: {self.word_list}")
            print(f"Current syllables: {self.syllable_count}")
            print(f"Cur index: {i}")

            # Check if already reached max syllable count
            if self.syllable_count == self.MAX_SYLLABLES:
                break
            
            # If current string in word list is empty, get next word
            if self.word_list[i] == "":
                word = self.get_next_word(i)
                was_backtracking = False

                # If word is invalid, backtrack until a valid next word
                if word is None:
                    self.backtrack()
                    word = self.possible_words[0] # peek
                    i = word.index # update index
                    was_backtracking = True

                new_word = word
                val = new_word.word
                syl = new_word.num_syllables
                idx = new_word.index
                print(f"New word (Word Syllables Index): {val} {syl} {idx}")
                self.update_used_words(i, val)
                self.word_list[i] = val
                self.syllable_count += syl

                # Ensures deque does not add repeats
                if was_backtracking is False:
                    self.possible_words.appendleft(new_word)
                i += 1
            stop += 1

    def update_used_words(self, index, word):
        """Updates the used words dictionary based on given word list index
        and given word to add to set"""
        if index not in self.used_words_dict:
            self.used_words_dict[index] = set()
        self.used_words_dict[index].add(word)

    def clean_sentence(self):
        """After a valid sentence has been generated, it removes all the
        extra empty strings when word list was initalized (if any)"""
        cleaned_sentence = []
        for word in self.word_list:
            if word != "":
                cleaned_sentence.append(word)
        self.word_list = cleaned_sentence

    def __str__(self):
        """Generates a string representation of Sentence"""
        sentence = []
        for word in self.word_list:
            sentence.append(str(word))
        the_str = " ".join(sentence)
        return f"{the_str.capitalize()}"
    
    def __repr__(self):
        """Returns an unambiguous representation of the Sentence."""
        return f"Word('{self.secret_letter}', '{self.theme}', '{self.rhyme}')"