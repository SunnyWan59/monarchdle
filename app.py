from flask import Flask, request, jsonify
import random
import json

app = Flask(__name__)

# Mock data 
with open('./monarchs/english_monarchs.json', 'r') as file:
    monarchs = json.load(file)

# Initialize game state
current_Monarch = None

@app.route("/start", methods=["POST"])
def start_game():
    global current_Monarch
    current_Monarch = random.choice(monarchs)
    return jsonify({"message": "Game started!", "hint": "Guess the monarch based on the clues!"})

@app.route("/clue/<clue_type>", methods=["GET"])
def get_clue(clue_type):
    if not current_Monarch:
        return jsonify({"error": "Start the game first using /start"}), 400

    clue = current_Monarch.get(clue_type)
    if clue:
        return jsonify({clue_type: clue})
    else:
        return jsonify({"error": f"Clue type '{clue_type}' not available."}), 400

@app.route("/guess", methods=["POST"])
def guess_champion():
    if not current_Monarch:
        return jsonify({"error": "Start the game first using /start"}), 400

    data = request.get_json()
    if not data or "guess" not in data:
        return jsonify({"error": "You must provide a guess in the request body."}), 400

    guess = data["guess"]
    if guess.lower() == current_Monarch["name"].lower():
        return jsonify({"result": "Correct!", "champion": current_Monarch})
    else:
        return jsonify({"result": "Incorrect. Try again!"})

@app.route("/end", methods=["POST"])
def end_game():
    global current_Monarch
    if not current_Monarch:
        return jsonify({"error": "No game in progress."}), 400

    finished_champion = current_Monarch
    current_Monarch = None
    return jsonify({"message": "Game ended.", "champion": finished_champion})

if __name__ == "__main__":
    app.run(debug=True)
