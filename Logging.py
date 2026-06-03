def clear_board_logs():
    with open("Logs.txt", "w") as f:
        f.write("")

def clear_log():
    with open("Board Logs.txt", "w") as f:
        f.write("")

def clear_performace():
    with open("Performance.txt", "w") as f:
        f.write("")


def Log(board,move_list, WBot_time, BBot_time):
    Board = f"{board}\n{move_list}\n\n"
    with open("Board Logs.txt", "a") as B:
        B.write(Board)

    Logs = f"Checkmate: {board.outcome()}\n"
    with open("Logs.txt", "a") as L:
        L.write(Logs)

    Performace = f"White: {WBot_time}\nBlack: {BBot_time}\n\n"
    with open("Performance.txt", "a") as P:
        P.write(Performace)

clear_log()
clear_board_logs()
clear_performace()