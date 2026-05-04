import random

#Exemplar bot that recives the board state, picks a random move from the legal list, and returns that move to be made within the Handler
def bot_random(board):
    Legal_List = []

    for m in board.legal_moves:
        Legal_List.append(board.san(m))

    if Legal_List.__len__()-1 == 0:
        move = Legal_List[0]
    else:
        move = Legal_List[random.randint(0,Legal_List.__len__()-1)]
    return move
