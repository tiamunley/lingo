#!/usr/bin/python

import random
import re


class LingoException(Exception):
    pass


class Lingo:
    def __init__(self):
        self.SUCCESS = 0
        self.FAILURE = 1
        self.GIVE_UP = 2
        self.REGEX = '^[a-z]{5}$'
        self.word_list = []
        self.word = None

        self._initialize_word_list()

    # Initialize the word list
    # The list of all 5-character words in words.txt
    def _initialize_word_list(self):
        dictionary = 'words.txt'

        with open(dictionary, 'r') as fptr:
            for line in fptr:
                self.word_list.append(line.strip())

        if not self.word_list:
            raise LingoException('Invalid word list')

    # Verify that the user's guess is a legal 5-character word
    def _verify_guess(self, word):
        try:
            if not re.search(self.REGEX, word):
                return False
        except TypeError:
            return False

        return True

    # See what to do with the guess the user entered
    def move(self, entry):
        # Check if the guess is even valid (5-character word with no special chars)
        verified = self._verify_guess(entry)
        if not verified:
            return self.FAILURE

        entry = entry.strip().lower()

        # If the word was the secret word, return success
        if entry == self.word:
            return self.SUCCESS

        # If the word was 'zzzzz' (case-insensitive), return GIVE UP
        if entry == 'zzzzz':
            return self.GIVE_UP

        # Otherwise evaluate the guess
        # If a letter is correct in the correct place, print it uppercase
        # If the letter is in the word but not in the correct place, print it lowercase
        # Otherwise print '*'
        ret_val = ''
        for i in range(0, 5):
            if entry[i] == self.word[i]:
                ret_val += entry[i].upper()
            elif entry[i] in self.word:
                ret_val += entry[i].lower()
            else:
                ret_val += '*'

        # Return the appropriate ret_val
        return ret_val

    # Start a new game
    # Choose a random word from the word_list
    def new_game(self):
        self.word = random.choice(self.word_list)
        print 'Starting a new game'
        print 'If you want to quit a game, enter "ZZZZZ" as your next guess.'

    # Play!
    def play_lingo(self):
        do_you_want_to_play = raw_input('\nDo you want to play Lingo? (y/n) ')

        # Keep starting new games as long as the user enters 'y'
        while do_you_want_to_play.strip().lower() == 'y':
            self.new_game()

            # Keep allowing the user to guess forever, until SUCCESS, GIVE_UP, or <ctrl>-C
            while True:
                # Prompt for the next move
                guess = raw_input('Your next guess: ')
                move_result = self.move(guess)

                # User guessed the right word
                # Quit this game; start a new one
                if move_result == self.SUCCESS:
                    print 'Success!! You win!!'
                    break

                # User entered an invalid string (anything other than a string of 5 lower-case letters)
                # Prompt user again
                if move_result == self.FAILURE:
                    print 'Invalid guess. Please try again'
                    continue

                # User entered 'ZZZZZ' which means they want to end this one round
                # Print secret word and move on to the next round
                if move_result == self.GIVE_UP:
                    give_up_response = raw_input('Do you give up? Are you sure? (y/n) ')
                    if give_up_response.strip().lower() == 'y':
                        print 'Your word was %s' % self.word
                        break
                    continue

                # Print the response from the move
                print move_result + '\n'

            # Do you want to play again?
            do_you_want_to_play = raw_input('\nDo you want to play Lingo? (y/n) ')

        # Thanks for playing
        print '\nThanks for playing!\n'


if __name__ == '__main__':
    lingo = Lingo()
    lingo.play_lingo()
