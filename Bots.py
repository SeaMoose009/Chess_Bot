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
    # Creating a temperatry board where the future moves can be tested.
    board_fen = board.fen()


    # Base pieces scoring.
    score_base = {
        # Classifying the king as None so it doesn't try to taking/capturing/using its king
        "K" : 0,
        "Q" : 9,
        "R" : 5,
        "B" : 3,
        "N" : 3,
        "P" : 1,

        "k" : 0,
        "q" : 9,
        "r" : 5,
        "b" : 3,
        "n" : 3,
        "p" : 1,

        "None" : 0
    }

    board_score_weight = {
        "a1" : 1,   "b1" : 0,   "c1" : 0,   "d1" : 0,   "e1" : 0,   "f1" : 0,   "g1" : 0,   "h1" : 0,
        "a2" : 1,   "b2" : 0,   "c2" : 0,   "d2" : 0,   "e2" : 0,   "f2" : 0,   "g2" : 0,   "h2" : 0,
        "a3" : 0,   "b3" : 0,   "c3" : 0,   "d3" : 0,   "e3" : 0,   "f3" : 0,   "g3" : 0,   "h3" : 0,
        "a4" : 0,   "b4" : 0,   "c4" : 0,   "d4" : 0,   "e4" : 0,   "f4" : 0,   "g4" : 0,   "h4" : 0,
        "a5" : 0,   "b5" : 0,   "c5" : 0,   "d5" : 0,   "e5" : 0,   "f5" : 0,   "g5" : 0,   "h5" : 0,
        "a6" : 0,   "b6" : 0,   "c6" : 0,   "d6" : 0,   "e6" : 0,   "f6" : 0,   "g6" : 0,   "h6" : 0,
        "a7" : 0,   "b7" : 0,   "c7" : 0,   "d7" : 0,   "e7" : 0,   "f7" : 0,   "g7" : 0,   "h7" : 0,
        "a8" : 0,   "b8" : 0,   "c8" : 0,   "d8" : 0,   "e8" : 0,   "f8" : 0,   "g8" : 0,   "h8" : 0
    }


    # weighting scores

    SCORE_WEIGHT_move_to_defended = 1
    SCORE_WEIGHT_capture_higher_scored = 3
    SCORE_WEIGHT_take_center = 1


    # Check whose turn it is
    if board.turn == chess.WHITE:
        colour = True
    else:
        colour = False

    # Defining the list of possible legal moves for the bots turn and the scoring
    # Moves will have the id of [Move, Score, UCI_move] (Move index = 0 and Score index = 1) <== maybe make it faster by setting to a uint_16
    Moves = []

    for m in board.legal_moves:
        Moves.append([board.san(m), 0])

    if Moves.__len__() == 1:
        return Moves[0][0]

    # Adding UCI moves
    for m in Moves:
        m.append(san_to_uci(m[0], board))

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
        move = m[2]
        temp = chess.Board(board_fen)
        temp.push_san(m[0])
        atk = temp.attackers(not colour, chess.parse_square(uci_to(move))).__len__()
        dfd = temp.attackers(colour, chess.parse_square(uci_to(move))).__len__()

        m[1] += (dfd-atk) * SCORE_WEIGHT_move_to_defended

    # -----------------------------------------------------------
    # Taking pieces with higher or equal score
    # ---------

    for m in Moves:
        from_piece = board.piece_at(chess.parse_square(uci_from(m[2])))
        to_piece = board.piece_at(chess.parse_square(uci_to(m[2])))

        from_score = score_base[str(from_piece)]
        to_score = score_base[str(to_piece)]

        if from_score + to_score != 0:
            if from_score >= to_score:
                m[1] += from_score - to_score * SCORE_WEIGHT_capture_higher_scored

    # -----------------------------------------------------------
    # Taking the center of the board
    # ---------



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