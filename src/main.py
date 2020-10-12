import random
from game import Game
from game import WHITE, BLACK
from players import HumanPlayer, MinimaxPlayer, MCTSPlayer
from policy_value import PolicyValueNet

g = Game(random.randint(0, 7), random.randint(0, 7))
white = HumanPlayer(WHITE)
# black = MinimaxPlayer(BLACK)
best_policy = PolicyValueNet()
black = MCTSPlayer(BLACK, best_policy.policy_value_fn, c_puct=5, n_playout=400)

while True:
    moves = g.generate_valid_moves()
    game_over, winner = g.check_terminal(moves)
    if game_over:
        if winner == WHITE:
            print("White wins!")
        elif winner == BLACK:
            print("Black wins!")
        else:
            print("Stalemate!")
        break

    col = WHITE if g.turn % 2 == 1 else BLACK
    if col == WHITE:
        print("White to play:")
        print(g)
        move = white.select_move(moves, g)
        g.apply_move(move)
        print("White played", move)
    else:
        print("Black to play:")
        print(g)
        move = black.select_move(moves, g)
        g.apply_move(move)
        print("Black played", move)
    print()
