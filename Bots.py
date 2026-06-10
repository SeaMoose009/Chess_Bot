import random
from operator import invert

import chess
from chess import BaseBoard, square_name


# Exemplar bot that receives the board state, picks a random move from the legal list, and returns that move to be made within the Handler
def bot_random(board):
    Legal_List = []

    for m in board.legal_moves:
        Legal_List.append(board.san(m))

    if Legal_List.__len__() == 1:
        move = Legal_List[0]
    else:
        move = Legal_List[random.randint(0,Legal_List.__len__() - 1)]
    return move

    

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# SACE ID number labeling the creator of the bot
def bot_994625T(board, temperature=0):

    # Base pieces scoring.
    score_base = {
        "Q": 9,
        "R": 5,
        "B": 3,
        "N": 3,
        "P": 1,

        "q" : 9,
        "r" : 5,
        "b" : 3,
        "n" : 3,
        "p" : 1
    }

    # Check whose turn it is
    if board.turn == chess.WHITE:
        colour = True
    else:
        colour = False

    # Creating a temperatry board where the future moves can be tested.
    board_fen = board.fen()
    # Defining the list of possible legal moves for the bots turn and the scoring
    # Moves will have the id of [Move, Score] (Move index = 0 and Score index = 1) <== maybe make it faster by setting to a uint_16
    Moves = []

    for m in board.legal_moves:
        Moves.append([board.san(m), 0])

    if Moves.__len__() == 1:
        return Moves[0][0]

    # -----------------------------------------------------------
    # Adding checkmate in one
    # ---------

    for i in Moves:
        if i[0][-1] == '#':
            return i[0]  # Immediately returning the move that checkmates to reduce runtime

    # -----------------------------------------------------------
    # Avoiding checkmate in one
    # ---------

    for i in Moves:
        temp_board = chess.Board(board_fen)
        temp_board.push_san(i[0])
        for m in temp_board.legal_moves:
            if temp_board.san(m)[-1] == '#':
                i[1] -= 10000  # Guarantees that it avoids checkmate on itself

    # -----------------------------------------------------------
    # Adding score for moving to defended squares
    # ---------

    for m in Moves:
        move = san_to_uci(m[0], board)
        temp = chess.Board(board_fen)
        temp.push_san(m[0])
        atk = temp.attackers(not colour, chess.parse_square(uci_to(move))).__len__()
        dfd = temp.attackers(colour, chess.parse_square(uci_to(move))).__len__()

        m[1] += dfd-atk

    # -----------------------------------------------------------
    # Picking the best available move within a given temperature
    # ---------
    final_move_list = []
    best_score = Moves[0][1]

    # First pass
    for i in Moves:
        if i[1] > best_score:
            best_score = i[1]
    # Second pass
    for i in Moves:
        if i[1] >= best_score - temperature:
            final_move_list.append(i[0])

    if final_move_list.__len__() > 1:
        move = final_move_list[random.randint(0,final_move_list.__len__() - 1)]
    else:
        move = final_move_list[0]
    # Returning a random move from the best options
    return move

#------------------------------------------------------
#Function to convert san type moves to uci
#-----------
def san_to_uci(san_move, board):

    try:
        move = board.parse_san(san_move)
        return move.uci()
    except ValueError as e:
        return f"Invalid SAN move: {e}"


#------------------------------------------------------
#Function to get the first and last square
#-----------

def uci_from(uci):
    return uci[0]+uci[1]


def uci_to(uci):
    return uci[2] + uci[3]


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\




def bot_saceID(board):
    pass