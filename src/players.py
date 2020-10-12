import random
import math
from game import WHITE, BLACK
from mcts import MCTS
import numpy as np


class Player:
    def __init__(self, col):
        self.col = col

    def select_move(self, moves, game):
        """
        Selects the best move depending on the possible moves and the game state
        """


class RandomPlayer(Player):
    def select_move(self, moves, game):
        return random.choice(moves)


class HumanPlayer(Player):
    def select_move(self, moves, game):
        print("Valid Moves:", moves)
        move = None
        print("Please enter your move: ")
        while move is None:
            print("From:", end=" ")
            fr = input().lower()
            print("To:", end=" ")
            to = input().lower()
            for mv in moves:
                if fr in mv.__str__() and to in mv.__str__():
                    move = mv
            if move is None:
                print("Please enter a move:")
        return move


class MinimaxPlayer(Player):
    def select_move(self, moves, game):
        def static_eval(board):
            wp = 0
            bp = 0
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col] == WHITE:
                        wp += 1
                    elif board[row][col] == BLACK:
                        bp += 1
            return wp - bp

        def minimax(game, depth, alpha, beta, col):
            if depth == 0:
                return static_eval(game.board), None

            valid_moves = game.generate_valid_moves()
            game_over, winner = game.check_terminal(valid_moves)
            if game_over:
                if winner == WHITE:
                    return math.inf, None
                if winner == BLACK:
                    return -math.inf, None
                return 0, None

            assert len(valid_moves) > 0

            best_eval = 0
            best_move = valid_moves[0]
            if col == WHITE:
                best_eval = -math.inf
                for move in valid_moves:
                    game.apply_move(move)
                    ev, _ = minimax(game, depth - 1, alpha, beta, -col)
                    game.unapply_move(move)

                    if ev > best_eval:
                        best_eval = ev
                        best_move = move
                    alpha = max(alpha, best_eval)
                    if beta <= alpha:
                        break
            else:
                best_eval = math.inf
                for move in valid_moves:
                    game.apply_move(move)
                    ev, _ = minimax(game, depth - 1, alpha, beta, -col)
                    game.unapply_move(move)

                    if ev < best_eval:
                        best_eval = ev
                        best_move = move
                    beta = min(beta, best_eval)
                    if beta <= alpha:
                        break

            return best_eval, best_move

        _, best_move = minimax(game, 12, -math.inf, math.inf, self.col)
        return best_move


class MCTSPlayer(Player):
    def __init__(self, col, policy_value_function, c_puct=5, n_playout=2000, is_selfplay=0):
        self.col = col
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self.is_selfplay = is_selfplay
    
    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def select_move(self, moves, game, temp=1e-3, return_prob=0):
        # the pi vector returned by MCTS as in the AlphaGo Zero paper
        move_probs = np.zeros(8 * 8)
        acts, probs = self.mcts.get_move_probs(game, temp)
        move_probs[list(acts)] = probs
        if self.is_selfplay:
            # add Dirichlet Noise for exploration (needed for
            # self-play training)
            move = np.random.choice(acts, p = 0.75 * probs + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs))))
            # update the root node and reuse the search tree
            self.mcts.update_with_move(move)
        else:
            # with the default temp=1e-3, it is almost equivalent
            # to choosing the move with the highest prob
            move = np.random.choice(acts, p=probs)
            # reset the root node
            self.mcts.update_with_move(-1)
            # location = board.move_to_location(move)
            # print("AI move: %d,%d\n" % (location[0], location[1]))

        if return_prob:
            return move, move_probs
        else:
            return move

    def __str__(self):
        return "MCTS {}".format(self.player)

