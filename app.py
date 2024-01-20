#flask api

from flask import Flask, jsonify, request, Response, abort
from flask_cors import CORS
from Room import Room
from datetime import datetime, timedelta

endpointroot = '/api'



app = Flask(__name__)
CORS(app)
games = []

ip_request_count = {}

max_requests_per_minute = 100000

# @app.before_request
# def limit_request():
#     ip = request.remote_addr

#     if ip not in ip_request_count:
#         ip_request_count[ip] = {'count': 1, 'timestamp': datetime.now()}
#     else:
#         if datetime.now() - ip_request_count[ip]['timestamp'] > timedelta(minutes=1):
#             ip_request_count[ip] = {'count': 1, 'timestamp': datetime.now()}
#         else:
#             if ip_request_count[ip]['count'] >= max_requests_per_minute:
#                 abort(429)  # Too Many Requests HTTP kodu ile isteği reddet

#             ip_request_count[ip]['count'] += 1

@app.route(endpointroot + "/ping" , methods=['GET'])
def ping():
	return jsonify({'response': 'pong!'})

@app.route(endpointroot+"/ping" , methods=['POST'])
def post_ping():
	data = request.get_json()
	return jsonify(data), 201


@app.route(endpointroot+"/new_game", methods=['POST'])
def new_game():
	data = request.get_json()
	password = data['password']
	gameid = data['gameid']
	private = data['private']
	password_p1 = None
	password_p2 = None
	if private == True:
		password_p1 = data['password_p1']
		password_p2 = data['password_p2']
	for game in games:
		if game.isdestroyed:
			games.remove(game)
	for game in games:
		if game.game_id == gameid:
			return jsonify({'response': 'game already exists'}), 409
	if games.count(gameid) > 0:
		return jsonify({'response': 'game already exists'}), 409
	if games.__len__() > 2:
		return jsonify({'response': 'server full'}), 503
	games.append(Room(gameid, password, private, password_p1, password_p2))
	return jsonify({'response': 'game created'}), 201


def get_game(gameid):
	for game in games:
		if game.game_id == gameid:
			return game
	return None


@app.route(endpointroot+"/join_game", methods=['POST'])
def join_game():
	print("join_game")
	data = request.get_json()
	gameid = data['gameid']
	password = data['password']
	player = data['player']
	player_pass = None
	try:
		player_pass = data['player_pass']
	except KeyError:
		pass

	game = get_game(gameid)
	if game is None:
		return jsonify({'response': 'game does not exist'}), 404
	
	if game.be_ready(password, player, player_pass):
		return jsonify({'response': 'game joined'}), 200
	return jsonify({'response': 'wrong password'}), 401


@app.route(endpointroot+"/move", methods=['POST'])
def move():
	data = request.get_json()
	gameid = data['gameid']
	player = data['player']
	password = data['password']
	direction = data['direction']
	player_pass = None
	try:
		player_pass = data['player_pass']
	except KeyError:
		pass
	game = get_game(gameid)
	print(direction)
	if game is None:
		return jsonify({'response': 'game does not exist'}), 404
	if game.password != password:
		return jsonify({'response': 'wrong password'}), 401
	if game.move_paddle(player, direction, player_pass):
		print("succes")
		return jsonify({'response': 'paddle moved'}), 200
	print("not")
	return jsonify({'response': 'wrong password'}), 401




@app.route( endpointroot + '/info/<string:gameid>', methods=['GET'])
def get_state(gameid):
	game = get_game(gameid)
	if game is None:
		return jsonify({'response': 'game does not exist'}), 404
	ball_pos = game.get_ball_pos()
	p1_pos = game.get_paddle_pos(1)
	p2_pos = game.get_paddle_pos(2)
	state = game.get_state()
	score1 = game.game.score1
	score2 = game.game.score2
	print(p1_pos, p2_pos)
	return jsonify({'ball_pos': ball_pos, 'p1_pos': p1_pos, 'p2_pos': p2_pos, 'state': state, 'score1': score1, 'score2': score2}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2700)
