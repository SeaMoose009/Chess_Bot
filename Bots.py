import math
import random
import chess


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
def bot_994625T(board, temperature=0, move_counter=0):
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
        "a1" : 0.25,   "b1" : 0.25,   "c1" : 0.5,   "d1" : 0.5,   "e1" : 0.5,   "f1" : 0.5,   "g1" : 0.25,   "h1" : 0.25,
        "a2" : 0.25,   "b2" : 1,   "c2" : 1,   "d2" : 1,   "e2" : 1,   "f2" : 1,   "g2" : 1,   "h2" : 0.25,
        "a3" : 0.25,   "b3" : 1,   "c3" : 1,   "d3" : 1,   "e3" : 1,   "f3" : 1,   "g3" : 1,   "h3" : 0.25,
        "a4" : 0.5,   "b4" : 1,   "c4" : 1,   "d4" : 2,   "e4" : 2,   "f4" : 1,   "g4" : 1,   "h4" : 0.5,
        "a5" : 0.5,   "b5" : 1,   "c5" : 1,   "d5" : 2,   "e5" : 2,   "f5" : 1,   "g5" : 1,   "h5" : 0.5,
        "a6" : 0.25,   "b6" : 1,   "c6" : 1,   "d6" : 1,   "e6" : 1,   "f6" : 1,   "g6" : 1,   "h6" : 0.25,
        "a7" : 0.25,   "b7" : 1,   "c7" : 1,   "d7" : 1,   "e7" : 1,   "f7" : 1,   "g7" : 1,   "h7" : 0.25,
        "a8" : 0.25,   "b8" : 0.25,   "c8" : 0.5,   "d8" : 0.5,   "e8" : 0.5,   "f8" : 0.5,   "g8" : 0.25,   "h8" : 0.25
    }


    # weighting scores

    SCORE_WEIGHT_move_to_defended = 1
    SCORE_WEIGHT_move_to_safety = 1
    SCORE_WEIGHT_capture_higher_scored = 5
    SCORE_WEIGHT_free_piece = 5
    SCORE_WEIGHT_checking = 3
    SCORE_WEIGHT_avoid_check = 1


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
    # Checks for moves from and to
    # ---------

    for m in Moves:
        move = m[2]
        temp = chess.Board(board_fen)
        temp.push_san(m[0])

        atk = temp.attackers(not colour, chess.parse_square(uci_to(move))).__len__()
        dfd = temp.attackers(colour, chess.parse_square(uci_to(move))).__len__()

        atk_from = temp.attackers(not colour, chess.parse_square(uci_from(move))).__len__()
        dfd_from = temp.attackers(colour, chess.parse_square(uci_from(move))).__len__()

        from_piece = board.piece_at(chess.parse_square(uci_from(m[2])))
        to_piece = board.piece_at(chess.parse_square(uci_to(m[2])))

        from_score = score_base[str(from_piece)]
        to_score = score_base[str(to_piece)]


        # Defending pieces
        m[1] += (dfd-atk) * SCORE_WEIGHT_move_to_defended

        # Avoiding attack
        m[1] += (dfd_from - atk_from + math.sqrt(from_score)) * SCORE_WEIGHT_move_to_safety

        # Taking free material
        if to_piece != None and atk == 0:
            m[1] += to_score * SCORE_WEIGHT_free_piece

        # Taking pieces with higher or equal score
        if to_score != 0:
            if from_score <= to_score:
                m[1] += (from_score - to_score) * SCORE_WEIGHT_capture_higher_scored


    # -----------------------------------------------------------
    # Checking
    # ---------

    for i in Moves:
        if i[0][-1] == '+':
            i[1]  += SCORE_WEIGHT_checking

    # -----------------------------------------------------------
    # Avoiding check
    # ---------

    for i in Moves:
        temp_board = chess.Board(board_fen)
        temp_board.push_san(i[0])
        for m in temp_board.legal_moves:
            if temp_board.san(m)[-1] == '+':
                i[1] -= SCORE_WEIGHT_avoid_check


    # -----------------------------------------------------------
    # Taking center
    # ---------
    for m in Moves:
        if m[1] >= 0:
            m[1] += board_score_weight[uci_to(m[2])] * 27**(-move_counter)

    for m in Moves:
        m[1] -= score_base[str(board.piece_at(chess.parse_square(uci_from(m[2]))))]
        if str(board.piece_at(chess.parse_square(uci_from(m[2])))).lower() == "k":
            m[1] -= 10


    # -----------------------------------------------------------
    # Connecting pawn structures
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