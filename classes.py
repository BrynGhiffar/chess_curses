#!/usr/bin/python3
import curses

# TODO: implement enpassant DONE
# TODO: implement castling move DONE
# TODO: implement checking, you can't move any pieces that doesn't 
#       make your king safe
# TODO: implement safe king moving, your king cannot move to a square
#       that is attacked. This has to be embedded into the move of every
#       piece
# TODO: implement check mating. The computer can recognize once
#       there are no moves that can save the king.
# TODO: implement stalemating. The game can recognize once
#       there are no moves that can be made by the current player
# TODO: implement pawn promotion
# TODO: Make you code better!

SQR = 8

# From the board the pieces will deduce how
# to make the move. For each piece is responsible
# to coordinate themselves on how they operate

# Each piece looks at the board to determine
# What are their valid moves.

# defines how the board is controlled
class Control:

    # * The Control determine the players turns
    # * The Controls controls the cursor
    # * THe Control controls the the current selected piece
    # * The Control controls the board

    def __init__(self):

        # Below are the constants for the twelve pieces in the board
        self.WR, self.WKN, self.WB, self.WQ, self.WK, self.WP,\
        self.BR, self.BKN, self.BB, self.BQ, self.BK, self.BP = list(range(12)) 

        self.EP = -1
        self.brd = [
        [self.BR, self.BKN, self.BB, self.BQ, self.BK, self.BB, self.BKN, self.BR],
        [self.BP, self.BP, self.BP, self.BP, self.BP, self.BP, self.BP, self.BP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP, self.EP],
        [self.WP, self.WP, self.WP, self.WP, self.WP, self.WP, self.WP, self.WP],
        [self.WR, self.WKN, self.WB, self.WQ, self.WK, self.WB, self.WKN, self.WR]]

        self.WHITE = 0
        self.BLACK = 1
        self.turn = self.WHITE
        self.curs_loc = [0, 0] # CPs(0, 0)
        self.pce_loc = [-1, -1]
        self.moves = []

        # -- for enpassant --
        self.last_pawn_skip = -1 # the column of the pawn which skipped in
                                    # the last move, if no pawns skip
                                    # then value equals to -1.

        self.has_king_moved = [False, False]
        # self.has_king_moved[self.WHITE] = whether the white king has moved
        # self.has_king_moved[self.BLACK] = whether the black king has moved

        # -- for castling --
        self.has_rook_moved = [[False, False],
                               [False, False]]
        # self.has_rook_moved[self.WHITE][0] = has leftmost white rook moved
        # self.has_rook_moved[self.WHITE][1] = has rightmost white rook moved
        # self.has_rook_moved[self.BLACK][0] = has leftmost black rook moved
        # self.has_rook_moved[self.BLACK][1] = has rightmost black rook moved

    def get_current_player(self):
        return self.turn

    def n_plyr(self):
        """returns the next player of the current turn"""
        return (self.turn + 1) % 2

    def toggle_player_turn(self):
        self.turn = self.n_plyr()

    def get_ally_func(self):
        """returns a function which test's whether a piece is an ally
        based on turn"""
        if self.turn == self.WHITE:
            return self.is_white
        else:
            return self.is_black

    def get_attacking_square(self, cp):
        """returns all the squares attacked by
        the piece at position cp"""
        piece = self.brd[cp[0]][cp[1]]
        attacks = []
        if piece != self.EP:
            t = [self.WHITE, self.BLACK][self.is_black(cp)]
            if piece in [self.WP, self.BP]:
                # diagonal capture
                dc1 = (pc_pos[0] + [-1, 1][t], pc_pos[1] + [-1, 1][t])
                if self.is_within_bounds(dc1) and is_sqr_enemy(dc1):
                    attacks.append(dc1)

                dc2 = (pc_pos[0] + [-1, 1][t], pc_pos[1] + [1, -1][t])
                if self.is_within_bounds(dc2) and is_sqr_enemy(dc2):
                    attacks.append(dc2)
            elif piece in [self.WR, self.BR]:
                pass
            elif piece in [self.WKN, self.BKN]:
                pass
            elif piece in [self.WB, self.BB]:
                pass
            elif piece in [self.WQ, self.BQ]:
                pass
            elif piece in [self.WK, self.BK]:
                pass
        pass

    def get_all_attacking_square(self, side):
        """returns all the squares attacked by side"""
        pass

    def toggle_select_piece(self):
        """toggles the selected piece to point to a certain piece
        or point to nothing at all. points to nothing when
        self.pce_loc == [-1, -1]"""
        piece = self.brd[self.curs_loc[0]][self.curs_loc[1]]
        if (piece != self.EP) and (self.get_ally_func()(piece)):
            self.pce_loc = self.curs_loc[:]
            self.moves = self.get_valid_move()
            # print(self.last_pawn_skip)
        else:
            self.pce_loc = [-1, -1]
            self.moves = []

    def is_enpassant(self, cp, tp):
        """returns true if the move being played is an enpassant"""
        is_enemy_pawn = self.brd[cp[0]][tp[1]] == [self.WP, self.BP][self.n_plyr()]
        return is_enemy_pawn and self.last_pawn_skip == tp[1]

    def move(self, cp, tp):
        """moves piece from location cp to location
        tp"""
        self.brd[cp[0]][cp[1]],\
        self.brd[tp[0]][tp[1]] =\
        self.EP, self.brd[cp[0]][cp[1]]

    def make_empty(self, tp):
        """sets board at position tp to empty"""
        self.brd[tp[0]][tp[1]] = self.EP

    def is_pawn(self, p):
        return self.brd[p[0]][p[1]] in [self.WP, self.BP]
    
    def is_king(self, p):
        return self.brd[p[0]][p[1]] in [self.WK, self.BK]

    def is_rook(self, p):
        return self.brd[p[0]][p[1]] in [self.WR, self.BR]

    def is_right_castling(self, cp, tp):
        t = self.turn
        r = (7, 0)[t]
        c = 4
        not_moved = not self.has_king_moved[t] and\
                    not self.has_rook_moved[t][1]
        king_correct_pos = (cp[0] == r) and (cp[1] == c)
        rook_correct_pos = self.brd[r][7] == (self.WR, self.BR)[t]
        all_correct_pos = king_correct_pos and rook_correct_pos
        empty_right = [self.is_sqr_ep((r, i)) for i in range(c + 1, 7)]

        is_king = self.is_king(cp)
        col_move = tp[1] - cp[1] == 2
        row_move = cp[0] - tp[0] == 0
        return is_king and col_move and row_move and all(empty_right)\
             and not_moved and all_correct_pos

    def is_left_castling(self, cp, tp):
        t = self.turn
        r = (7, 0)[t]
        c = 4
        not_moved = not self.has_king_moved[t] and\
                    not self.has_rook_moved[t][0]
        king_correct_pos = (cp[0] == r) and (cp[1] == c)
        rook_correct_pos = self.brd[r][0] == (self.WR, self.BR)[t]
        all_correct_pos = king_correct_pos and rook_correct_pos
        empty_left = [self.is_sqr_ep((r, i)) for i in range(1, c)]

        is_king = self.is_king(cp)
        col_move = cp[1] - tp[1] == 2
        row_move = cp[0] - tp[0] == 0
        return is_king and col_move and row_move and all(empty_left)\
            and not_moved and all_correct_pos

    def move_piece(self):
        """move selected piece on pce_loc to 
        curs_loc if curs_loc is a valid move"""
        tp = tuple(self.curs_loc) # target move
        cp = tuple(self.pce_loc) # current piece location


        if tp in self.moves:
            piece = self.brd[cp[0]][cp[1]]

            # when the move being done is an enpassant
            if self.is_pawn(cp) and self.is_enpassant(cp, tp):
                self.move(cp, tp)
                ep = (tp[0] + (1, -1)[self.turn], tp[1]) # enemy position
                self.make_empty(ep)
                self.toggle_player_turn()
                return

            # when the move being done is a right castle
            if self.is_right_castling(cp, tp):
                self.move(cp, tp)
                self.make_empty(((7, 0)[self.turn], 7))
                self.brd[tp[0]][tp[1] - 1] = (self.WR, self.BR)[self.turn]
                self.toggle_player_turn()
                return

            # when the move being done is a left castle
            if self.is_left_castling(cp, tp):
                self.move(cp, tp)
                self.make_empty(((7, 0)[self.turn], 0))
                self.brd[tp[0]][tp[1] + 1] = (self.WR, self.BR)[self.turn]
                self.toggle_player_turn()
                return

            # when the move being done is a pawn skip
            do_pawn_skip = lambda cp, tp : tp[0] == cp[0] + [-2, 2][self.turn]
            if self.is_pawn(cp) and do_pawn_skip(cp, tp):
                self.last_pawn_skip = tp[1]
            else:
                self.last_pawn_skip = -1

            # when the king moves we want to tell the game the king has moved
            if self.is_king(cp):
                self.has_king_moved[self.turn] = True
            
            if self.is_rook(cp):
                if cp == (7, 0) and self.turn == self.WHITE:
                    self.has_rook_moved[self.WHITE][0] = True
                elif cp == (7, 7) and self.turn == self.WHITE:
                    self.has_rook_moved[self.WHITE][1] = True
                elif cp == (0, 0) and self.turn == self.BLACK:
                    self.has_rook_moved[self.BLACK][0] = True
                elif cp == (0, 7) and self.turn == self.BLACK:
                    self.has_rook_moved[self.BLACK][1] = True


            self.move(cp, tp)
            self.toggle_player_turn()
        
    def empty_board(self):
        """clears the board of all the pieces"""
        self.brd = [[self.EP for _ in range(SQR)] for _ in range(SQR)]

    def move_curs_right(self):
        """moves the cursor right"""
        if self.curs_loc[1] + 1 < SQR:
            self.curs_loc[1] += 1

    def move_curs_left(self):
        """moves the cursor left"""
        if self.curs_loc[1] - 1 >= 0:
            self.curs_loc[1] -= 1

    def move_curs_down(self):
        """moves the cursor down"""
        if self.curs_loc[0] + 1 < SQR:
            self.curs_loc[0] += 1

    def move_curs_up(self):
        """moves the cursor up"""
        if self.curs_loc[0] - 1 >= 0:
            self.curs_loc[0] -= 1

    def is_white(self, piece):
        return piece <= 5 and piece >= 0

    def is_black(self, piece):
        return piece > 5 and piece < 12

    def is_pawn_first_move(self, pc_pos):
        piece = self.brd[pc_pos[0]][pc_pos[1]]
        if piece == self.WP:
            return pc_pos[0] == 6
        else:
            return pc_pos[0] == 1

    def is_within_bounds(self, p):
        return 0 <= p[0] < SQR and 0 <= p[1] < SQR

    def is_sqr_ep(self, p):
        return self.brd[p[0]][p[1]] == self.EP

    def get_pawn_march_moves(self, cp, t):
        """returns the marching forward move of the pawn
        based on side and position"""
        moves = []
        fm = (cp[0] + [-1, 1][t], cp[1])
        if self.is_within_bounds(fm) and self.is_sqr_ep(fm):
            moves.append(fm)

            sm = ([4, 3][t], cp[1])
            if self.is_pawn_first_move(cp) and self.is_sqr_ep(sm):
                moves.append(sm)
        return moves
    
    def get_pawn_diagonal_capture_moves(self, cp, t, is_sqr_enemy):
        # diagonal capture
        moves = []
        dc1 = (cp[0] + [-1, 1][t], cp[1] + [-1, 1][t])
        if self.is_within_bounds(dc1) and is_sqr_enemy(dc1):
            moves.append(dc1)

        dc2 = (cp[0] + [-1, 1][t], cp[1] + [1, -1][t])
        if self.is_within_bounds(dc2) and is_sqr_enemy(dc2):
            moves.append(dc2)
        return moves

    def get_pawn_enpassant_capture_moves(self, cp, t):
        moves = []
        ec1 = (cp[0] + [-1, 1][t], cp[1] + [-1, 1][t])
        if self.is_within_bounds(ec1) and self.is_enpassant(cp, ec1):
            moves.append(ec1)

        ec2 = (cp[0] + [-1, 1][t], cp[1] + [1, -1][t])
        if self.is_within_bounds(ec2) and self.is_enpassant(cp, ec2):
                moves.append(ec2)
        return moves
    
    def get_rook_moves(self, cp, is_sqr_ally, is_sqr_enemy):
        moves = []
        for d in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            r, c = cp
            tp = (r + d[0], c + d[1]) # target position
            while self.is_within_bounds(tp) and not is_sqr_ally(tp):
                moves.append(tp)
                if is_sqr_enemy(tp):
                    break
                tp = (tp[0] + d[0], tp[1] + d[1])
        return moves

    def get_knight_moves(self, cp, is_sqr_ally):
        moves = []
        for s in [(-1, 1), (1, -1), (1, 1), (-1, -1)]:
            for d in [(2, 1), (1, 2)]:
                tp = (cp[0] + d[0] * s[0], cp[1] + d[1] * s[1])
                if self.is_within_bounds(tp) and not is_sqr_ally(tp):
                    moves.append(tp)
        return moves

    def get_bishop_moves(self, cp, is_sqr_ally, is_sqr_enemy):
        moves = []
        for d in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = cp
            tp = (r + d[0], c + d[1]) # target position
            while self.is_within_bounds(tp) and not is_sqr_ally(tp):
                moves.append(tp)
                if is_sqr_enemy(tp):
                    break
                tp = (tp[0] + d[0], tp[1] + d[1])
        return moves
    
    def get_king_moves(self, cp, is_sqr_ally):
        moves = []
        r, c = cp
        for d in [(1, 1), (1, -1), (-1, 1), (-1, -1),
                  (0, -1), (0, 1), (1, 0), (-1, 0)]:
            tp = (r + d[0], c + d[1])
            if self.is_within_bounds(tp) and not is_sqr_ally(tp):
                moves.append(tp)
        return moves

    def get_king_castling_move(self, cp, t):
        moves = []
        r, c = (7, 0)[t], 4
        tp = (r, c - 2)
        if self.is_left_castling(cp, tp):
            moves.append((r, c - 2))
        tp = (r, c + 2)
        if self.is_right_castling(cp, tp):
            moves.append((r, c + 2))
        return moves

    def get_valid_move_aux(self, pc_pos, is_ally, is_enemy):
        """generates valid moves for selected piece"""
        moves = []
        selected_piece = self.brd[pc_pos[0]][pc_pos[1]]
        t = self.turn

        # does this square contain an enemy piece
        is_sqr_enemy = lambda p : is_enemy(self.brd[p[0]][p[1]])

        # does this square contain an ally piece
        is_sqr_ally = lambda p : is_ally(self.brd[p[0]][p[1]])

        if selected_piece in [self.WP, self.BP]:

            moves.extend(self.get_pawn_march_moves(pc_pos, t))

            moves.extend(
                self.get_pawn_diagonal_capture_moves(pc_pos, t, is_sqr_enemy))

            moves.extend(self.get_pawn_enpassant_capture_moves(pc_pos, t))

        elif selected_piece in [self.WR, self.BR]:
            moves.extend(
                self.get_rook_moves(pc_pos, is_sqr_ally, is_sqr_enemy))

        elif selected_piece in [self.WKN, self.BKN]:
            moves.extend(self.get_knight_moves(pc_pos, is_sqr_ally))

        elif selected_piece in [self.WB, self.BB]:
            moves.extend(
                self.get_bishop_moves(pc_pos, is_sqr_ally, is_sqr_enemy))

        elif selected_piece in [self.WQ, self.BQ]:
            moves.extend(
                self.get_rook_moves(pc_pos, is_sqr_ally, is_sqr_enemy))
            moves.extend(
                self.get_bishop_moves(pc_pos, is_sqr_ally, is_sqr_enemy))

        elif selected_piece in [self.WK, self.BK]:
            moves.extend(self.get_king_moves(pc_pos, is_sqr_ally))
            moves.extend(self.get_king_castling_move(pc_pos, t))
        return moves

    def get_valid_move(self):
        # returns array of legal positions
        pc_pos = self.pce_loc
        selected_piece = self.brd[pc_pos[0]][pc_pos[1]]
        moves = []
        if self.is_white(selected_piece):

            # find legal next moves for that particular black piece
            moves.extend(self.get_valid_move_aux(pc_pos, self.is_white, self.is_black))
            pass
        elif self.is_black(selected_piece):

            # find legal next moves for that particular white piece
            moves.extend(self.get_valid_move_aux(pc_pos, self.is_black, self.is_white))
            pass
        return moves

class Display(Control):

    def __init__(self, stdscr):
        super().__init__()

        self.stdscr = stdscr
        self.BOARD_POS = (0, 0) # dimension of board is 40 rows x 72 columns
        self.CHR_PR_COL = 9
        self.CHR_PR_ROW = 5
        # determines the color of the board
        self.CLR_BRD = [[(i + j) % 2 for j in range(SQR)]\
                            for i in range(SQR)]

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

        self.AWK = [  '   _+_   ', # Each piece has dimensions w x h : 5 x 5
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

        # colors

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
        col = self.CHR_PR_COL
        row = self.CHR_PR_ROW
        square = SQR
        empty = self.EP
        pb = self.brd
        cb = self.CLR_BRD
        ap = self.ALL_PIECES
        # texture = [' ', '█']
        texture = [' ', ':']
        curses.init_pair(1, -1, curses.COLOR_CYAN) # selected_cursor
        curses.init_pair(2, -1, curses.COLOR_GREEN) # selected_piece
        curses.init_pair(3, -1, curses.COLOR_YELLOW) # moves

        for _ in range(col * square + 2):
            self.stdscr.addstr(':')
        self.stdscr.addstr('\n')

        for i in range(row * square):
            self.stdscr.addstr(':')
            for j in range(col * square):
                is_slt_piece = [ i // row, j // col ] == self.pce_loc
                is_slt_curs = [i // row, j // col] == self.curs_loc
                is_move_sqr = (i // row, j // col) in self.moves

                if is_slt_piece:
                    self.stdscr.attron(curses.color_pair(2))
                if is_move_sqr:
                    self.stdscr.attron(curses.color_pair(3))
                if is_slt_curs:
                    self.stdscr.attron(curses.color_pair(1))

                if pb[i // row][j // col] == empty:
                    self.stdscr.addstr(texture[cb[i // row][j // col]])
                else:
                    self.stdscr.addstr(ap[cb[i // row][j // col]]\
                          [pb[i // row][j // col]][i % row][j % col])

                self.stdscr.attroff(curses.color_pair(1))
                self.stdscr.attroff(curses.color_pair(2))
                self.stdscr.attroff(curses.color_pair(3))
            # print(":")
            self.stdscr.addstr(':\n')

        for _ in range(col * square + 2):
            self.stdscr.addstr(':')
        self.stdscr.addstr('\n')


class Interface(Display):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.key_right = ord('l')
        self.key_left = ord('h')
        self.key_up = ord('k')
        self.key_down = ord('j')
        self.key_toggle_select = ord(' ')

    def on_key_press(self, key):
        if key == self.key_right:
            self.move_curs_right()
        elif key == self.key_left:
            self.move_curs_left()
        elif key == self.key_down:
            self.move_curs_down()
        elif key == self.key_up:
            self.move_curs_up()
        elif key == self.key_toggle_select:
            self.move_piece()
            self.toggle_select_piece()
        pass

    def play(self):
        quit = False
        while not quit:
            self.stdscr.clear()
            self.draw_board()
            key = self.stdscr.getch()
            self.on_key_press(key)
            if key == ord('q'):
                quit = True

def main():
    c = Control()
    c.turn = c.BLACK
    c.curs_loc = (1, 1)
    print(c.get_valid_move())
    pass

if __name__ == '__main__':
    main()
