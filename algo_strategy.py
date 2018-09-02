import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()
		self.mode = 0
		self.prev_health = 30
		self.prev_wall = {}
		self.paths = [0,0,0]
		self.sectors = [0,0,0]
		self.wall = [[27,13],[0,13],[26,12],[1,12],[25,11],[2,11],[24,10],[3,10],[23,9],[4,9],[22,8],[5,8],[21,7],[6,7],[20,6],[7,6],[19,5],[8,5],[18,4],[9,4],[17,3],[10,3],[16,2],[11,2]]
		self.defe = [[
			["DF",[[16,5],[11,5],[18,7],[9,7],[16,9],[11,9],[20,9],[7,9],[18,11],[9,11],[22,11],[5,11],[16,13],[11,13],[24,13],[3,13],[20,13],[7,13],
				   [16,7],[11,7],[18,9],[9,9],[16,11],[11,11],[20,11],[7,11],[18,13],[9,13],[22,13],[5,13]]],
			["FF",[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],[15,13],[12,13]]]
		],[
			["DF",[[16,5],[11,5],[16,7],[11,7],[16,9],[11,9],[16,11],[11,11],
				   [13,11],[14,9],[13,7],[14,5],[13,3],[14,1],
				   [15,4],[12,4],[15,6],[12,6],[15,8],[12,8],[15,10],[12,10],[15,12],[12,12],
				   [16,3],[11,3]]],
			["FF",[[15,5],[12,5],[15,7],[12,7],[15,9],[12,9],[15,11],[12,11],
				   [15,3],[12,3]]]
		],[
			["DF",[[16,5],[18,7],[16,7],[18,9],[20,9],[22,11],[20,11],[24,13],[22,13]]],
			["FF",[[10+i,i] for i in range(6,14)]]
		],[
			["DF",[[11,5],[9,7],[11,7],[9,9],[7,9],[5,11],[7,11],[3,13],[5,13]]],
			["FF",[[17-i,i] for i in range(6,14)]]
		],[
			["DF",[[0,13],[1,13],[1,12],[2,13],[2,12],[2,11],[3,13],[3,12],[4,13]]],
			["FF",[[5,13],[4,12],[3,11]]]
		],[
			["DF",[[27,13],[26,13],[26,12],[25,13],[25,12],[25,11],[24,13],[24,12],[23,13]]],
			["FF",[[22,13],[23,12],[24,11]]]
		]]
		self.offe = [[
			["EF",[[16,6],[11,6],[16,8],[11,8],[16,10],[11,10],[16,12],[11,12]]]
		],[
			["EF",[[16,4],[11,4],[16,6],[11,6],[16,8],[11,8],[16,10],[11,10],[16,12],[11,12]]]
		],[
			["EF",[[21,10],[19,8],[17,6],[23,12]]]
		],[
			["EF",[[6,10],[8,8],[10,6],[4,12]]]
		],[
			["FF",[[11+i,i] for i in range(13,0,-1)]],
			["EF",[[12+i,i] for i in range(13,0,-1)]]
		],[
			["FF",[[16-i,i] for i in range(13,0,-1)]],
			["EF",[[15-i,i] for i in range(13,0,-1)]]
		]]

	def process_config(self, config):
		self.config = config

	def step(self, game_map):
		hole = 0
		if game_map.turn_number == 0:
			for loc in self.wall:
				if game_map.attempt_spawn("FF", loc):
					self.prev_wall[tuple(loc)] = True
		elif self.mode < 4:
			path = game_map.find_path_to_edge([1,13], "top_left")
			self.paths[0] += len(path[0]) if path[1] else 28
			path = game_map.find_path_to_edge([26,13], "top_right")
			self.paths[2] += len(path[0]) if path[1] else 28
			path = game_map.find_path_to_edge([13,13], "top_left")
			left = len(path[0]) if path[1] else 28
			path = game_map.find_path_to_edge([14,13], "top_right")
			right = len(path[0]) if path[1] else 28
			self.paths[1] += left if left < right else right

			change = False
			for loc in self.wall:
				if not game_map.is_blocked(loc):
					key = tuple(loc)
					if self.prev_wall[key]:
						if loc[1] <= 5:
							self.sectors[1] += 1
							change = True
						elif loc[1] >= 10:
							if loc[0] < 14:
								self.sectors[0] += 1
							else:
								self.sectors[2] += 1
							change = True
						self.prev_wall[key] = False
					if game_map.attempt_spawn("DF", loc):
						self.prev_wall[key] = True
					else:
						hole += 1

			if change:
				if self.sectors[0] > 2 and self.sectors[0] > self.sectors[2] * 2:
					if self.paths[0] < self.paths[2] and self.paths[0] < self.paths[1]:
						game_map.attempt_remove_multiple([[14,1],[15,3],[16,3],[16,4]])
						game_map.attempt_remove_multiple(game_map.get_edge_locations("bottom_right"))
						self.mode = 4
					else:
						game_map.attempt_remove_multiple([[14,1],[12,3],[11,3],[11,4]])
						self.mode = 3
					gamelib.debug_write("paths:{}".format(self.paths))
				elif self.sectors[2] > 2 and self.sectors[2] > self.sectors[0] * 2:
					if self.paths[2] < self.paths[0] and self.paths[2] < self.paths[1]:
						game_map.attempt_remove_multiple([[14,1],[12,3],[11,3],[11,4]])
						game_map.attempt_remove_multiple(game_map.get_edge_locations("bottom_left"))
						self.mode = 5
					else:
						game_map.attempt_remove_multiple([[14,1],[15,3],[16,3],[16,4]])
						self.mode = 2
					gamelib.debug_write("paths:{}".format(self.paths))
				elif self.sectors[1] > 0:
					self.mode = 1
				elif self.sectors[0] > 2 and self.sectors[2] > 2:
					self.mode = 0
				gamelib.debug_write("{} MODE:{}".format(self.sectors, self.mode))
			elif not hole and game_map.my_integrity < self.prev_health:
				self.mode = 1
				gamelib.debug_write("{} MODE:{}".format(self.sectors, self.mode))
			self.prev_health = game_map.my_integrity

		defe = self.defe[self.mode]
		game_map.attempt_spawn_multiple(defe[0][0], defe[0][1])
		if not hole:
			game_map.attempt_spawn_multiple(defe[1][0], defe[1][1])

		if math.floor(game_map.bits_in_future()) - math.floor(game_map.get_resource("bits")) < 4:
			gamelib.debug_write("{} health:{} enemy:{}".format(game_map.turn_number, int(game_map.my_integrity), int(game_map.enemy_integrity)))
			for offe in self.offe[self.mode]:
				game_map.attempt_spawn_multiple(offe[0], offe[1])

			if self.mode == 2 or self.mode == 4:
				loc = [13,0]
			elif self.mode == 3 or self.mode == 5:
				loc = [14,0]
			else:
				loc = random.choice([[13,0],[14,0]])

			while game_map.get_resource("bits") >= 1:
				if self.mode >= 4:
					game_map.attempt_spawn("EI", loc)
					game_map.attempt_spawn("SI", loc)
				else:
					game_map.attempt_spawn("PI", loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
