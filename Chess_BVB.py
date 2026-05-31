import chess
import Bots
from Logging import calculate_win
#--------------------------------------------------------------#

def main(num_games):

    board = chess.Board()

    print("Progress of games complete:")
    for i in range(num_games):

        board.reset()
        move_list = []

        while board.is_game_over() == 0:
# Bot vs Bot
          
# White
# Bot 1 - bot_random
            bot_move = Bots.bot_random(board)
            board.push_san(bot_move)
            move_list.append(bot_move)

            if board.is_game_over() == 0:
# Black
# Bot 2 - bot_994625T
                bot_move = Bots.bot_994625T(board)
                board.push_san(bot_move)
                move_list.append(bot_move)

        calculate_win(board, move_list)
        print(f"{i + 1}/{num_games} || {round(((i + 1) / num_games) * 100)}%")
    print("Simulation successfully executed")






#First number represents the number of games
main(1)