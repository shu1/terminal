import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()
		gamelib.debug_write("init")
		self.mode = 1

	def process_config(self, config):
		gamelib.debug_write("config")
		self.config = config

	def step(self, game_map):
		gamelib.debug_write("turn:{} health:{}".format(game_map.turn_number, int(game_map.my_integrity)))

		if game_map.turn_number == 0:
			game_map.attempt_spawn_multiple("DF", [[3,13],[24,13],[7,9],[20,9],[11,11],[16,11]])

		filt_locs = [[24,13],[23,12],[22,11],[21,10],[20,9],[19,8],[18,7],[17,6],[16,5],[15,4],[14,3],[13,2],[12,1]]
		encr_locs = [[25,13],[24,12],[23,11],[22,10],[21,9],[20,8],[19,7],[18,6],[17,5],[16,4],[15,3],[14,2],[13,1]]
		offe_locs = [
			["FF",
			filt_locs,
			filt_locs,
			[[3,13],[4,12],[5,11],[6,10],[7,9],[8,8],[9,7],[10,6],[11,5],[12,4],[13,3],[14,2],[15,1]]],
			["EF",
			encr_locs,
			encr_locs,
			[[2,13],[3,12],[4,11],[5,10],[6,9],[7,8],[8,7],[9,6],[10,5],[11,4],[12,3],[13,2],[14,1]]]
		]
		defe_locs = [
			["DF",
			[[13,13],[14,13],[12,12],[15,12],[13,12],[14,12],[11,11],[16,11],[12,11],[15,11],[13,11],[14,11]],
			[[0,13],[1,13],[1,12],[2,13],[2,12],[2,11],[3,13],[3,12],[4,13]],
			[[27,13],[26,13],[26,12],[25,13],[25,12],[25,11],[24,13],[24,12],[23,13]]],
			["FF",
			[[12,13],[15,13],[11,12],[16,12],[10,11],[17,11]],
			[[5,13],[4,12],[3,11]],
			[[22,13],[23,12],[24,11]]]
		]

		if self.mode == 1:
			for y in range(14,17):
				if len(game_map.filter_blocked_locations([[12,y],[13,y],[14,y],[15,y]])) == 0:
					if len(game_map.filter_blocked_locations([[26,14],[27,14]])) == 0:
						for defe in defe_locs:
							game_map.attempt_remove_multiple(defe[self.mode])
						self.mode = 2
					elif len(game_map.filter_blocked_locations([[0,14],[1,14]])) == 0:
						for defe in defe_locs:
							game_map.attempt_remove_multiple(defe[self.mode])
						for offe in offe_locs:
							game_map.attempt_remove_multiple(offe[self.mode])
						self.mode = 3
					gamelib.debug_write("mode:{}".format(self.mode))

		cores = game_map.get_resource("cores") - len(game_map.filter_blocked_locations(offe_locs[0][self.mode])) * game_map.type_cost(offe_locs[0][0])
		for defe in defe_locs:
			for loc in defe[self.mode]:
				if cores >= game_map.type_cost(defe[0]):
					if game_map.attempt_spawn(defe[0], loc):
						cores -= game_map.type_cost(defe[0])

		bits = game_map.get_resource("bits")
		if math.floor(game_map.bits_in_future()) - math.floor(bits) < 4:
			gamelib.debug_write("bits:{}".format(bits))

			for offe in offe_locs:
				game_map.attempt_spawn_multiple(offe[0], offe[self.mode])

			if self.mode == 3:
				spawn_loc = [14,0]
			else:
				spawn_loc = [13,0]

			while game_map.get_resource("bits") >= 1:
				game_map.attempt_spawn("EI", spawn_loc)
				game_map.attempt_spawn("SI", spawn_loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
