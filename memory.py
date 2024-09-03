import tkinter as tk
import random
import time

# Rows and columns of the field
N_ROWS = 4
N_COLS = 4

# colors
blue = "#4584b6"
gray = "#343434"
light_gray = "#646464"
green = "#5ce65c"
red = "#c91b00"
violet = "#CF9FFF"
orange = "#FFA500"
yellow = "#ffde57"
white = "#FFFFFF"
black = "#000000"

# symbols and colors
symbols = ["x", "o", "△", "□", "♦", "♠", "♣", "♥"]
symbols_colors = [blue, orange, green, violet, yellow, white, black, red]

# field
field = [["","", "", ""],
         ["","", "", ""],
         ["","", "", ""],
         ["","", "", ""]]

# indices of the fields
field_indices = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

# check for the boxes are already paired
field_check = [[False, False, False, False],
               [False, False, False, False],
               [False, False, False, False],
               [False, False, False, False]]

prec_move, pos_x, pos_y = -1, -1, -1
moves = 0
win = False
start_time = None
label = None


def close_window(event):
    """ Closes the window when the player presses escape (Esc) """
    window.destroy()


def create_window() -> tk.Tk:
    global label, moves

    """ Creates the window """
    window = tk.Tk()
    window.title("Memory")
    window.resizable(False, False)

    # event on window
    window.bind('<Escape>', close_window)

    # wait to dispay window
    window.withdraw()

    frame = tk.Frame(window)

    # label that dispays the moves 
    label = tk.Label(frame, text="Moves: " + str(moves), font=("Times new roman", 20), background=gray, foreground=white)
    label.grid(row=0, column=0, columnspan=N_COLS, sticky="we") #west to east / left to right

    # field setup
    for row in range(N_ROWS):
        for column in range(N_COLS):
            field[row][column] = tk.Button(frame, text=field[row][column], font=("Times new roman", 50, "bold"), background=gray, foreground=blue, width=4, height=1, command=lambda row=row, column=column: set_box(row, column))
            field[row][column].grid(row=row+1, column=column)

    # reset button
    button = tk.Button(frame, text="Reset", font=("Times new roman", 20), background=gray, foreground=white, command=lambda row=row, column=column: new_game())
    button.grid(row=N_ROWS+1, column=0, columnspan=N_COLS, sticky="we")

    frame.pack()

    # center the window in the center of the scrreen
    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    window.deiconify()

    return window


def init_grid():
    """ Initializes the field randomly """
    global field, symbols, field_indices, symbols_colors, start_time
    
    idx = list(range(len(symbols))) * 2

    random.shuffle(idx)

    count = 0
    for i in range(N_ROWS):
        for j in range(N_COLS):
            field_indices[i][j] = idx[count]
            count += 1
   
    start_time = time.time()


def set_box(row, column):
    """ Shows the selected symbols, check if there is a win and manage the moves. 
    In memory each move involves two actions because two boxes must be chosen at a time,
    so if it's the first action the unpaired boxes are deleted and the current symbol found is saved, 
    otherwise it checks whether a pair has been found """

    global field, field_check, field_indices, symbols, prec_move, moves, pos_x, pos_y, start_time

    # do nothing if the player as already completed the memory
    if(win):
        return
    
    # do nothing if the player has selected an already open box
    if field[row][column]["text"] != "":
        return

    # first action
    if(prec_move == -1):
        # removes the unpaired boxes
        for r in range(N_ROWS):
            for c in range(N_COLS):
                if not(field_check[r][c]):
                    field[r][c].config(text="", foreground=gray)      

        # saves the current symbol  
        prec_move = field_indices[row][column]
        pos_x = row
        pos_y = column
   
    else:
        # check if there is a pair
        if (prec_move == field_indices[row][column]):
            field[row][column].config(background=light_gray)   
            field[pos_x][pos_y].config(background=light_gray)   
            field_check[row][column] = True
            field_check[pos_x][pos_y] = True
        
        # reset variables
        prec_move, pos_x, pos_y = -1, -1, -1
        moves += 1

        # Update the moves
        label.config(text="Moves: " + str(moves))

    # show the selected symbol
    index = field_indices[row][column]
    field[row][column].config(text=symbols[index], foreground=symbols_colors[index])

    # check if the memory is completed
    check_win()

    if(win):
        label.config(text=f"Win in {moves} moves and {int(time.time() - start_time)} seconds")


def check_win() -> None:
    """ Checks if all symbol pairs have been found.
    If all field_check members are True the player has won, otherwise not """

    global win

    for row in range(N_ROWS):
        for column in range(N_COLS):
            if not(field_check[row][column]):
                return
            
    win = True


def new_game():
    """ Reset all variables to start a new game and initializes the field randomly """
    global prec_move, win, field_indices, field, field_check, pos_x, pos_y, moves, label, start_time

    prec_move, pos_x, pos_y = -1, -1, -1
    moves = 0
    start_time = None
    win = False

    label.config(text="Moves: " + str(moves), foreground=white)

    for row in range(N_ROWS):
        for column in range(N_COLS):
            field[row][column].config(text="", background=gray)
            field_indices[row][column] = 0
            field_check[row][column] = False
    
    init_grid()
    

if __name__ == '__main__':
    init_grid()
    window = create_window()
    window.mainloop()