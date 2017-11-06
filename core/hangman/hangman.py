#!/usr/local/bin/python3

import random

test = False
def get_word(file_name, length):
    #get a random word of length 'length' from file 'file'
    possible_words = []
    f = open(file_name, 'r')
    #can use a list comprehension here
    for word in f.readlines():
        word = word.strip()
        if len(word) == length:
            possible_words.append(word)
    f.close()
    return random.choice(possible_words)

def guess_to_string(current_guess):
    #given the current guess (a list of underscores and letters) print it
    #in a clear way
    string = ""
    for character in current_guess:
        string += character
        string += " "
    return string

def new_guess(already_guessed):
    #get a guess from the user and ensure that it is only one character and has not already been guessed
    guess_char = input("Guess a letter: ")
    while len(guess_char) != 1 or guess_char in already_guessed:
        if guess_char in already_guessed:
            guess_char = input("You already guessed that letter, please guess a different one: ")
        if len(guess_char) != 1:
            guess_char = input("Please guess a single letter: ")
    return guess_char

def check_guess(guess_char, guess_word, secret_word):
    #return a tuple (bool, int, list)
    #find the letter in the word, and return a boolean (if found),
    #how many times found, and the new updated guess_word
    is_found = False
    times_found = 0
    updated_guess_word = guess_word
    for i in range(len(secret_word)):
        if secret_word[i] == guess_char:
            is_found = True
            updated_guess_word[i] = guess_char
            times_found += 1
    return (is_found, times_found, updated_guess_word)

def intro():
    #get game parameters
    global test
    print("Welcome to Hangman!")
    word_length = int(input("How many letters would you like? (2-22, or 28): "))
    while(word_length < 2 or (word_length > 22 and word_length != 28)):
        word_length = int(input("Please choose between 2 and 22, or 28: "))
    misses = int(input("How many misses would you like? : "))
    test_string = input("Would you like to run in test mode (y/n)? : ")
    secret_word = get_word("noplurals.txt", word_length)
    if test_string == "y" or test_string == "yes":
        test = True
    return secret_word, misses

def play_game(secret_word, misses):
    #play the game!
    global test
    guess_word = ["_"] * len(secret_word)
    already_guessed = []
    while misses > 0 and "_" in guess_word:
        if test:
            print("The secret word is: '" + secret_word + "'")
        print("Current guess is:\n", guess_to_string(guess_word), "\n")
        print("misses left:", misses, "\n")
        guess_char = new_guess(already_guessed)
        was_found, times_found, guess_word = check_guess(guess_char, guess_word, secret_word)
        if was_found:
            print("You found " + str(times_found) + " '" + guess_char + "'s!")
            already_guessed.append(guess_char)
        else:
            print("Oh no! '" + guess_char + "' was not found")
            misses -= 1
            already_guessed.append(guess_char)
    if misses == 0:
        print("You lost :P The word was: '" + secret_word + "'")
    else:
        print("Congrats, you won! The word was: '" + secret_word + "'")

def main():
    secret_word, misses = intro()
    play_game(secret_word, misses)

if __name__ == '__main__':
    main()
