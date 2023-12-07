from pythongame import Game
import threading as th
import time



def timing(seconds=10, callback=None):
		start = time.time()
		while True:
			if time.time() - start > seconds:
				if callback is not None:
					try:
						callback()
					except:
						return
				break
			time.sleep(1)

class Room:
	def __init__(self, game_id, password, private=False, p1pass=None, p2pass=None):
		self.isdestroyed = False
		self.game_id = game_id
		self.password = password
		self.private = private
		self.p1pass = p1pass
		self.p2pass = p2pass
		self.p1_is_ready = False
		self.p2_is_ready = False
		self.winner = 0
		self.game = Game()
		self.runner = th.Thread(target=self.game.run)
		self.timer()



	def start(self):
		if self.game.state == "menu":
			if self.p1_is_ready and self.p2_is_ready:
				self.game.state = "play"
				self.runner.start()
				return True
			if self.p1_is_ready is False:
				print("p1 not ready")
				self.game_over(2)
				return False
			if self.p2_is_ready is False:
				print("p2 not ready")
				self.game_over(1)
				return False
		print("game already started")
		return False	
		
	def game_over(self, winner):
		self.game.state = "finished"
		self.winner = winner
		timing(60, self.destroy)

	def timer(self):
		thr = th.Thread(target=timing, args=(60, self.start))
		thr.start()


	def be_ready(self, room_password, player, player_pass=None):
		if self.private is False:
			if player == 1:
				self.p1_is_ready = True
			elif player == 2:
				self.p2_is_ready = True
			
			if self.p1_is_ready and self.p2_is_ready:
					self.start()
			return True
		if self.password == room_password:
			if self.p1pass == player_pass:
				self.p1_is_ready = True
			elif self.p2pass == player_pass:
				self.p2_is_ready = True
			if self.p1_is_ready and self.p2_is_ready:
					self.start()
			return True

		return False


	def move_paddle(self, player, direction, player_pass=None):
		if self.private is True:
			if player == 1:
				if self.p1pass != player_pass:
					return False
			elif player == 2:
				if self.p2pass != player_pass:
					return False
		if player == 1:
			self.game.paddle1.move(direction)
		elif player == 2:
			self.game.paddle2.move(direction)
		return True
	

	def get_ball_pos(self):
		return self.game.get_ball_pos()
	
	def get_paddle_pos(self, player):
		if player == 1:
			return self.game.get_p1_pos()
		elif player == 2:
			return self.game.get_p2_pos()
		return None
	
	def get_state(self):
		return self.game.get_state()
	
	def get_result(self):
		return self.game.get_winner()
	
	def destroy(self):
		self.isdestroyed = True