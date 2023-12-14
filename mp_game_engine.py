import random
from components import initialise_board, create_battleships, place_battleships
from game_engine import cli_coordinates_input, attack

players = {"Player": None,
           "AI": None}
attacks = []


def generate_attack():
    global attacks
    x_coordinate = random.randint(0, 9)
    y_coordinate = random.randint(0, 9)
    coordinate = x_coordinate, y_coordinate
    if coordinate in attacks:
        generate_attack()
    else:
        attacks.append(coordinate)
        return x_coordinate, y_coordinate
    return


def ai_opponent_game_loop():
    print("Welcome to Battleships")
    players["Player"] = [place_battleships(initialise_board(10), create_battleships(), "custom"), create_battleships()]
    players["AI"] = [place_battleships(initialise_board(10), create_battleships(), "random"), create_battleships()]
    game_end = False

    while not game_end:
        coordinates = cli_coordinates_input()
        hit = attack(coordinates, players["AI"][0], players["AI"][1])
        if hit:
            print("You hit a ship")
        elif not hit:
            print("You did not hit a ship")

        print("The AI is attacking...")
        hit = attack(generate_attack(), players["Player"][0], players["Player"][1])
        if hit:
            print("AI hit a ship")
        elif not hit:
            print("AI did not hit a ship")

        print("Lets take a look at your board: ")
        for row in players["Player"][0]:
            current_row = ""
            for column in row:
                if column is None:
                    current_row += "o "
                else:
                    current_row += "x "
            print(current_row)

        game_end = all(value == 0 for value in players["Player"][1].values()) or all(value == 0 for value in players["AI"][1].values())
    print("Game Over!")


ai_opponent_game_loop()
