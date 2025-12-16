"""
My attempt at writing code for a lights out game in Python.
Feel free to share feedback on how I can improve my code.
By CSClub05
"""

import random

# Set up a board
board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

count = 0  # Count how many moves a player takes
finish = False


def display_board() -> None:
    """
    Prints the board in a 5x5 grid.
    """
    print("    1 2 3 4 5\n    - - - - -")

    current_row_num_display = 1
    for j in range(5):  # Printing the rows
        display_row = str(current_row_num_display) + " | "
        for i in range(5):  # Printing the column
            display_row += str(board[5 * j + i]) + " "
        current_row_num_display += 1
        print(display_row)


def check_finish() -> bool:
    """
    Return True if all the cells in the board are equal to 0.
    """
    zeros_counter = 0
    for cell in board:
        if cell == 0:
            zeros_counter += 1
    return zeros_counter == 25


def flip(cell_index: int) -> int:
    """
    Flips the cell from 0 to 1, or 1 to 0.
    """
    if board[cell_index] == 1:
        return 0
    else:
        return 1


def flip_cell_at_index(index_to_flip: int) -> None:
    """
    Flips cell according to certain rules based on 
    the position of the index (corners, edges, normal).
    """
    board[index_to_flip] = flip(index_to_flip)

    # Corner = 0, 4, 20, 24
    if index_to_flip == 0:  # i+1, i+5
        board[1] = flip(1)
        board[5] = flip(5)

    elif index_to_flip == 4:  # i-1, i+5
        board[3] = flip(3)
        board[9] = flip(9)

    elif index_to_flip == 20:  # i-5, i+1
        board[15] = flip(15)
        board[21] = flip(21)

    elif index_to_flip == 24:  # i-5, i-1
        board[19] = flip(19)
        board[23] = flip(23)

    elif index_to_flip in [5, 9, 10, 14, 15, 19]:
        board[index_to_flip - 5] = flip(index_to_flip - 5)
        board[index_to_flip + 5] = flip(index_to_flip + 5)
        if index_to_flip % 5 == 0:  # LEFT edge = 5, 10, 15. Flip n-5, n+5, n+1
            board[index_to_flip + 1] = flip(index_to_flip + 1)
        else:  # RIGHT edge = 9, 14, 19. Flip n-5, n+5, n-1
            board[index_to_flip - 1] = flip(index_to_flip - 1)

    elif index_to_flip in [1, 2, 3, 21, 22, 23]:
        board[index_to_flip - 1] = flip(index_to_flip - 1)
        board[index_to_flip + 1] = flip(index_to_flip + 1)
        if index_to_flip > 20:
            # BOTTOM edge = 21, 22, 23. Flip n-1, n+1, n-5
            board[index_to_flip - 5] = flip(index_to_flip - 5)
        else:
            # TOP edge = 1, 2, 3. Flip n-1, n+1, n+5
            board[index_to_flip + 5] = flip(index_to_flip + 5)

    else:  # Normal = Flip n + 1, n - 1, n + 5, n - 5
        board[index_to_flip - 1] = flip(index_to_flip - 1)
        board[index_to_flip + 1] = flip(index_to_flip + 1)
        board[index_to_flip - 5] = flip(index_to_flip - 5)
        board[index_to_flip + 5] = flip(index_to_flip + 5)


def generate_board() -> None:
    """
    Generate Board. To ensure solvability, we generate a board 
    by starting from the solved state. Then, having the program 
    flip the cells like a normal player would. Essentially, the 
    player would have to "reverse" what the program flipped.
    Program will scramble up to 50 times. Note I have NOT done 
    research into how many times is considered "optimal" or adequate 
    scrambling.
    """
    for _ in range(random.randint(1, 50)):
        index_generated = random.randint(0, 24)
        flip_cell_at_index(index_generated)


consent_validity = False

file_consent = False

while not consent_validity:
    print("If you consent, this program will create a file.")
    print("The file will store your various board configurations")
    print("and the number of moves it took you to solve the board.")
    game_file_consent = input("Do you allow this program to do so [Y/N]: ")
    consent_validity = game_file_consent == "Y" or game_file_consent == "N"

if game_file_consent == "Y":
    file_consent = True

print("---------------------")
print("Welcome to Lights Out")
print("An attempt by CSClub05")
print("Choose the following options: ")
print("1. See your best score")
print("Note: You need to first have a valid attempt.")
print("Otherwise, the program crashes.")
print("2. Play the game")

option_input_validity = False
while not option_input_validity:
    option_input = int(input("Choice: "))
    option_input_validity = option_input == 1 or option_input == 2

if option_input == 1:
    if not file_consent:
        print("Sorry, this information isn't available.")
    else:
        list_of_boards = []
        list_of_moves = []
        score_file = open('csclub_lights_out.txt', 'r')
        for line in score_file:
            temp_list = line.strip("\n").split("+")
            list_of_boards.append(temp_list[0])
            list_of_moves.append(int(temp_list[1]))
        personal_best = min(list_of_moves)
        best_board_str = list_of_boards[list_of_moves.index(personal_best)]
        best_board = best_board_str.strip("[").strip("]").split(",")
        for best_cell_num in range(25):
            board[best_cell_num] = int(best_board[best_cell_num])
        print("Board where you got your PB:")
        display_board()
        print("Your personal best is: " + str(personal_best) + " moves!")
        score_file.close()

elif option_input == 2:
    if file_consent:
        score_file = open('csclub_lights_out.txt', 'a')

    generate_board()

    if file_consent:
        # + acts as a separator so we can easily use the .split() function later
        score_file.write(str(board) + "+")
        score_file.close()

    finish = check_finish()  # Edge case check if board is already solved.

    while not finish:

        display_board()
        print("Number of moves: " + str(count))

        input_validity = False  # Assume player's input is invalid

        while not input_validity:
            player_row = int(input("Row: "))
            input_validity = 1 <= player_row <= 5

        input_validity = False  # Reset the value to check the column input

        while not input_validity:
            player_col = int(input("Col: "))
            input_validity = 1 <= player_col <= 5

        index = 5 * (player_row - 1) + player_col - 1

        flip_cell_at_index(index)

        count += 1

        finish = check_finish()

    display_board()
    print("It took you " + str(count) + " moves.")

    if file_consent:
        with open('csclub_lights_out.txt', 'a') as score_file:
            score_file.write(str(count) + "\n")
