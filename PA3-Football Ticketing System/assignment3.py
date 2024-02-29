import sys
import os
import string

# Ömer Kayra Çetin
# 2210356060

# Environmental Variables

CURRENT_PATH = os.getcwd()
INPUT_FILE_NAME = sys.argv[1]
INPUT_FILE_PATH = os.path.join(CURRENT_PATH, INPUT_FILE_NAME)
OUTPUT_FILE_NAME = "output.txt"
OUTPUT_FILE_PATH = os.path.join(CURRENT_PATH, OUTPUT_FILE_NAME)

# Global Variables

categories = dict()  # This is a dictionary of category names and their values
list_of_alphabet = string.ascii_uppercase


def read_input():
    with open(INPUT_FILE_PATH) as file:
        return [l.replace("\n", "") for l in file.readlines()]  # Return the lines in a list without new line chars


def write_output(output):
    with open(OUTPUT_FILE_PATH, "a") as file:
        file.write(output)
        return output  # Returns the output for it to be used in a print statement


def create_category(*args):
    global categories
    category_name = args[0]  # First argument is category name
    if category_name not in categories:
        row, column = args[1].split("x")  # Second argument is row and column
        seat_number = int(row)*int(column)
        # For every row char key, there is a list of seats according to column number
        # Since row and column are strings, I convert them to integers
        category = {list_of_alphabet[i]: ["X" for _ in range(int(column))] for i in range(int(row))}
        categories[category_name] = category
        print(write_output(f"The category '{category_name}' having {seat_number} seats has been created\n"), end="")
    else:
        message = f"Warning: Cannot create the category for the second time. " \
                  f"The stadium has already {category_name}\n"
        print(write_output(message), end="")


def sell_ticket(*args):
    name = args[0]
    payment = args[1]
    if payment == "student":
        payment_char = "S"
    elif payment == "full":
        payment_char = "F"
    else:
        payment_char = "T"
    category_name = args[2]
    category = categories[category_name]
    column_num = len(category["A"])  # I choose an arbitrary column to get its length
    seats = args[3:]
    for seat in seats:
        # Check if it's an only seat or seat segment
        if "-" in seat:
            column = int(seat.split("-")[1])  # If it's a seat segment get the last seat wanted to be bought
        else:
            column = int(seat[1:])
        row = seat[0]
        # Check if the seat's row and column are in the category's boundries
        if row not in category and column > column_num:
            message = f"Error: The category '{category_name}' has less row and column than the specified " \
                      f"index {seat}!\n"
        elif row not in category:
            message = f"Error: The category '{category_name}' has less row than the specified index {seat}!\n"
        elif column > column_num:
            message = f"Error: The category '{category_name}' has less column than the specified index {seat}!\n"
        else:
            if "-" in seat:
                # If it's a seat segment get the start and end
                start_column = int(seat[1:].split("-")[0])
                end_column = int(seat[1:].split("-")[1])
                # Check if any of the seats that wanted to be bought are already sold
                its_sold = False
                for i in range(start_column, end_column+1):
                    if category[row][i] != "X":
                        its_sold = True
                if its_sold:
                    message = f"Error: The seats {seat} cannot be sold to {name} due some of them " \
                              f"have already been sold!\n"
                else:
                    message = f"Success: {name} has bought {seat} at {category_name}\n"
                    for i in range(start_column, end_column + 1):
                        category[row][i] = payment_char
            else:
                # If it's an only seat
                if category[row][column] == "X":
                    message = f"Success: {name} has bought {seat} at {category_name}\n"
                    category[row][column] = payment_char
                else:
                    message = f"Error: The seat {seat} cannot be sold to {name} since it was already sold!\n"
        print(write_output(message), end="")


def cancel_ticket(*args):
    category_name = args[0]
    category = categories[category_name]
    column_num = len(category["A"])
    seats = args[1:]
    for seat in seats:
        row = seat[0]
        column = int(seat[1:])
        # Check if the seat's row and column are in the category's boundries
        if row not in category and column > column_num:
            message = f"Error: The category '{category_name}' has less row and column than the specified " \
                      f"index {seat}!\n"
        elif row not in category:
            message = f"Error: The category '{category_name}' has less row than the specified index {seat}!\n"
        elif column > column_num:
            message = f"Error: The category '{category_name}' has less column than the specified index {seat}!\n"
        else:
            if category[row][column] == "X":
                message = f"Error: The seat {seat} at '{category_name}' has already been free! Nothing to cancel\n"
            else:
                category[row][column] = "X"
                message = f"Success: The seat {seat} at '{category_name}' " \
                          f"has been canceled and now ready to sell again\n"
        print(write_output(message), end="")


def balance(*args):
    category_name = args[0]
    category = categories[category_name]
    student = 0
    full = 0
    season = 0
    header = f"Category report of {category_name}\n"
    header_length = len(header)-1
    dashes = header_length * "-" + "\n"
    print(write_output(header), end="")
    print(write_output(dashes), end="")
    for row in category:
        for seat in category[row]:
            if seat == "S":
                student += 1
            elif seat == "F":
                full += 1
            elif seat == "T":
                season += 1
    revenue = (10 * student) + (20 * full) + (250 * season)
    message = f"Sum of students = {student}, Sum of full pay = {full}, Sum of season ticket = {season}, " \
              f"and Revenues = {revenue} Dollars\n"
    print(write_output(message), end="")


def show_category(*args):
    category_name = args[0]
    category = categories[category_name]
    print(write_output(f"Printing category layout of {category_name}\n\n"), end="")
    # Print it starting from the last row
    for row_index in range(len(category)-1, -1, -1):
        row_char = list_of_alphabet[row_index]
        row = category[row_char]
        line = ""
        line += row_char + " "
        for seat in row:
            line += "%-3s" % seat
        line += "\n"
        print(write_output(line), end="")
    line = ""
    column_number = len(category["A"])  # Get the column number
    for index in range(column_number):
        line += "%3d" % index
    line += "\n"
    print(write_output(line), end="")


# Read the input file line by line into a list
input_file = read_input()
# Main loop
for command_line in input_file:
    # Seperate command from its arguments
    command = command_line.split(" ")[0]
    arguments = command_line.split(" ")[1:]
    # Check which command to execute and pass its arguments to the correct function
    if command == "CREATECATEGORY":
        create_category(*arguments)
    elif command == "SELLTICKET":
        sell_ticket(*arguments)
    elif command == "CANCELTICKET":
        cancel_ticket(*arguments)
    elif command == "BALANCE":
        balance(*arguments)
    elif command == "SHOWCATEGORY":
        show_category(*arguments)
