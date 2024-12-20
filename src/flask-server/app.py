from flask import Flask, request, jsonify
import random
import json

app = Flask(__name__)

"""
Just for now. Not good for production.
TODO: Move this to a SQLite database.
"""
with open('../../src/monarchs/english_monarchs.json', 'r') as file:
    monarchs = json.load(file)

# Initialize game state
global current_Monarch
current_Monarch = None


@app.route("/api/monarch", methods=["GET, POST"])
def monarch():
    if request.method == "POST":
        current_Monarch = random.choice(monarchs)
        return jsonify({"message": "Monarch updated!"})
    elif request.method == "GET":
        if not current_Monarch:
            current_Monarch = random.choice(monarchs)
        return current_Monarch
    
    
@app.route("/api/hint", methods=["GET","PUT"])
def get_champion_hint():
    """Get a hint for the current Monarch. Might not be needed."""
    return jsonify({
        "hint": {
            "role": current_Monarch["role"],
            "releaseYear": current_Monarch["releaseYear"],
            "region": current_Monarch["region"],
        }
    })

def replace_ligatures(text):
    """
    Replace ligatures with their ASCII counterparts. This is primarily for the Early English kings.
    """
    # Dictionary of ligatures and their UTF-8 counterparts
    ligatures = {
        'æ': 'ae',  # Latin small ligature AE
        'Æ': 'AE',  # Latin capital ligature AE
        'œ': 'oe',  # Latin small ligature OE
        'Œ': 'OE',  # Latin capital ligature OE
    }
    for ligature, utf_char in ligatures.items():
        text = text.replace(ligature, utf_char)
    return text

def process_guess(guess: str):
    """Process the user's guess."""
    guess = replace_ligatures(guess.strip().replace('').lower())
    return guess

@app.route("/api/guess", methods=["POST"])
def check_guess():
    """Validate the user's guess."""
    data = request.json
    guess = data.get("guess", "").strip().lower()
    if guess == current_Monarch["name"].lower():
        return jsonify({"correct": True, "monarch": current_Monarch["name"]})
    return jsonify({"correct": False})


@app.route("/api/restart", methods=["POST"])
def restart_game():
    """Restart the game with a new monarch."""
    current_Monarch = random.choice(monarchs)
    return jsonify({"message": "Game restarted!"})


@app.route("/api/test")
def test():
    return jsonify({
        "name": "William III",
        "portrait": "src/python/monarchs/england/William_III.jpg",
        "start_year": "",
        "end_year": "8 March 1702",
        "reign_time": "13 years, 24 days",
        "country": "England"
    })

if __name__ == "__main__":
    app.run()
