#!/usr/bin/python3
class ChessBoard:

    def __init__(self):

        self.SQR = 8 # chess board is 8 x 8
        self.CHR_PR_COL = 9
        self.CHR_PR_ROW = 5
        # determines the color of the board
        self.CLR_BRD = [[(i + j) % 2 for j in range(self.SQR)]\
                            for i in range(self.SQR)]

        # Below are the constants for the twelve pieces in the board
        self.WR, self.WKN, self.WB, self.WQ, self.WK, self.WP,\
        self.BR, self.BKN, self.BB, self.BQ, self.BK, self.BP = list(range(12)) 

        self.EP = -1
        self.pieces_board = [
        [self.BR, self.EP, self.BB, self.BQ, self.BK, self.BB, self.BKN, self.BR],
        [self.BP, self.BP, self.BP, self.BP, self.BP, self.BP, self.BP, self.BP],
        [self.EP, self.EP, self.BKN, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.WP, self.WP, self.WP, self.WP, self.WP, self.WP, self.WP, self.WP],
        [self.WR, self.WKN, self.WB, self.WQ, self.WK, self.WB, self.WKN, self.WR]]
        
        self.ABK = [  '   _+_   ', # Each piece has dimensions w x h : 5 x 5
                      '   )@(   ',
                      '   |@|   ',
                      '   |@|   ',
                      '  /@@@\\  ']
        self.ABQ = [  '   www   ',
                      '   )@(   ',
                      '   |@|   ',
                      '   |@|   ',
                      '  /@@@\\  ' ]
        self.ABB= [   '         ',
                      '   (/)   ',
                      '   |@|   ',
                      '   |@|   ',
                      '  /@@@\\  ']
        self.ABKN = [ '         ',
                      '   _,,   ',
                      '  "- \~  ',
                      '   |@|   ',
                      '  /@@@\\  ']
        self.ABR = [  '         ',
                      '  |_|_|  ',
                      '   |@|   ',
                      '   |@|   ',
                      '  /@@@\\  ']
        self.ABP = [  '         ',
                      '         ',
                      '   ()    ',
                      '   )(    ',
                      '  /@@\\   ']

        self.AWK = [ '   _+_   ', # Each piece has dimensions w x h : 5 x 5
                      '   ) (   ',
                      '   | |   ',
                      '   | |   ',
                      '  /___\\  ']
        self.AWQ = [  '   www   ',
                      '   ) (   ',
                      '   | |   ',
                      '   | |   ',
                      '  /___\\  ' ]
        self.AWB = [  '         ',
                      '   (/)   ',
                      '   | |   ',
                      '   | |   ',
                      '  /___\\  ']
        self.AWKN = [ '         ',
                      '   _,,   ',
                      '  "- \~  ',
                      '   | |   ',
                      '  /___\\  ']
        self.AWR = [  '         ',
                      '  |_|_|  ',
                      '   | |   ',
                      '   | |   ',
                      '  /___\\  ']
        self.AWP = [  '         ',
                      '         ',
                      '   ()    ',
                      '   )(    ',
                      '  /__\\   ']
        self.PIECES = [self.AWR, self.AWKN, self.AWB, self.AWQ, self.AWK, self.AWP,
                       self.ABR, self.ABKN, self.ABB, self.ABQ, self.ABK, self.ABP]
        self.MASK_PIECES = [self.mask(piece) for piece in self.PIECES]
        self.ALL_PIECES = [self.PIECES, self.MASK_PIECES]

    def mask(self, ascii_piece):
        # create a copy of the piece
        piece = [[ascii_piece[i][j] for j in range(self.CHR_PR_COL)]\
                 for i in range(self.CHR_PR_ROW)]

        # modify the copy to fill the background
        for line in piece:
            # 0 to right
            i = 0
            while (i < self.CHR_PR_COL) and (line[i] == ' '):
                line[i] = ':'
                i += 1
            # self.
            i = self.CHR_PR_COL - 1
            while (i >= 0) and (line[i] == ' '):
                line[i] = ':'
                i -= 1

        # return the masked copy
        return [''.join(line) for line in piece]

    def draw_board(self):
        column = self.CHR_PR_COL
        row = self.CHR_PR_ROW
        square = self.SQR
        empty = self.EP
        pb = self.pieces_board
        cb = self.CLR_BRD
        ap = self.ALL_PIECES
        texture = [' ', ':']

        for _ in range(column * square + 2):
            print(':', end='')
        print()

        for i in range(row * square):
            print(":", end='')

            for j in range(column * square):
                if pb[i // row][j // column] == empty:
                    print(texture[cb[i // row][j // column]], end='')
                else:
                    print(ap[cb[i // row][j // column]]\
                          [pb[i // row][j // column]][i % row][j % column], end='')
            print(":")

        for _ in range(column * square + 2):
            print(':', end='')
        print()

def main():
    print("♔♕♖♗♘♙")
    print("♚♛♜♝♞♟︎")
    print("""
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:         :::::::::         :::www:::   _+_   :::::::::         ::::::::::
:  |_|_|  :: _,,:::   (/)   :::)@(:::   )@(   :::(/):::   _,,   ::|_|_|:::
:   |@|   ::"- \~::   |@|   :::|@|:::   |@|   :::|@|:::  "- \~  :::|@|::::
:   |@|   :::|@|:::   |@|   :::|@|:::   |@|   :::|@|:::   |@|   :::|@|::::
:  /@@@\  ::/@@@\::  /@@@\  ::/@@@\::  /@@@\  ::/@@@\::  /@@@\  ::/@@@\:::
::::::::::         :::::::::         :::::::::         :::::::::         :
:::::():::    ()   ::::():::    ()   ::::():::    ()   ::::():::    ()   :
:::::)(:::    )(   ::::)(:::    )(   ::::)(:::    )(   ::::)(:::    )(   :
::::/@@\::   /@@\  :::/@@\::   /@@\  :::/@@\::   /@@\  :::/@@\::   /@@\  :
::::::::::         :::::::::         :::::::::         :::::::::         :
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
:         :::::::::         :::::::::         :::::::::         ::::::::::
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
::::::::::         :::::::::         :::::::::         :::::::::         :
:         :::::::::         :::::::::         :::::::::         ::::::::::
:    ()   ::::():::    ()   ::::():::    ()   ::::():::    ()   ::::()::::
:    )(   ::::)(:::    )(   ::::)(:::    )(   ::::)(:::    )(   ::::)(::::
:   /__\  :::/__\::   /__\  :::/__\::   /__\  :::/__\::   /__\  :::/__\:::
:         :::::::::         :::::::::         :::::::::         ::::::::::
::::::::::         :::::::::   www   :::_+_:::         :::::::::         :
:::|_|_|::   _,,   :::(/):::   ) (   :::) (:::   (/)   :::_,,:::  |_|_|  :
::::| |:::  "- \~  :::| |:::   | |   :::| |:::   | |   ::"- \~::   | |   :
::::| |:::   | |   :::| |:::   | |   :::| |:::   | |   :::| |:::   | |   :
:::/___\::  /___\  ::/___\::  /___\  ::/___\::  /___\  ::/___\::  /___\  :
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """)
    BLACK_KING = [  ' _+_ ', # Each piece has dimensions w x h : 5 x 5
                    ' )@( ',
                    ' |@| ',
                    ' |@| ',
                    '/@@@\\']
    BLACK_QUEEN = [ ' www ',
                    ' )@( ',
                    ' |@| ',
                    ' |@| ',
                    '/@@@\\' ]
    BLACK_BISHOP = ['     ',
                    ' (/) ',
                    ' |@| ',
                    ' |@| ',
                    '/@@@\\']
    BLACK_KNIGHT = ['     ',
                    ' _,, ',
                    '"- \~',
                    ' |@| ',
                    '/@@@\\']
    BLACK_ROOK = [  '     ',
                    '|_|_|',
                    ' |@| ',
                    ' |@| ',
                    '/@@@\\']
    BLACK_PAWN = [  '    ',
                    '    ',
                    ' () ',
                    ' )( ',
                    '/@@\\']
    BLACK_PIECES = [BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN]

    WHITE_KING = [  ' _+_ ', # Each piece has dimensions w x h : 5 x 5
                    ' ) ( ',
                    ' | | ',
                    ' | | ',
                    '/___\\']
    WHITE_QUEEN = [ ' www ',
                    ' ) ( ',
                    ' | | ',
                    ' | | ',
                    '/___\\' ]
    WHITE_BISHOP = ['     ',
                    ' (/) ',
                    ' | | ',
                    ' | | ',
                    '/___\\']
    WHITE_KNIGHT = ['     ',
                    ' _,, ',
                    '"- \~',
                    ' | | ',
                    '/___\\']
    WHITE_ROOK = [  '     ',
                    '|_|_|',
                    ' | | ',
                    ' | | ',
                    '/___\\']
    WHITE_PAWN = [  '    ',
                    '    ',
                    ' () ',
                    ' )( ',
                    '/__\\']
    WHITE_PIECES = [WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN]
    for i in range(5):
        for piece in BLACK_PIECES:
            print(piece[i], end=' ' * 4)
        print()
    for i in range(5):
        for piece in WHITE_PIECES:
            print(piece[i], end=' ' * 4)
        print()
    ChessBoard().draw_board()

if __name__ == '__main__':
    main()
