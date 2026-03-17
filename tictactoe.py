# from tkinter import *
# import random


# def next_turn(row, column):

#     global player

#     if buttons[row][column]['text'] == "" and chech_winner() is False:

#         buttons[row][column]['text'] = player

#         result = chech_winner()

#         if result is False:
#             player = players[1] if player == players[0] else players[0]
#             label.config(text=player + " Turn")

#         elif result is True:
#             label.config(text=player + " Wins")

#         elif result == "Tie":
#             label.config(text="Tie!!!")


# def chech_winner():

#     # check rows
#     for row in range(3):
#         if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
#             buttons[row][0].config(bg="#90ee90")
#             buttons[row][1].config(bg="#90ee90")
#             buttons[row][2].config(bg="#90ee90")
#             return True

#     # check columns
#     for column in range(3):
#         if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
#             buttons[0][column].config(bg="#90ee90")
#             buttons[1][column].config(bg="#90ee90")
#             buttons[2][column].config(bg="#90ee90")
#             return True

#     # check diagonals
#     if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
#             buttons[0][0].config(bg="#90ee90")
#             buttons[1][1].config(bg="#90ee90")
#             buttons[2][2].config(bg="#90ee90")
#             return True

#     if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
#             buttons[0][2].config(bg="#90ee90")
#             buttons[1][1].config(bg="#90ee90")
#             buttons[2][0].config(bg="#90ee90")
#             return True

#     # check tie
#     if empty_spaces() is False:
#         for row in range(3):
#             for column in range(3):
#                 buttons[row][column].config(bg="yellow")
#         return "Tie"

#     return False


# def empty_spaces():
#     for row in range(3):
#         for column in range(3):
#             if buttons[row][column]['text'] == "":
#                 return True
#     return False


# def new_game():
#     global player

#     player = random.choice(players)
#     label.config(text=player + " Turn")

#     for row in range(3):
#         for column in range(3):
#             buttons[row][column].config(text="",bg="#F0F0F0")


# # ---------------- MAIN PROGRAM ----------------

# window = Tk()
# window.title("Tic-Tac-Toe")
# # window.config(bg="#63e5ff")
# window.config(bg="#1e3d59")



# players = ["X", "O"]
# player = random.choice(players)

# buttons = [[0, 0, 0],
#            [0, 0, 0],
#            [0, 0, 0]]




# label = Label(
#     text=player + " Turn",
#     font=('consolas', 36, 'bold'),
#     bg="#1e3d59",
#     fg="white"
# )
# label.pack(side="top", pady=25)



# frame = Frame(window, bd=5, relief="solid")
# frame.pack(pady=20)


# for row in range(3):
#     for column in range(3):
#         buttons[row][column] = Button(frame,
#                                       text="",
#                                       font=('consolas', 40),
#                                       width=5,
#                                       height=2,
#                                       command=lambda row=row, column=column: next_turn(row, column))

#         buttons[row][column].grid(row=row, column=column)


# reset_button = Button(text="Restart", font=('consolas', 20), command=new_game)
# reset_button.config(bg="#de0a26")
# reset_button.pack(side="top", pady=20)

# window.mainloop()

from tkinter import *
import random

# ---------------- GLOBAL VARIABLES ----------------

current_player = "X"
game_mode = "player"
difficulty = "Hard"

score_x = 0
score_o = 0

buttons = []

# ---------------- GAME FUNCTIONS ----------------

def player_move(row, col):

    global current_player

    if buttons[row][col]["text"] != "" or check_winner():
        return

    buttons[row][col]["text"] = current_player

    if current_player == "X":
        buttons[row][col].config(fg="#0b84ff")
    else:
        buttons[row][col].config(fg="#ff2e63")

    result = check_winner()

    if result:
        end_game(current_player)
        return

    if board_full():
        draw_board()
        return

    switch_player()

    if game_mode == "computer" and current_player == "O":
        status_label.config(text="Computer thinking...")
        window.after(800, computer_move)


def switch_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"
    status_label.config(text=current_player + " Turn")


# ---------------- COMPUTER AI ----------------

def computer_move():

    if difficulty == "Easy":
        move = random_move()

    elif difficulty == "Medium":
        if random.random() < 0.5:
            move = random_move()
        else:
            move = best_move()

    else:
        move = best_move()

    if move:
        r, c = move
        buttons[r][c]["text"] = "O"
        buttons[r][c].config(fg="#ff2e63")

    result = check_winner()

    if result:
        end_game("O")
        return

    if board_full():
        draw_board()
        return

    switch_player()


def random_move():

    empty = []

    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == "":
                empty.append((r, c))

    return random.choice(empty) if empty else None


def best_move():

    best_score = -1000
    move = None

    for r in range(3):
        for c in range(3):

            if buttons[r][c]["text"] == "":
                buttons[r][c]["text"] = "O"
                score = minimax(False)
                buttons[r][c]["text"] = ""

                if score > best_score:
                    best_score = score
                    move = (r, c)

    return move


def minimax(is_max):

    winner = evaluate_board()

    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if board_full():
        return 0

    if is_max:
        best = -1000

        for r in range(3):
            for c in range(3):
                if buttons[r][c]["text"] == "":
                    buttons[r][c]["text"] = "O"
                    score = minimax(False)
                    buttons[r][c]["text"] = ""
                    best = max(score, best)

        return best

    else:
        best = 1000

        for r in range(3):
            for c in range(3):
                if buttons[r][c]["text"] == "":
                    buttons[r][c]["text"] = "X"
                    score = minimax(True)
                    buttons[r][c]["text"] = ""
                    best = min(score, best)

        return best


# ---------------- WIN CHECK ----------------

def evaluate_board():

    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] != "":
            return buttons[r][0]["text"]

    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] != "":
            return buttons[0][c]["text"]

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    return None


def check_winner():

    winner = evaluate_board()

    if winner:
        highlight_winner(winner)
        return True

    return False


def highlight_winner(winner):

    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] == winner:
            for c in range(3):
                buttons[r][c].config(bg="#90ee90")

    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] == winner:
            for r in range(3):
                buttons[r][c].config(bg="#90ee90")

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == winner:
        buttons[0][0].config(bg="#90ee90")
        buttons[1][1].config(bg="#90ee90")
        buttons[2][2].config(bg="#90ee90")

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == winner:
        buttons[0][2].config(bg="#90ee90")
        buttons[1][1].config(bg="#90ee90")
        buttons[2][0].config(bg="#90ee90")


def board_full():

    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == "":
                return False
    return True


def draw_board():

    status_label.config(text="Draw Game!")

    for r in range(3):
        for c in range(3):
            buttons[r][c].config(bg="yellow")


# ---------------- GAME CONTROL ----------------

def end_game(winner):

    global score_x, score_o

    if winner == "X":
        score_x += 1
        status_label.config(text="Player X Wins!")

    else:
        score_o += 1

        if game_mode == "computer":
            status_label.config(text="Computer Wins!")
        else:
            status_label.config(text="Player O Wins!")

    update_score()


def update_score():

    score_label.config(text=f"Score  X:{score_x}   O:{score_o}")


def reset_board():

    global current_player

    current_player = "X"
    status_label.config(text="X Turn")

    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="#f5f5f5", fg="black")


def reset_score():

    global score_x, score_o

    score_x = 0
    score_o = 0

    update_score()
    reset_board()


def set_mode(mode):

    global game_mode
    game_mode = mode
    reset_board()


def set_difficulty(level):

    global difficulty
    difficulty = level


# ---------------- GUI ----------------

window = Tk()
window.title("Professional Tic Tac Toe")
window.geometry("420x540")
window.config(bg="#1e3d59")

title = Label(window,
text="TIC TAC TOE",
font=("Arial",26,"bold"),
bg="#1e3d59",
fg="white")

title.pack(pady=10)

status_label = Label(window,
text="X Turn",
font=("Arial",18),
bg="#1e3d59",
fg="white")

status_label.pack()

score_label = Label(window,
text="Score  X:0   O:0",
font=("Arial",16),
bg="#1e3d59",
fg="white")

score_label.pack(pady=5)

control_frame = Frame(window,bg="#1e3d59")
control_frame.pack()

Button(control_frame,text="2 Players",
command=lambda:set_mode("player")).grid(row=0,column=0,padx=5)

Button(control_frame,text="Vs Computer",
command=lambda:set_mode("computer")).grid(row=0,column=1,padx=5)

diff_frame = Frame(window,bg="#1e3d59")
diff_frame.pack(pady=5)

Button(diff_frame,text="Easy",
command=lambda:set_difficulty("Easy")).grid(row=0,column=0,padx=3)

Button(diff_frame,text="Medium",
command=lambda:set_difficulty("Medium")).grid(row=0,column=1,padx=3)

Button(diff_frame,text="Hard",
command=lambda:set_difficulty("Hard")).grid(row=0,column=2,padx=3)

board = Frame(window)
board.pack(pady=15)

for r in range(3):

    row = []

    for c in range(3):

        btn = Button(board,
        text="",
        font=("Arial",40,"bold"),
        width=4,
        height=2,
        bg="#f5f5f5",
        activebackground="#dcdcdc",
        bd=3,
        relief="ridge",
        command=lambda r=r,c=c:player_move(r,c))

        btn.grid(row=r,column=c)

        row.append(btn)

    buttons.append(row)

bottom_frame = Frame(window,bg="#1e3d59")
bottom_frame.pack(pady=10)

Button(bottom_frame,
text="Restart",
command=reset_board).grid(row=0,column=0,padx=5)

Button(bottom_frame,
text="Reset Score",
command=reset_score).grid(row=0,column=1,padx=5)

window.mainloop()