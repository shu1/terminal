import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()

		gamelib.debug_write("init")
		self.mode = 0
		self.prev_health = 30
		self.prev_wall = {}
		self.sectors   = [0,0,0]
		self.wall_locs = [[27,13],[0,13],[26,12],[1,12],[25,11],[2,11],[24,10],[3,10],[23,9],[4,9],[22,8],[5,8],[21,7],[6,7],[20,6],[7,6],[19,5],[8,5],[18,4],[9,4],[17,3],[10,3],[16,2],[11,2]]
		self.dest_locs = [
			[[15,5],[12,5],[17,7],[10,7],[15,9],[12,9],[19,9],[8,9],[17,11],[10,11],[21,11],[6,11],[15,13],[12,13],[23,13],[4,13],[19,13],[8,13],[15,7],[12,7],[17,9],[10,9],[15,11],[12,11],[19,11],[8,11],[17,13],[10,13],[21,13],[6,13]],
			[[15,5],[17,7],[15,7],[17,9],[19,9],[21,11],[19,11],[23,13],[21,13]],
			[[12,5],[10,7],[12,7],[10,9],[8,9],[6,11],[8,11],[4,13],[6,13]],
			[[15,5],[12,5],[17,7],[10,7],[15,7],[12,7],[17,9],[10,9],[15,9],[12,9],[15,11],[12,11],[17,11],[10,11],[15,13],[12,13],[17,13],[10,13]]
		]
		self.filt_locs = [
			[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],[15,13],[12,13]],# mode 0 shifted out
			[[16,6],[17,7],[18,8],[19,9],[20,10],[21,11],[22,12],[23,13]],
			[[11,6],[10,7],[9,8],[8,9],[7,10],[6,11],[5,12],[4,13]],
			[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],[15,13],[12,13]]	# mode 3 shifted out
#			[[18,8],[9,8],[18,10],[9,10],[18,12],[9,12]]	# mode 3 shifted in
		]
		self.encr_locs = [
			[],	# [[16,11],[11,11],[20,11],[7,11],[18,9],[9,9],[16,7],[11,7],[18,13],[9,13],[22,13],[5,13]],	# mode 0 Encryptors
			[[21,10],[19,8],[17,6],[23,12]],
			[[6,10],[8,8],[10,6],[4,12]],
			[[16,10],[11,10],[16,8],[11,8],[16,6],[11,6],[16,12],[11,12]]
		]
		self.shift(self.dest_locs, 1)
#		self.shift(self.filt_locs, -1)
#		self.shift(self.encr_locs, -1)

	def shift(self, locs, i):
		for a in locs:
			for b in a:
				if b[0] < 14:
					b[0] -= i
				else:
					b[0] += i

	def process_config(self, config):
		gamelib.debug_write("config")
		self.config = config

	def step(self, game_map):
		gamelib.debug_write("turn:{} health:{}".format(game_map.turn_number, int(game_map.my_integrity)))

		if game_map.turn_number == 0:
			for i, loc in enumerate(self.wall_locs):
				game_map.attempt_spawn("FF", loc)
				self.prev_wall[tuple(loc)] = True

		wall_holes = 0
		change_mode = False
		for i, loc in enumerate(self.wall_locs):
			if not game_map.is_blocked(loc):
				key = tuple(loc)
				if self.prev_wall[key]:
					if loc[1] <= 5:
						self.sectors[0] += 1
						change_mode = True
					elif loc[1] >= 10:
						if loc[0] >= 14:
							self.sectors[1] += 1
						else:
							self.sectors[2] += 1
						change_mode = True
					self.prev_wall[key] = False
				if game_map.attempt_spawn("DF", loc):
					self.prev_wall[key] = True
				else:
					wall_holes += 1

		if change_mode:
			if self.sectors[1] > 2 and self.sectors[1] > self.sectors[2] * 2:
				self.mode = 1
			elif self.sectors[2] > 2 and self.sectors[2] > self.sectors[1] * 2:
				self.mode = 2
			elif self.sectors[0] > 0:
				self.mode = 3
			elif self.sectors[1] > 2 and self.sectors[2] > 2:
				self.mode = 0
			gamelib.debug_write("{} mode:{}".format(self.sectors, self.mode))
		elif not wall_holes and game_map.my_integrity < self.prev_health:
			self.mode = 3
			gamelib.debug_write("{} mode:{}".format(self.sectors, self.mode))
		self.prev_health = game_map.my_integrity

		game_map.attempt_spawn_multiple("DF", self.dest_locs[self.mode])
		if not wall_holes:
			game_map.attempt_spawn_multiple("FF", self.filt_locs[self.mode])
		game_map.attempt_spawn_multiple("EF", self.encr_locs[self.mode])

		if self.mode == 1:
			spawn_loc = random.choice([[12,1],[13,0]])
		elif self.mode == 2:
			spawn_loc = random.choice([[14,0],[15,1]])
		else:
			spawn_loc = random.choice([[12,1],[13,0],[14,0],[15,1]])

		while game_map.get_resource("bits") >= 1:
			game_map.attempt_spawn("EI", spawn_loc)
			game_map.attempt_spawn("SI", spawn_loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
