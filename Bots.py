import random

# Exemplar bot that recives the board state, picks a random move from the legal list, and returns that move to be made within the Handler
def bot_random(board):
    Legal_List = []

    for m in board.legal_moves:
        Legal_List.append(board.san(m))

    if Legal_List.__len__()-1 == 0:
        move = Legal_List[0]
    else:
        move = Legal_List[random.randint(0,Legal_List.__len__()-1)]
    return move

    

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# SACE ID number labeling the creator of the bot
def bot_994625T(board, temperature=0): 
# Creating a temperatry board where the future moves can be tested.
    temp_board = chess.Board()
    board_fen = board.fen()
# Defining the list of possible legal moves for the bots turn and the scoring
# Moves will have the id of [Move, Score] (Move index = 0 and Score index = 1) <== maybe make it faster by setting to a uint_16
    Moves = []
    
    for m in board.legal_moves:
        Moves.append([board.san(m),0])

    if Moves.__len__() == 1:
        return Moves[0][0]
        
# -----------------------------------------------------------
# Adding checkmate in one
# ---------
    
    for i in Moves:
        if i[0] == if i[0][-1] == '#':
            return i[0] # Immediately returning the move that checkmates to reduce runtime
        
# -----------------------------------------------------------
# Advoiding checkmate in one
# ---------
        
    for i in Moves:
        temp_board = chess.Board(board_fen)
        temp_board.push(i[0])
        for m in temp_board.legal_moves:
            if m[-1] == '#':
            i[1] -= 10000 # Garentees that it avoids checkmate on itself


# -----------------------------------------------------------
# Picking the best avaliable move within a given temperature
# ---------
    
    final_move_list = []
    best_score = 0

    
# First pass
    for i in Moves:
        if i[1] < best_score:
            best_score = i[1]
# Second pass
    for i in Moves:
        if i[1] <= best_score - temperature:
            final_move_list.append(i[0])
                
# Returning a random move from the best options
    return final_move_list[random.randint(0,final_move_list.__len__()-1)]
