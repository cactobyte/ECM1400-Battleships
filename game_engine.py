from pip import __main__

from components import initialise_board, create_battleships, place_battleships


def attack(coordinates, board, battleships):
    if board[coordinates[1]][coordinates[0]] is not None:
        ship_name = board[coordinates[1]][coordinates[0]]
        battleships[ship_name] -= 1
        board[coordinates[1]][coordinates[0]] = None
        hit = True
    elif board[coordinates[1]][coordinates[0]] is None:
        hit = False
    return hit


def cli_coordinates_input():
    try:
        X_coordinate = int(input("Input an X coordinate (0-9): "))
        Y_coordinate = int(input("Input an Y coordinate (0-9): "))
        if -1 < Y_coordinate < 10 and -1 < X_coordinate < 10:
            return X_coordinate, Y_coordinate                       # Add some third variable
        else:
            print("Please enter a valid number between 0-9")
            cli_coordinates_input()
    except ValueError:
        print("You entered an invalid number")
        cli_coordinates_input()


def simple_game_loop():
    print("Welcome to Battleships!")
    board = initialise_board(10)
    ships = create_battleships()
    number_of_ships = len(ships)
    place_battleships(board, ships)
    while number_of_ships > 0:
        coordinates = cli_coordinates_input()                       # Add third variable check
        ship_name = board[coordinates[1]][coordinates[0]]
        hit = attack(coordinates, board, ships)
        if hit:
            print("You hit a ship")
            if ships[ship_name] == 0:
                number_of_ships -= 1
        elif not hit:
            print("You did not hit a ship")
    print("You have sunken all ships")


if __name__ == "__main__":
    simple_game_loop()
