""" 
This program is witten by ShaderOX (https://github.com/ShaderOX) and free to use and modify by anyone.
"""
import os
import sys
import time
import random
import curses

# All the words presented by the computer to the user
ALL_WORDS = []
# All the words entered by the user
USER_WORDS = []
# Varibale for keeping track of number of keypresses
CHARS_PRESSED = 0
# The test duration is currently 60 seconds
TEST_DURATION = 60


def main():
    # Starts a timer of 3 seconds.
    start_timer(3)
    # Wraps the terminal_screen() function with the curses initscr().
    curses.wrapper(terminal_screen)
    # Prepares and Displays the results to the user.
    prepare_results()


def terminal_screen(stdscr):
    """ Controls and handles the entire testing process """
    global ALL_WORDS, USER_WORDS, CHARS_PRESSED, TEST_DURATION

    # Gets the max screen size height, width
    _, max_x = stdscr.getmaxyx()
    # Reads all 1000 words in ./words.txt
    words = read_file()
    # Enables echo in the terminal i.e. you have see what you have written
    curses.echo()
    # Keeps track of the number of spacebars pressed for manipulation
    spacebar_presses = 0
    # Gets the initial reading of time for estimating TEST_DURATION
    time_ini = time.time()
    while True:
        stdscr.clear()  # Clears the screen
        if spacebar_presses == 12 or spacebar_presses == 0:
            # Gets a random line from the words and an array containing the words in that sentence
            line, word_list = get_random_line(words, 12)

            spacebar_presses = 0    # Resets the spacebars
            word = ""               # Reinitializes the word = ""

        # Removes the word that is already entered by the press of a spacebar
        if word != "":
            line = line.replace(word_list[spacebar_presses - 1], "")

        # Calculates the elapsed time
        elapsed_time = time.time() - time_ini
        # Displays the line to the screen at coordinates (y:2, x:2)
        stdscr.addstr(2, 2, line.strip())
        # Displays the time elapsed to the screen at coordinates (y:2, x:screen_width - 4 - 2)
        stdscr.addstr(2, max_x - 2 - 4,
                      str(elapsed_time.__round__(2)) + "\n  ")

        # Resfreshes the screen so we can see the changes
        stdscr.refresh()
        word = ""
        while True:
            key = stdscr.getch()                # Gets each character entered by the user
            CHARS_PRESSED += 1
            # Adds the entered character to the word
            word += chr(key)
            if key == curses.KEY_BACKSPACE:     # If the key pressed is a spacebar so the words loses its last two characters to account for the character removal
                word = word[:-2]

            # If the spacebar is pressed then it means the current word is done being typed
            if key == ord(' '):
                spacebar_presses += 1
                # word gets added to the USER_LINES
                USER_WORDS.append(word)
                break

            if elapsed_time > TEST_DURATION:    # If during anytime if the time exceeds the TEST_DURATION then the test ends
                return

        if elapsed_time > TEST_DURATION:
            return


def prepare_results():
    """ Prepares and displays the results """
    wrong_words = 0
    correct_words = 0
    total_words = 0
    for i in range(len(ALL_WORDS)):
        # Runs only till the USER_LINES is not out of index.
        try:
            # If the word entered by the user matches the word asked by the system then its marked as true
            if ALL_WORDS[i].strip() == USER_WORDS[i].strip():
                correct_words += 1
            # Else its added to and marked as wrong word
            else:
                wrong_words += 1
        except IndexError:
            break
        total_words += 1

    print("<-- Results -->")
    print("\tWords per Minute (WPM):", correct_words)
    print("\tTotal Words:", total_words)
    print("\tIncorrect Words:", wrong_words)
    print("\tAccuracy:", (correct_words / total_words * 100).__round__(2))
    print("\tTotal Characters Entered:", CHARS_PRESSED)


def read_file(path='./words.txt'):
    """ Reads the files and returns the array of words in the file """
    words = []
    # Simply reads the file 'words.txt' and turns the words array
    with open(path, 'r') as f:
        for word in f.readlines():
            words.append(word.strip())

    return words


def get_random_line(words, words_in_line=12):
    """ Returns a tuple of a randomly generated line and an array of words contained by that line """
    global ALL_WORDS
    line = ""
    word_list = []
    for _ in range(words_in_line):
        # Finds a random number b/w 0 and (length of words) -1
        random_int = random.randint(0, len(words) - 1)
        # Finds a random word ursing the random number from the words array
        random_word = words[random_int]
        line += random_word + " "                       # Adds the word to the line
        # Adds the word to ALL_LINES
        ALL_WORDS.append(random_word)
        # Adds the word to word_list
        word_list.append(random_word)

    # returns the line and words_list
    return line.strip(), word_list


def clear():
    """ Clears the screen """
    # clears the screen depending upon the platform (linux/windows)
    os.system("cls" if sys.platform == 'win32' else 'clear')


def start_timer(timer=10):
    """ Sets the timer for timer seconds defaulted to 10 """
    counter = 0
    # Starts a timer for timer seconds and clears the screen for the test
    while counter < timer:
        print("Starting in", timer - counter)
        time.sleep(1)
        counter += 1
        clear()


if __name__ == "__main__":
    # Calls the main function for program to proceed
    main()
