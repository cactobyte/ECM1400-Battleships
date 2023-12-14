from flask import Flask, render_template, jsonify, request, redirect, url_for
from components import create_battleships, place_battleships, initialise_board
import json
import random

app = Flask(__name__)

player_board = []
attacks = [] # For Harder AI Difficulty
selected_difficulty = "easy" # Can be between "easy", "medium" and "hard"
last_guess = None
ai_hit = False

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

@app.route("/difficulty", methods=["GET", "POST"])
def difficulty():
    if request.method == "POST":
        global selected_difficulty
        selected_difficulty = request.form.get("difficulty")
        return redirect(url_for("placement_interface", difficulty=selected_difficulty))
    return render_template("difficulty.html")


@app.route("/attack", methods=["GET"])
def attack():
    if request.args:                        # Is Triggered every go
        player_x = int(request.args.get("x"))
        player_y = int(request.args.get("y"))

        global last_guess, ai_hit

        # Generate Attack according to difficulty selected
        if selected_difficulty == "easy":
            coordinate = random.randint(0, 9), random.randint(0, 9)
        if selected_difficulty == "medium":
            coordinate = generate_attack()
        if selected_difficulty == "hard":
            if ai_hit is False:
                coordinate = generate_attack()
            if ai_hit:                                              # If AI hit a ship last go, it tries to attack around previous attack
                guess_orientation = random.choice([True, False])    # True = Vertical, False = Horizontal
                random_change = random.randrange(-1, 2, 2)          # Either -1 or 1
                if guess_orientation:
                    coordinate = last_guess[1] + random_change, last_guess[0]
                else:
                    coordinate = last_guess[1], last_guess[0] + random_change

        # AI Attacks Player
        if player_board[coordinate[1]][coordinate[0]] is not None:
            if not player_board[coordinate[1]][coordinate[0]] == "-":
                player_ships[player_board[coordinate[1]][coordinate[0]]] -= 1
                player_board[coordinate[1]][coordinate[0]] = "-"
                last_guess = coordinate[1], coordinate[0]
                ai_hit = True
                print("hit")
        else:
            ai_hit = False
            print("no hit")

        global ai
        ai_board = ai[0]
        ai_ships = ai[1]

        # Player Attacks AI
        if ai_board[player_y][player_x] is not None:
            if not ai_board[player_y][player_x] == "-":
                ai_ships[ai_board[player_y][player_x]] -= 1
                ai_board[player_y][player_x] = "-"
                hit = True  # Player hit an AI ship
        else:
            ai_board[player_y][player_x] = "-"
            hit = False

        game_end = all(value <= 0 for value in player_ships.values()) or all(value <= 0 for value in ai_ships.values())
        if game_end:
            if all(value <= 0 for value in player_ships.values()):
                return jsonify({"hit": hit, "AI_Turn": coordinate, "finished": "Game Over! AI Won"})
            else:
                return jsonify({"hit": hit, "AI_Turn": coordinate, "finished": "Game Over! You Won"})
        else:
            return jsonify({"hit": hit, "AI_Turn": coordinate})


@app.route("/", methods=["GET"])
def root():
    return render_template("main.html", player_board=player_board)


@app.route("/placement", methods=["GET", "POST"])
def placement_interface():
    board_size = 10
    ships = create_battleships()

    if request.method == "GET":
        return render_template("placement.html", ships=ships, board_size=board_size)

    if request.method == "POST":
        data = request.get_json()

        with open("sample.json", "w") as outfile:
            json.dump(data, outfile)

        global player_board
        player_board = place_battleships(initialise_board(10), create_battleships(), "custom", "sample.json")

        return jsonify({"success": True})

    return


if __name__ == "__main__":
    ai = [place_battleships(initialise_board(10), create_battleships(), "random"), create_battleships()]
    player_ships = create_battleships()

    app.template_folder = "templates"
    app.run()

