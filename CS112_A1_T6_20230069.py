# filename: CS112_A1_T6_2_20230069.py
# Purpose: This program runs the tic-tac-toe with numbers game for 2 players
# Author: Andrew Wafae
# ID: 20230069
# Date: Feb 21, 2023
# Version v1.0

from math import floor


# the main() function contains the main control flow of the program
# it is called at the end of the file
def main():

    played_before = False
    scores = [0 for i in range(2)]  # a list to store player scores

    UPPER_LIMIT = 9
    TARGET = 15

    # Main Program Loop
    while True:

        # Greeting
        print()
        if not played_before:
            print("Welcome to Number Tic-Tac-Toe!")
        print(f"Would you like to play{" again" if played_before else ""}?", "A) Yes!", "B) No, Quit.", sep = "\n")

        while True:
            action = input("Select a choice (A/B): ").upper().strip()
            if not choice_is_valid(action, 2):
                print("Invalid choice, please select a valid choice" + "\n")
            else:
                break

        if action == "B":
            if played_before:
                print("\n" + "Thanks for playing!")
            print()
            break

        # Instructions if not played before + Ask users whether to display score after each round
        if not played_before:

            print("\n" + "—" * 86, "Instructions:", "Players choose a number to place in a square of the board each turn,",
                  "Player 1 may only choose odd numbers (1-9), Player 1 may only choose odd numbers (0-8)",
                  "Players may only pick a number once",
                  "First to fill a row, column, or diagonal with 3 numbers adding to 15 wins!",
                  "To pick a square, enter its corresponding number",
                  "The squares are numbered as follows:", sep = "\n", end = "\n\n")
            display_board([[1,2,3], [4,5,6], [7,8,9]])
            print("—" * 86)

            display_score = False
            print("\n" + f"Would you like to display the score after each round?", "A) Yes", "B) No", sep="\n")
            while True:
                action = input("Select a choice (A/B): ").strip()
                if not choice_is_valid(action, 2):
                    print("Invalid choice, please select a valid choice" + "\n")
                else:
                    break
            if action == "A":
                display_score = True

        # Initializes the resources of the current round
        game_won = False
        nums = [i for i in range(UPPER_LIMIT + 1)]  # a list to mark picked numbers
        entries = [[-1 for i in range(3)] for j in range(3)]  # the 2d list containing player moves

        # Game Logic
        i = 0
        while not game_won and i < 9:

            print()
            display_board(entries)

            player_no = (i % 2) + 1
            move, square = get_valid_move(player_no, nums, entries, UPPER_LIMIT)
            row_index = floor((square - 1) / 3)
            column_index = (square - 1) % 3

            # mark number as picked
            nums[move] = -1
            # add number to player's moves
            entries[row_index][column_index] = move

            if is_winner(row_index, column_index, entries, TARGET):

                # Declare Winner
                print()
                display_board(entries)

                game_won = True
                played_before = True
                print(f"Player {player_no} wins!" + "\n")

                scores[player_no - 1] += 1
                if display_score:
                    print(f"Score: {scores[0]}-{scores[1]}")

            i += 1

        played_before = True

        # Declare Draw
        if not game_won:
            print("\n" "Draw!" + "\n")
            if display_score:
                print(f"Score: {scores[0]}-{scores[1]}")


# Checks if the user chose a valid choice
def choice_is_valid(choice, n_choices):
    # if choice is one of the first n alphabetical characters, returns True (where n is n_choices)
    if len(choice) == 1:  # must be checked first, otherwise ord() crashes the program
        if 1 <= (ord(choice.upper()) - 64) <= n_choices:
            return True
    return False


def display_board(entries):

    board = ""

    for i in range(5):
        if i % 2 != 0:
            board += ("—" * 9 + "\n")
        else:
            row_idx = int(i / 2)
            for j in range(3):
                board += f"{entries[row_idx][j] if entries[row_idx][j] != -1 else "-"}" + " | "
            board = board[:-3] + "\n"

    print(board)


# gets a legal move from the user each turn
def get_valid_move(player_no, nums, entries, range_limit):

    while True:

        print("\n" + f"Available numbers: {str([i for i in nums if i != -1 and i % 2 == (1 if player_no == 1 else 0)])[1:-1]}")

        while True:

            print(f"Player {player_no}'s turn. ")

            try:
                # not int(input()) because floats are numbers, the int() cast happens later
                choice = float(input("Pick a number: "))

            except ValueError:
                print("Not a number, please try again.")

            else:

                if choice % 1 != 0:
                    print("Not an integer, please try again.")
                    continue

                choice = int(choice)

                if not 0 <= choice <= range_limit:
                    print(f"Number out of range, please pick a number from 1 to {range_limit}")
                elif nums[choice] == -1:
                    print(f"Number already picked, try another.")
                elif choice % 2 != (1 if player_no == 1 else 0):
                    print(f"Player {player_no} may only pick {"odd" if player_no == 1 else "even"} numbers, try again")
                else:
                    break

        while True:

            try:
                # not int(input()) because floats are numbers, the int() cast happens later
                square = float(input("Pick a square: "))

            except ValueError:
                print("Not a number, please try again.")

            else:

                if square % 1 != 0:
                    print("Not an integer, please try again.")
                    continue

                square = int(square)

                if not 1 <= square <= range_limit:
                    print(f"Number out of range, please pick a number from 1 to {range_limit}")
                elif entries[floor((square - 1) / 3)][(square - 1) % 3] != -1:
                    print("Square already filled, try another")
                else:
                    return [choice, square]


# check if the player has a winning combination
def is_winner(row_index, column_index, entries, target_number):

    # if a row sums to 15
    if -1 not in entries[row_index] and sum(entries[row_index]) == target_number:
        return True
    # if a column sums to 15
    elif (-1 not in [entries[i][column_index] for i in range(3)]
          and   sum([entries[i][column_index] for i in range(3)]) == target_number):
        return True
    # if the left diagonal sums to 15
    elif ((row_index == column_index)
          and -1 not in [entries[i][i] for i in range(3)]
          and       sum([entries[i][i] for i in range(3)]) == target_number):
        return True
    # if the right diagonal sums to 15
    elif ((row_index + column_index == 2)
          and -1 not in [entries[i][2-i] for i in range(3)]
          and       sum([entries[i][2-i] for i in range(3)]) == target_number):
        return True
    else:
        return False


main()
