import chess
import Bots

# --------------------------------------------------------------#

def main(num_games, vs_state):

    board = chess.Board()

    print("Progress of games complete:")
    for i in range(num_games):

        board.reset()
        move_list = []

        while board.is_checkmate() + board.can_claim_threefold_repetition() + board.is_insufficient_material() + board.can_claim_fifty_moves() + board.is_stalemate() == 0:
                       #Player vs Bot
            if vs_state == 1:
                # 1
                # White
                print(f"{board}\n\n")

                can_move = True
                Legal_List = []

                for m in board.legal_moves:
                    Legal_List.append(board.san(m))

                print("Legal move list |>|", *Legal_List)

                while can_move == True:
                    move = input("Make your move |>|")

                    try:
                        can_move = False
                        board.push_san(move)
                        move_list.append(move)
                    except chess.InvalidMoveError or chess.IllegalMoveError:
                        can_move = True
                        print("Invalid move type")

                if board.is_checkmate() + board.can_claim_threefold_repetition() + board.is_insufficient_material() + board.can_claim_fifty_moves() + board.is_stalemate() == 0:
                    # Black
                    bot_move = Bots.bot_random(board)
                    board.push_san(bot_move)
                    move_list.append(bot_move)

        print(f"{i + 1}/{num_games} || {round(((i + 1) / num_games) * 100)}%")
    print("Simulation successfully executed")
    print(f"{board}\n\n")
    print(f"{move_list}\n\n")






#First number represents the number of games
#The second number being the type of gameplay. valid numbers being 0,1,2.
main(1,0)
