#!/usr/bin/env python3

import os
import sys

def hr(char, cols):
    line = ''
    
    # Append char to line until it's greater than char
    while len(line) < cols:
        line += char

    # Clip some off in case cols isn't a multiple of length of char
    print(line[:cols]) 

def main():
    # Get the size of the terminal
    rows, columns = os.popen('stty size', 'r').read().split()

    # If there are command line arguments, use those, else just use '#'
    if len(sys.argv) > 1:
        chars = sys.argv[1:]
    else:
        chars = ['#']


    # Loop though and print a seperate line for each
    for value in chars:
        hr(value, int(columns))


if __name__ == '__main__':
    main()
