#!/usr/bin/python3
import curses
from classes import Display, Interface

def main(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    maxy, maxx = stdscr.getmaxyx()
    # Display(stdscr).draw_board()
    # stdscr.getch()
    Interface(stdscr).play()
    pass

if __name__ == '__main__':
    # main()
    curses.wrapper(main)

