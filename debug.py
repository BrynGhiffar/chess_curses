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

def debug_knight(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WKN
    game.brd[0][1] = game.BKN
    game.play()

def debug_bishop(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WB
    game.brd[0][1] = game.BB
    game.play()

def debug_queen(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WQ
    game.brd[0][1] = game.BQ
    game.play()

def debug_king(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[0][0] = game.WK
    game.brd[7][7] = game.BK
    game.play()

def debug_castling(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    game = Interface(stdscr)
    game.empty_board()
    game.brd[7][0] = game.WR
    game.brd[7][4] = game.WK
    game.brd[7][7] = game.WR
    for i in range(8):
        game.brd[6][i] = game.WP

    game.brd[0][0] = game.BR
    game.brd[0][4] = game.BK
    game.brd[0][7] = game.BR
    for i in range(8):
        game.brd[1][i] = game.BP
    game.play()

if __name__ == '__main__':
    # curses.wrapper(debug_rook)
    # curses.wrapper(debug_knight)
    # curses.wrapper(debug_bishop)
    # curses.wrapper(debug_queen)
    # curses.wrapper(debug_king)
    curses.wrapper(debug_castling)
