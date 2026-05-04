import chess
import Bots

#--------------------------------------------------------------#

def main(num_games):

    board = chess.Board()

    print("Progress of games complete:")
    for i in range(num_games):

        board.reset()
        move_list = []

        while board.is_checkmate() + board.can_claim_threefold_repetition() + board.is_insufficient_material() + board.can_claim_fifty_moves() + board.is_stalemate() == 0:
# Bot vs Bot
          
# White
# Bot 1 - bot_random
                    bot_move = Bots.bot_random(board)
                    board.push_san(bot_move)
                    move_list.append(bot_move)

                if board.is_checkmate() + board.can_claim_threefold_repetition() + board.is_insufficient_material() + board.can_claim_fifty_moves() + board.is_stalemate() == 0:
# Black
# Bot 2 - bot_random
                    bot_move = Bots.bot_random(board)
                    board.push_san(bot_move)
                    move_list.append(bot_move)

        print(f"{i + 1}/{num_games} || {round(((i + 1) / num_games) * 100)}%")
    print("Simulation successfully executed")






#First number represents the number of games
main(1)
