import random
import json

def initialise_board(size=10):
    board = []
    for rows in range(size):
        row_list = []
        for columns in range(size):
            row_list.append(None)
        board.append(row_list)

    return board


def create_battleships(filename="battleships.txt"):
    battleships = {}

    file = open(filename, "r")
    for line in file:
        name, size = line.split(":")
        battleships[name] = int(size)

    return battleships


def place_battleships(board, ships, type="custom", filename="placement.json"):
    # Simple Algorithm
    if type == "simple":
        ship_names = list(ships)
        for y in range(0, len(ships)):
            ship_size = ships[ship_names[y]]
            for i in range(0, ship_size):
                board[y][i] = ship_names[y]

    # Random Algorithm
    if type == "random":
        for ship in ships:
            ship_placed = False
            while not ship_placed:
                do_not_place = False
                ship_vertical = random.choice([True, False])  # Using Boolean as orientation is binary    is a binary value
                ship_size = ships[ship]
                if ship_vertical:
                    random_column = random.randint(0, len(board) - 1)
                    starting_row = random.randint(0, len(board) - ship_size)
                    for i in range(starting_row, starting_row + ship_size):
                        if board[i][random_column] is not None:
                            do_not_place = True
                    if not do_not_place:
                        for i in range(starting_row, starting_row + ship_size):
                            board[i][random_column] = ship
                            ship_placed = True
                if not ship_vertical:
                    random_row = random.randint(0, len(board) - 1)
                    starting_column = random.randint(0, len(board) - ship_size)
                    for i in range(starting_column, starting_column + ship_size):
                        if board[random_row][i] is not None:
                            do_not_place = True
                    if not do_not_place:
                        for i in range(starting_column, starting_column + ship_size):
                            board[random_row][i] = ship
                            ship_placed = True

    # Custom Placement
    if type == "custom":
        f = open(str(filename))
        data = json.load(f)
        for ship in ships:
            ship_size = ships[ship]
            if data[ship][2] == "h":
                for i in range(0, ship_size):
                    board[int(data[ship][1])][int(data[ship][0]) + i] = ship
            elif data[ship][2] == "v":
                for i in range(0, ship_size):
                    board[int(data[ship][1]) + i][int(data[ship][0])] = ship
        f.close()

    return board




