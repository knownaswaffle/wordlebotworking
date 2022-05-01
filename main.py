#!/bin/python3

from words import WORDLE_ANSWER_SET, WORDLE_GUESS_SET

################
### WORD SET ###
################

WORDLE_WORD_SET = WORDLE_ANSWER_SET + WORDLE_GUESS_SET
WORDLE_WORD_SET_LENGTH = len(WORDLE_WORD_SET)

# Change to WORDLE_WORD_SET if you want 
# to be able to answer more words. (SLOW)
INITIAL_GUESSER_SET = WORDLE_ANSWER_SET 

###################
### ACTUAL CODE ###
###################


# Length of word in wordle.
WORDLE_WORD_LENGTH = 5


# Have the script play a game for you if you are testing.
from sys import argv
WORDLE_DEBUG_WORD = argv[1] if len(argv) > 1 else None


# The first guess takes a long time to 
# calculate and it is always the same.
WORDLE_FIRST_GUESS = "trace" # None = recalculate


# Constant values for how the game result is represented.
WORDLE_CORRECT = "G"
WORDLE_WRONG_SPOT = "W"
WORDLE_INCORRECT = "_"
WORDLE_CHARACTER_SET = "abcdefghijklmnopqrstuvwxyz"


# Message that gets shown at the beginning of the script.
WORDLE_EXAMPLE_STR = f'''

    Welcome to Waffle's Wordle Bot!
        the BEST working wordle bot

When Typing in the Result:
    1) {WORDLE_CORRECT   } - Letter in Correct Spot
    2) {WORDLE_WRONG_SPOT} - Letter in Wrong Spot
    3) {WORDLE_INCORRECT } - Letter not in word

Examples:
   - sugar : trace = _WW__
   - sugar : samba = GW___
   - whack : trace = __GG_
   - whack : shuln = _G___

'''


# Take any user input for the result of a guess
# and format it so it is consistent with the code.
# This also handles any case issues / typos.
def wordle_sanitize(result):
    return "".join(
        WORDLE_CORRECT if char == WORDLE_CORRECT else
        WORDLE_WRONG_SPOT if char == WORDLE_WRONG_SPOT else
        WORDLE_INCORRECT
        for char in result.upper()
    )


# Compare two words with the Wordle rules and
# return a string with the formatting defined above.
def wordle_compare(target_str, guess):
    result = [WORDLE_INCORRECT] * WORDLE_WORD_LENGTH
    target = list(target_str)

    for i, char in enumerate(guess):
        if char == target[i]:
            result[i] = WORDLE_CORRECT
            target[i] = '\0'
    
    for i, char in enumerate(guess):
        if result[i] == WORDLE_INCORRECT and char in target:
            result[i] = WORDLE_WRONG_SPOT
            target[target.index(char)] = '\0'

    return "".join(result)


# Class that stores information 
# needed in the process of guessing.
class WordleGuesser:
    
    def __init__(self):
        self.words = INITIAL_GUESSER_SET
        
    def get_chances(self):
        return len(self.words)
    
    # THIS PART IS CRITICAL TO THE BOTS FUNCTIONING
    # TLDR; This tells us how useful a word is.
    # 
    # By telling us how many unique results a guess can generate 
    # from the current possible word set, it is also telling us 
    # how much information this guess will give us. If we sort 
    # using this function we will get the best possible guess.
    def _get_word_splits(self, w):
        return len(set(wordle_compare(t,w) for t in self.words))

    # Get the best guess that the guesser has. This guess will 
    # reveal the most information to the guesser, meaning that 
    # it can narrow down self.words as much as possible.
    def get_guess(self):
        length = len(self.words)
        
        if length == len(INITIAL_GUESSER_SET) and WORDLE_FIRST_GUESS:
            return WORDLE_FIRST_GUESS

        if length == 1:
            return self.words[0]
        
        best_word = self.words[0]
        best_split = 1

        step = WORDLE_WORD_SET_LENGTH // 100
        for i, word in enumerate(WORDLE_WORD_SET):
            split = self._get_word_splits(word)

            if i % step == 0:
                print(f"Thinking... {(100*i)//WORDLE_WORD_SET_LENGTH}%", end='\r')
            if split >= best_split:
                best_word = word
                best_split = split

        return best_word


    # Remove any words that would not generate 
    # the same result when compared to guess.        
    def filter_words(self, guess, result):
        guess = guess
        result = wordle_sanitize(result)

        self.words = list(filter(lambda word: wordle_compare(word, guess) == result, self.words))


# Main shell loop.
if __name__ == '__main__':
    guesser = WordleGuesser()

    print(WORDLE_EXAMPLE_STR)

    # While there are still possible guesses.
    while guesser.get_chances() > 1:
        guess = guesser.get_guess()

        # Print guess and wait for response.
        print(f"Robot Guess - {guess}")
        if WORDLE_DEBUG_WORD:
            result = wordle_compare(WORDLE_DEBUG_WORD, guess)
            print(f"     Result - {result}")
        else:
            result = input(f"     Result - ")

        # Eliminate words and print change.
        if result:
            prev_chance = guesser.get_chances()
            guesser.filter_words(guess, result)
            print(f"# of Words: {prev_chance} -> {guesser.get_chances()}")
            print()
        else:
            WORDLE_WORD_SET.remove(guess)
            print(f"Removing Word: {guess}")
            print()

    # If there was a found answer.
    if guesser.get_chances() == 1:
        print(f"Answer - {guesser.get_guess()}")
    
    # If no answer exists.
    else:
        print("There are no possible answers :(")
        print("The word you picked is likely not in the Wordle answer set.")

    # If using debug mode, 
    # print information about the word.
    if WORDLE_DEBUG_WORD:
        print()
        print(f"Target - {WORDLE_DEBUG_WORD}")
        print(f"    - [In Answer Set? {WORDLE_DEBUG_WORD in WORDLE_ANSWER_SET}]")
        print(f"    - [In Total Set?  {WORDLE_DEBUG_WORD in WORDLE_WORD_SET}]")