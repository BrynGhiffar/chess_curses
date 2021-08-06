#!/usr/bin/python3
import curses
from classes import Interface

def debug_rook(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WR
    game.brd[0][1] = game.BR
    # print(game.brd)
    game.play()
    pass


def debug_knight(stdscr)

def debug_bishop(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WB
    game.brd[0][1] = game.BB
    game.play()

if __name__ == '__main__':
    # test_rook()
    curses.wrapper(debug_rook)
