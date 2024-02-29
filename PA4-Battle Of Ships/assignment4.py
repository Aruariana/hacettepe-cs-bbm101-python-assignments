import sys
import os

# b2210356060
# Ömer Kayra Çetin


def read_txt(path):
    """Takes player txt file path as input and returns a list where each item is a line."""
    with open(path) as f:
        return f.read().split("\n")


def read_in(path):
    """Takes player in file path as input and returns a list where each item is a shot coordinat."""
    with open(path) as f:
        return f.read().split(";")[:-1]  # Last item is empty so I don't include it


def make_empty_board():
    """Returns a two-dimensional 10x10 list where each item is '-'."""
    return [["-" for _ in range(10)] for _ in range(10)]


def make_ship_board(ship_pos_list):
    """Takes player txt file list as input and returns a list where each ship is placed."""
    b_ship = make_empty_board()
    for i in range(len(ship_pos_list)):
        line = ship_pos_list[i]
        j = 0  # j is a counter for ; char to correctly place ships
        for char in line:
            if char == ";":
                j += 1
            else:
                b_ship[i][j] = char
    return b_ship


def make_ship_counter():
    """Returns a dictionary where keys are ship types, and their values are '-' times ship numbers."""
    # This dictionary will be used to correctly show which ships are sunk.
    ship_counter = dict()
    ship_counter["C"] = "-"
    ship_counter["D"] = "-"
    ship_counter["S"] = "-"
    ship_counter["B"] = "- -"
    ship_counter["P"] = "- - - -"
    return ship_counter


def make_ship_flags():
    """Returns a dictionary where each key is a ship name and their values are all 'floating'."""
    # This will be used to check if a ship is floating or sunk.
    ship_names = ["C", "D", "S", "B1", "B2", "P1", "P2", "P3", "P4"]
    return {name: "floating" for name in ship_names}


def find_ship_pos(board, opt_path):
    """Takes board and optional player txt file path as inputs and returns a dict where each key is a ship
    and their values are lists containing the ship's coordinates as tuples."""
    # Make a ship_pos dictionary, it's keys are ship names and values are its positions on the board
    ship_pos = dict()
    # Generate position lists for single ships
    c_pos, d_pos, s_pos = list(), list(), list()
    # Search single ship positions to add their values to its lists
    for i in range(10):
        for j in range(10):
            if board[i][j] == "C":
                c_pos.append((i, j))
            elif board[i][j] == "D":
                d_pos.append((i, j))
            elif board[i][j] == "S":
                s_pos.append((i, j))
    # Assign the single ships to their positions inside the dictionary
    ship_pos["C"], ship_pos["D"],  ship_pos["S"] = c_pos, d_pos, s_pos
    # Use the optinional txt files to correctly place ship categories that have more than one ship
    with open(opt_path) as f:
        lines = f.read().split("\n")  # Seperate lines
        for line in lines:
            name, content = line.split(":")
            pos, direction = content.split(";")[:-1]  # Don't include last item as it is empty
            # Get the x coordinate - 1 to correctly use in board lists which start from 0 as indexes
            x_cor = int(pos.split(",")[0]) - 1
            # Get the y coordinate as an integer to correctly use in board lists which start from 0 as indexes
            # Ord function gets the decimal ascii value of a given char
            # Since it is an upper char subtracting 65 would give the correct y coordinate
            y_cor = ord(pos.split(",")[1]) - 65
            if name[0] == "B":  # Check if it's a battleship or patrol boat
                # Check the direction to correctly get the coordinates
                if direction == "right":
                    ship_pos[name] = [(x_cor, y_cor), (x_cor, y_cor+1), (x_cor, y_cor+2), (x_cor, y_cor+3)]
                else:
                    ship_pos[name] = [(x_cor, y_cor), (x_cor+1, y_cor), (x_cor+2, y_cor), (x_cor+3, y_cor)]
            else:
                if direction == "right":
                    ship_pos[name] = [(x_cor, y_cor), (x_cor, y_cor+1)]
                else:
                    ship_pos[name] = [(x_cor, y_cor), (x_cor+1, y_cor)]
    return ship_pos


def show_ship_counter(s1_counter, s2_counter):
    """Takes p1's and p2's ship counter dictionaries as inputs and returns a txt string consisting of
    their ship counter infos."""
    txt = ""
    txt += f"Carrier\t\t{s1_counter['C']}\t\t\t\tCarrier\t\t{s2_counter['C']}\n"
    txt += f"Battleship\t{s1_counter['B']}\t\t\t\tBattleship\t{s2_counter['B']}\n"
    txt += f"Destroyer\t{s1_counter['D']}\t\t\t\tDestroyer\t{s2_counter['D']}\n"
    txt += f"Submarine\t{s1_counter['S']}\t\t\t\tSubmarine\t{s2_counter['S']}\n"
    txt += f"Patrol Boat\t{s1_counter['P']}\t\t\tPatrol Boat\t{s2_counter['P']}\n\n"
    return txt


def show_boards(b1, b2):
    """Takes p1's and p2's boards as inputs and returns a txt string consisting of their board infos."""
    txt = "Player1’s Hidden Board\t\tPlayer2’s Hidden Board\n"
    txt += "  A B C D E F G H I J\t\t  A B C D E F G H I J\n"
    for i in range(10):
        txt += "%-2d" % (i+1)
        for j in range(10):
            if j != 9:
                txt += "%-2s" % b1[i][j]
            else:
                txt += "%s" % b1[i][j]
        txt += "\t\t"
        txt += "%-2d" % (i+1)
        for j in range(10):
            if j != 9:
                txt += "%-2s" % b2[i][j]
            else:
                txt += "%s" % b2[i][j]
        txt += "\n"
    txt += "\n"
    return txt


def check_update_sunk(board, ship_count, ship_pos, ship_flag):
    """Takes a player's board, ship counter, ship positions and ship flags as input and
    checks for sunk ships and updates them. Returns none."""
    # Keys in ship_pos dictionary is each ship individually
    for key in ship_pos:
        all_shot = True
        for pos in ship_pos[key]:
            x_cor, y_cor = pos
            if board[x_cor][y_cor] != "X":
                all_shot = False
                break
        if all_shot and ship_flag[key] == "floating":
            ship_flag[key] = "sunk"
            # For updating ship count I use the first character of the key to correctly match the key for ship count
            ship_count[key[0]] = ship_count[key[0]].replace("-", "X", 1)


def check_loss(flags):
    """Takes a player's ship flags and returns True if they are all sunk, otherwise False."""
    for value in flags.values():
        if value == "floating":
            return False
    return True


def make_final_board(board, hidden_board):
    """Takes a player's actual board and hidden board as inputs and returns a board where each unshot ship
    is shown."""
    for i in range(10):
        for j in range(10):
            if board[i][j] != "-" and hidden_board[i][j] == "-":
                hidden_board[i][j] = board[i][j]
    return hidden_board


def try_paths(path_list):
    """Takes a list of paths as input and tries to open them. Returns none.
    Raises IOError if it can't open at least a file with a message that has unopenable file name(s)."""
    error_names_list = []
    for path in path_list:
        try:
            with open(path) as f:
                pass
        except IOError as err:
            error_names_list.append(os.path.basename(err.filename))
    if len(error_names_list) != 0:
        msg = ", ".join(error_names_list)
        raise IOError(msg)


def shot_ship(all_shots, shot_index, actual_board, hidden_board):
    """Takes a player's all shots, shot index and opponent's actual board, hidden board as inputs.
    Makes the shot and updates the opponent's hidden board accordingly. Returns None."""
    global output_txt
    shot = all_shots[shot_index]
    output_txt += f"Enter your move: {shot}\n\n"
    # Check for missing arguments
    if len(shot.split(",")) < 2 or "" in shot.split(","):
        raise IndexError(f"IndexError: Missing argument. You entered '{shot}' ,"
                         f"the correct format would be such as '3,A'.\n\n")
    # Check for more than 2 arguments
    if len(shot.split(",")) > 2:
        raise ValueError(f"ValueError: Too many arguments. You entered '{shot}' ,"
                         f"the correct format would be such as '3,A'.\n\n")
    # Check the arguments' validation
    if not shot.split(",")[0].isnumeric() or not shot.split(",")[1].isalpha():
        raise ValueError(f"ValueError: Bad arguments. You entered '{shot}' ,"
                         f"the correct format would be such as '3,A'.\n\n")

    pshot_x = int(shot.split(",")[0]) - 1  # Minus 1 to correctly use in board lists
    pshot_y = ord(shot.split(",")[1]) - 65  # Minus 65 to correctly use in board lists

    # Check if the shots are valid
    assert pshot_x in valid_cor
    assert pshot_y in valid_cor

    # Change the board accordingly if it's a miss or shot
    if actual_board[pshot_x][pshot_y] != "-":
        hidden_board[pshot_x][pshot_y] = "X"
    else:
        hidden_board[pshot_x][pshot_y] = "O"


# The output string which will be written into the actual output file
output_txt = ""

# Valid coordinates
valid_cor = [i for i in range(10)]

try:
    # Get the necessary file paths
    cwd = os.getcwd()
    player1txt_path = os.path.join(cwd, sys.argv[1])
    player2txt_path = os.path.join(cwd, sys.argv[2])
    player1in_path = os.path.join(cwd, sys.argv[3])
    player2in_path = os.path.join(cwd, sys.argv[4])
    opt_p1_path = os.path.join(cwd, "OptionalPlayer1.txt")
    opt_p2_path = os.path.join(cwd, "OptionalPlayer2.txt")
    # Test if files are openable using try_paths function
    p_list = [player1txt_path, player2txt_path, player1in_path, player2in_path]
    try_paths(p_list)

    # Get ship location lists
    p1_ships = read_txt(player1txt_path)
    p2_ships = read_txt(player2txt_path)

    # Get shot lists
    p1_shots = read_in(player1in_path)
    p2_shots = read_in(player2in_path)

    # Use ship location lists to generate p1's and p2's actual board
    p1_board = make_ship_board(p1_ships)
    p2_board = make_ship_board(p2_ships)

    # Generate p1's and p2's hidden boards
    p1_hidden_board = make_empty_board()
    p2_hidden_board = make_empty_board()

    # Get ship counters
    p1_ship_count = make_ship_counter()
    p2_ship_count = make_ship_counter()

    # Get p1's and p2's ship positions
    p1_ship_pos = find_ship_pos(p1_board, opt_p1_path)
    p2_ship_pos = find_ship_pos(p2_board, opt_p2_path)

    # Get p1's and p2's ship flags
    p1_ship_flags = make_ship_flags()
    p2_ship_flags = make_ship_flags()

    output_txt += "Battle of Ships Game\n\n"

    p1scount = 0  # Player1's shot count
    p2scount = 0  # Player2's shot count
    round_c = 1  # Round counter

    # Main Loop

    # Continue until one of the player's shots finish
    while p1scount < len(p1_shots) and p2scount < len(p2_shots):
        # Player 1's shot
        output_txt += "Player1's Move\n\n"
        output_txt += f"Round : {round_c}\t\t\t\t\tGrid Size: 10x10\n\n"
        output_txt += show_boards(p1_hidden_board, p2_hidden_board)
        output_txt += show_ship_counter(p1_ship_count, p2_ship_count)

        # Try to make a shot, if it is not valid, add the error message to the output txt and
        # try to make the next shot of the same player
        while True:
            try:
                shot_ship(p1_shots, p1scount, p2_board, p2_hidden_board)
            except IndexError as e:
                output_txt += str(e)
                if p1scount < len(p1_shots):
                    p1scount += 1
                else:
                    break
            except ValueError as e:
                output_txt += str(e)
                if p1scount < len(p1_shots):
                    p1scount += 1
                else:
                    break
            except AssertionError:
                output_txt += "AssertionError: Invalid Operation.\n\n"
                if p1scount < len(p1_shots):
                    p1scount += 1
                else:
                    break
            else:
                break

        check_update_sunk(p2_hidden_board, p2_ship_count, p2_ship_pos, p2_ship_flags)

        # Player 2's shot
        output_txt += "Player2's Move\n\n"
        output_txt += f"Round : {round_c}\t\t\t\t\tGrid Size: 10x10\n\n"
        output_txt += show_boards(p1_hidden_board, p2_hidden_board)
        output_txt += show_ship_counter(p1_ship_count, p2_ship_count)

        while True:
            try:
                shot_ship(p2_shots, p2scount, p1_board, p1_hidden_board)
            except IndexError as e:
                output_txt += str(e)
                if p2scount < len(p2_shots):
                    p2scount += 1
                else:
                    break
            except ValueError as e:
                output_txt += str(e)
                if p2scount < len(p2_shots):
                    p2scount += 1
                else:
                    break
            except AssertionError:
                output_txt += "AssertionError: Invalid Operation.\n\n"
                if p2scount < len(p2_shots):
                    p2scount += 1
                else:
                    break
            else:
                break

        check_update_sunk(p1_hidden_board, p1_ship_count, p1_ship_pos, p1_ship_flags)

        round_c += 1
        p1scount += 1
        p2scount += 1

        # Check if the game has ended

        if check_loss(p1_ship_flags) and check_loss(p2_ship_flags):
            output_txt += "It is a Draw!\n\n"
            break
        elif check_loss(p2_ship_flags):
            output_txt += "Player1 Wins!\n\n"
            break
        elif check_loss(p1_ship_flags):
            output_txt += "Player2 Wins!\n\n"
            break

    # Print final information
    output_txt += "Final Information\n\n"
    p1_final_board = make_final_board(p1_board, p1_hidden_board)
    p2_final_board = make_final_board(p2_board, p2_hidden_board)
    output_txt += "Player1's Board\t\t\t\tPlayer2's Board"
    # Correctly format the boards to get only the board part not the headings
    output_txt += "\n" + show_boards(p1_final_board, p2_final_board).split("\n", 1)[1]
    output_txt += show_ship_counter(p1_ship_count, p2_ship_count)
except IOError as e:
    output_txt += "IOError: input file(s) " + str(e) + " is/are not reachable."
except Exception:
    output_txt += "kaBOOM: run for your life!"
finally:
    # Write the output_txt to an output file
    # Print the output_txt to command line
    print(output_txt)
    with open("Battleship.out", "w") as file:
        file.write(output_txt)
