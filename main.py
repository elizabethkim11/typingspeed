import curses
from curses import wrapper #allows to initialize module, restores terminal back to previous state later
from pydoc import stripid
import stringprep 
import time
import random

def startScreen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the typing speed test!\n")
    stdscr.addstr("Correctly typed characters will show up in blue, while incorrectly typed characters will show up in pink.\n")
    stdscr.addstr("When you have completed *correctly* typing the target text, don't forget to press enter to see your typing speed!\n")
    stdscr.addstr("(You must reproduce the text exactly as written to complete the test.)\n")
    stdscr.addstr("Press any key to begin.")
    stdscr.refresh()
    stdscr.getkey()

def textOverlay(stdscr, target, input, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}") #easy concatenation of strings, curly braces evaluate as string

    for i, char in enumerate(input):
        correct = target[i]
        color = curses.color_pair(1)
        if char != correct:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color) #overlay on top of target text

def loadText():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines)

def speed(stdscr):
    target = loadText()
    input = []
    wpm = 0
    startTime = time.time()
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startTime, 1) #if speed is 0, gives 1 to avoid division by 0
        wpm = round((len(input) / (timeElapsed / 60)) / 5) #avg word has 5 char

        stdscr.clear()
        textOverlay(stdscr, target, input, wpm)
        stdscr.refresh()

        if "".join(input) == target:
            stdscr.nodelay(False)
            break

        try: 
            key = stdscr.getkey() #blocking, waits for user to input a key before doing anything
        except:
            continue


        if ord(key) == 27: #ascii of esc key is 27 so user can exit game
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"): #different representations of backspace key
            if len(input) > 0:
                input.pop() #get rid of last key we input
        elif len(input) < len(target):
            input.append(key)

def main(stdscr): #allows to write stuff to screen
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #id 1, foreground blue if correct, background black
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) #magenta if incorrect
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    startScreen(stdscr)

    while True:
        speed(stdscr)
        stdscr.addstr(2, 0, "Great job! Press any key to play again!")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main) #call main while initializing

