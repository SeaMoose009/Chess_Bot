def clear_board_logs():
    with open("Logs.txt", "w") as f:
        f.write("")

def clear_log():
    with open("Board Logs.txt", "w") as f:
        f.write("")

def calculate_win(board,move_list):
    outcome = board.outcome()
    Board = f"{board}\n{move_list}\n\n"
    with open("Logs.txt", "a") as B:
        B.write(Board)

        Logs = f"Checkmate: {outcome}\n"
        with open("Board Logs.txt", "a") as L:
            L.write(Logs)