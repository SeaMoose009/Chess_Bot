import chess
import Bots

#--------------------------------------------------------------#

def main():

    board = chess.Board()

    board.reset()
    move_list = []

        while board.is_checkmate() + board.can_claim_threefold_repetition() + board.is_insufficient_material() + board.can_claim_fifty_moves() + board.is_stalemate() == 0:
# White
# Displaying the current board state for the player to veiw
            print(f"{board}\n\n")


# Defining the valid move list that the player can make during their turn
            Legal_List = []

            for m in board.legal_moves:
                Legal_List.append(board.san(m))

            print("Legal move list |>|", *Legal_List)

            
# Player input handling. Request input from user untill a valid response is made
            can_move = True
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
# Requesting a move from the bot and making it
                bot_move = Bots.bot_random(board)
                board.push_san(bot_move)
                move_list.append(bot_move)
                
# Prints the final board state and the moves of all pieces up untill that point once the game ends
    print(f"{board}\n\n")
    print(f"{move_list}\n\n")


main()
