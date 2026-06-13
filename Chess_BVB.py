import chess
import Bots
from Logging import Log
import time
#--------------------------------------------------------------#

def main(num_games):

    board = chess.Board()

    print("Progress of games complete:")
    for i in range(num_games):

        board.reset()
        move_list = []
        W_time = []
        B_time = []

        while board.is_game_over() == 0:
            WBot_s = time.time()
# Bot vs Bot
          
# White
            bot_move = Bots.bot_random(board)
            board.push_san(bot_move)
            move_list.append(bot_move)

            W_time.append(str((time.time() - WBot_s) * 1e3) + "ms")

            if board.is_game_over() == 0:
                BBot_s = time.time()
# Black
                bot_move = Bots.bot_994625T(board)
                board.push_san(bot_move)
                move_list.append(bot_move)

                B_time.append(str((time.time() - BBot_s) * 1e3) + "ms")


        Log(board, move_list, W_time, B_time)
        print(f"{i + 1}/{num_games} || {round(((i + 1) / num_games) * 100)}%")
    print("Simulation successfully executed")






#First number represents the number of games
main(100)