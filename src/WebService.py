#!/usr/bin/env python
from flask import Flask, request, abort, jsonify

from ConnectFourAI import ConnectFourPlayboard
from ConnectFourAI import ConnectFourPlayerMinimaxAlphaBeta

app = Flask(__name__)

class Game:
	playboard = ConnectFourPlayboard()
	ai = ConnectFourPlayerMinimaxAlphaBeta(playboard, ConnectFourPlayboard.RED, 8)

games = {0: Game()}


@app.route('/games', methods=['ADD'])
def create():
	id = len(games)
	games[id] = Game()
	return jsonify({'id': id}), 201

@app.route('/games/<int:id>', methods=['GET'])
def get(id):
	if not id in games:
		abort(404)
	
	playboard = games[id].playboard

	 return jsonify({'playboard': [[playboard.GetField(i,j) for j in range(playboard.GetColumns())] for i in range(playboard.GetRows())], 
			 'winner': playboard.GetWinner() })
		
@app.route('/games/<int:id>/<int:column>', methods=['MOVE'])
def move(id, column):
	if not id in games:
		abort(404)

	playboard = games[id].playboard
	ai = games[id].ai

	playboard.MoveWhite(column)

	ai_move = ai.MakeMove()

	return jsonify({'ai': ai_move})

if __name__ == '__main__':
    app.run(debug=True)
