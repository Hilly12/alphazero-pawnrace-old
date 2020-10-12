from move import Move
import numpy as np

WHITE = 1
BLACK = -1
EMPTY = 0


class Game:
    def __init__(self, gap_white, gap_black):
        self.board = [[0] * 8 for i in range(8)]
        self.enpassant_col = -1
        self.turn = 1
        self.moves = []

        # Turing Test

        # self.board[1][1] = WHITE
        # self.board[2][2] = WHITE
        # self.board[2][3] = WHITE

        # self.board[4][1] = BLACK
        # self.board[4][2] = BLACK
        # self.board[4][3] = BLACK

        # Normal Board

        # for i in range(0, 8):
        #     self.board[1][i] = WHITE

        # self.board[1][gap_white] = 0

        # for i in range(0, 8):
        #     self.board[6][i] = BLACK

        # self.board[6][gap_black] = 0

    def get_current_color(self):
        return WHITE if self.turn % 2 == 1 else BLACK

    def generate_valid_moves(self): # pylint disable=too-many-branches
        color = self.get_current_color()
        moves = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] == color and color == WHITE:
                    if row == 1 and self.board[row + 1][col] == EMPTY and self.board[row + 2][col] == EMPTY:
                        moves.append(Move((row, col), (row + 2, col), False, False))
                    if row < 7 and self.board[row + 1][col] == EMPTY:
                        moves.append(Move((row, col), (row + 1, col), False, False))
                    if row < 7 and col < 7 and self.board[row + 1][col + 1] == BLACK:
                        moves.append(Move((row, col), (row + 1, col + 1), True, False))
                    if row < 7 and col > 0 and self.board[row + 1][col - 1] == BLACK:
                        moves.append(Move((row, col), (row + 1, col - 1), True, False))
                    if row == 4 and col < 7 and self.board[row][col + 1] == BLACK and self.enpassant_col == col + 1:
                        moves.append(Move((row, col), (row + 1, col + 1), True, True))
                    if row == 4 and col > 0 and self.board[row][col - 1] == BLACK and self.enpassant_col == col - 1:
                        moves.append(Move((row, col), (row + 1, col - 1), True, True))
                elif self.board[row][col] == color and color == BLACK:
                    if row == 6 and self.board[row - 1][col] == EMPTY and self.board[row - 2][col] == EMPTY:
                        moves.append(Move((row, col), (row - 2, col), False, False))
                    if row > 0 and self.board[row - 1][col] == EMPTY:
                        moves.append(Move((row, col), (row - 1, col), False, False))
                    if row > 0 and col < 7 and self.board[row - 1][col + 1] == WHITE:
                        moves.append(Move((row, col), (row - 1, col + 1), True, False))
                    if row > 0 and col > 0 and self.board[row - 1][col - 1] == WHITE:
                        moves.append(Move((row, col), (row - 1, col - 1), True, False))
                    if row == 3 and col < 7 and self.board[row][col + 1] == WHITE and self.enpassant_col == col + 1:
                        moves.append(Move((row, col), (row - 1, col + 1), True, True))
                    if row == 3 and col > 0 and self.board[row][col - 1] == WHITE and self.enpassant_col == col - 1:
                        moves.append(Move((row, col), (row - 1, col - 1), True, True))
        return moves

    def apply_move(self, move):
        self.moves.append(move)

        occupant = self.board[move.fr[0]][move.fr[1]]
        self.board[move.to[0]][move.to[1]] = occupant
        self.board[move.fr[0]][move.fr[1]] = EMPTY

        self.enpassant_col = move.to[1] if move.is_double_push() else -1

        if move.enpassant:
            self.board[move.fr[0]][move.to[1]] = EMPTY

        self.turn += 1

    def unapply_move(self, move):
        self.moves.pop()

        occupant = self.board[move.to[0]][move.to[1]]
        self.board[move.to[0]][move.to[1]] = EMPTY
        self.board[move.fr[0]][move.fr[1]] = occupant

        last_move = self.moves[-1]
        self.enpassant_col = last_move.to[1] if last_move.is_double_push() else -1

        other = -occupant
        if move.enpassant:
            self.board[move.fr[0]][move.to[1]] = other
        elif move.capture:
            self.board[move.to[0]][move.to[1]] = other

        self.turn -= 1

    def get_canonical(self):
        tensor = np.zeros((4, 8, 8))
        val = self.turn % 2
        last_move = self.moves[-1].to
        for x in range(0, 8):
            for y in range(0, 8):
                if self.board[x][y] == WHITE:
                    tensor[0][x][y] = 1
                if self.board[x][y] == BLACK:
                    tensor[1][x][y] = 1
                if last_move[0] == x and last_move[1] == y:
                    tensor[2][x][y] = 1
                tensor[3][x][y] = val

        return tensor

    def check_terminal(self, moves):
        if len(moves) == 0:
            return True, EMPTY
        for i in range(0, 8):
            if self.board[0][i] == BLACK:
                return True, BLACK
        for i in range(0, 8):
            if self.board[7][i] == WHITE:
                return True, WHITE
        return False, EMPTY

    def __str__(self):
        s = "  a b c d e f g h\n"
        for row in range(0, 8):
            r = str(row + 1) + " "
            for col in range(0, 8):
                n = self.board[row][col]
                if n == WHITE:
                    r += "W"
                elif n == BLACK:
                    r += "B"
                else:
                    r += "-"
                r += " "
            s += r + "\n"
        return s
