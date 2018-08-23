import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()
		gamelib.debug_write("init")

	def process_config(self, config):
		gamelib.debug_write("config")
		self.config = config
		self.mode = 0
		self.prev_health = 30
		self.prev_wall = {}
		self.sectors = [0,0,0]

	def step(self, game_map):
		wall_locs = [[27,13],[0,13],[26,12],[1,12],[25,11],[2,11],[24,10],[3,10],[23,9],[4,9],[22,8],[5,8],[21,7],[6,7],[20,6],[7,6],[19,5],[8,5],[18,4],[9,4],[17,3],[10,3],[16,2],[11,2]]
		defe_locs = [[
			["DF",[[16,5],[11,5],[18,7],[9,7],[16,9],[11,9],[20,9],[7,9],[18,11],[9,11],[22,11],[5,11],[16,13],[11,13],[24,13],[3,13],[20,13],[7,13],[16,7],[11,7],[18,9],[9,9],[16,11],[11,11],[20,11],[7,11],[18,13],[9,13],[22,13],[5,13]]],
			["FF",[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],[15,13],[12,13]]]
		],[
			["DF",[[16,5],[18,7],[16,7],[18,9],[20,9],[22,11],[20,11],[24,13],[22,13]]],
			["FF",[[16,6],[17,7],[18,8],[19,9],[20,10],[21,11],[22,12],[23,13]]]
		],[
			["DF",[[11,5],[9,7],[11,7],[9,9],[7,9],[5,11],[7,11],[3,13],[5,13]]],
			["FF",[[11,6],[10,7],[9,8],[8,9],[7,10],[6,11],[5,12],[4,13]]]
		],[
			["DF",[[16,5],[11,5],[16,7],[11,7],[16,9],[11,9],[16,11],[11,11],[15,4],[12,4],[15,6],[12,6],[15,8],[12,8],[15,10],[12,10],[15,12],[12,12],[13,11],[14,9],[13,7],[14,5],[13,3],[14,1],[16,3],[11,3]]],
			["FF",[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],[15,3],[12,3]]]
		]]
		encr_locs = [
			[[16,6],[11,6],[16,8],[11,8],[16,10],[11,10],[16,12],[11,12]],
			[[21,10],[19,8],[17,6],[23,12]],
			[[6,10],[8,8],[10,6],[4,12]],
			[[16,4],[11,4],[16,6],[11,6],[16,8],[11,8],[16,10],[11,10],[16,12],[11,12]]
		]

		if game_map.turn_number == 0:
			for loc in wall_locs:
				if game_map.attempt_spawn("FF", loc):
					self.prev_wall[tuple(loc)] = True

		hole = 0
		change = False
		for loc in wall_locs:
			if not game_map.is_blocked(loc):
				key = tuple(loc)
				if self.prev_wall[key]:
					if loc[1] <= 5:
						self.sectors[0] += 1
						change = True
					elif loc[1] >= 10:
						if loc[0] >= 14:
							self.sectors[1] += 1
						else:
							self.sectors[2] += 1
						change = True
					self.prev_wall[key] = False
				if game_map.attempt_spawn("DF", loc):
					self.prev_wall[key] = True
				else:
					hole += 1

		if change:
			if self.sectors[1] > 2 and self.sectors[1] > self.sectors[2] * 2:
				self.mode = 1
			elif self.sectors[2] > 2 and self.sectors[2] > self.sectors[1] * 2:
				self.mode = 2
			elif self.sectors[0] > 0:
				self.mode = 3
			elif self.sectors[1] > 2 and self.sectors[2] > 2:
				self.mode = 0
			gamelib.debug_write("{} MODE:{}".format(self.sectors, self.mode))
		elif not hole and game_map.my_integrity < self.prev_health:
			self.mode = 3
			gamelib.debug_write("{} MODE:{}".format(self.sectors, self.mode))
		self.prev_health = game_map.my_integrity

		defe = defe_locs[self.mode]
		game_map.attempt_spawn_multiple(defe[0][0], defe[0][1])
		if not hole:
			game_map.attempt_spawn_multiple(defe[1][0], defe[1][1])

		if math.floor(game_map.bits_in_future()) - math.floor(game_map.get_resource("bits")) < 4:
			gamelib.debug_write("turn:{} health:{}".format(game_map.turn_number, int(game_map.my_integrity)))
			game_map.attempt_spawn_multiple("EF", encr_locs[self.mode])

			if self.mode == 1:
				loc = [13,0]
			elif self.mode == 2:
				loc = [14,0]
			else:
				loc = random.choice([[13,0],[14,0]])

			while game_map.get_resource("bits") >= 1:
				game_map.attempt_spawn("PI", loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
