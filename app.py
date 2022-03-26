import json
from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}.
    >>> my_new_game = new_game()
    >>> my_new_game
    {'gameId': 'b8d2639c-21bd-4aa3-9a92-524ef979c6fe',
    'board':
    [['L', 'K', 'E', 'L', 'T'],
    ['D', 'K', 'S', 'K', 'E'],
    ['A', 'A', 'L', 'N', 'P'],
    'P', 'I', 'A', 'T', 'E'],
    ['A', 'R', 'J', 'U', 'A']]}
    >>> games
    {'b8d2639c-21bd-4aa3-9a92-524ef979c6fe':
    <BoggleGame board=LKELT.DKSKE.AALNP.PIATE.ARJUA played_words=set()>}
    >>> """
    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")
def is_word_legal():
    """{gameId: someID, word: some_word}"""
    request_data = request.get_json()
    gameId = request_data["gameId"]
    word = request_data["word"].upper()
    game = games[gameId]

    if not game.is_word_in_word_list(word):
        return jsonify({"result" : "not-word"})
    elif not game.check_word_on_board(word):
        return jsonify({"result" : "not-on-board"})
    else:
        return jsonify({"result": "ok"})




