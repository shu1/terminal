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
		self.mode = 1	# hounddog

		wall_locs = [[13-i,i] for i in range(13,1,-1)]
		self.defe = [[
			"DF",
			[[11,11],[16,11],[12,11],[15,11],[13,11],[14,11],[12,12],[15,12],[13,12],[14,12],[13,13],[14,13]],
			[[24,13],[23,13],[23,12],[22,13],[22,12],[22,11],[21,13],[21,12],[20,13]],
			[[0,13],[1,13],[1,12],[2,13],[2,12],[2,11],[3,13],[3,12],[4,13]],
			[[27,13],[26,13],[26,12],[25,13],[25,12],[25,11],[24,13],[24,12],[23,13]]
		],[
			"FF",
			[[10,11],[17,11],[11,12],[16,12],[12,13],[15,13]],
			[[19,13],[20,12],[21,11]],
			[[5,13],[4,12],[3,11]],
			[[22,13],[23,12],[24,11]]
		],[
			"FF",
			wall_locs,
			wall_locs,
			[],
			[]
		]]

		filt_locs = [[11+i,i] for i in range(13,0,-1)]
		encr_locs = [[12+i,i] for i in range(13,0,-1)]
		self.offe = [[
			"FF",
			filt_locs,
			filt_locs,
			filt_locs,
			[[16-i,i] for i in range(13,0,-1)]
		],[
			"EF",
			encr_locs,
			encr_locs,
			encr_locs,
			[[15-i,i] for i in range(13,0,-1)]
		]]

	def step(self, game_map):
		if game_map.turn_number == 0:
			game_map.attempt_spawn_multiple("DF", [[3,13],[24,13],[7,9],[20,9],[11,11],[16,11]])
		else:
			offset = 0
			if self.mode == 1:
				if len(game_map.filter_blocked_locations(game_map.get_edge_locations("top_left") + game_map.get_edge_locations("top_right"))) <= 4:
					for defe in self.defe:
						game_map.attempt_remove_multiple(defe[self.mode])
					self.mode = 2 # specter
					gamelib.debug_write("MODE:{}".format(self.mode))
				else:
					x = 14
					paths = [14,13,15,12,16,11,17,10,18,9,19,8,20,7,21,6,22,5,23,4,24,3,25,2,26,1,27,0]
					for i in [14,13,15,12,16,11,17,10,18,9,19,8,20,7,21,6,22,5,23,4,24,3,25,2,26,1,27,0]:
						j = 13 if i < 14 else 14
						paths[i] = len(game_map.find_path_to_location([i,13], [j,27], 0)[0])
						if paths[i] < paths[x]:
							x = i

					xs = []
					for i in range(0,28):
						if paths[i] == paths[x]:
							xs.append(i)
					gamelib.debug_write("{} {} {}".format(paths, paths[x], xs))

					if x < 5:
						for defe in self.defe:
							game_map.attempt_remove_multiple(defe[self.mode])
						self.mode = 3	# starfish
						gamelib.debug_write("MODE:{}".format(self.mode))
					elif x > 22:
						for defe in self.defe:
							game_map.attempt_remove_multiple(defe[self.mode])
						for offe in self.offe:
							game_map.attempt_remove_multiple(offe[self.mode])
						game_map.attempt_remove_multiple([[2,12],[3,12],[3,11],[4,11]])
						self.mode = 4	# champ
						gamelib.debug_write("MODE:{}".format(self.mode))
					else:
						offset = x - 14
						if offset > 5:
							offset = 5

			cores = game_map.get_resource("cores") - len(game_map.filter_blocked_locations(self.offe[0][self.mode])) * 1.5
			for i, defe in enumerate(self.defe):
				for loc in defe[self.mode]:
					if cores >= game_map.type_cost(defe[0]):
						if self.mode == 1 and i < 2:	# floating island
							loc = [loc[0] + offset, loc[1]]
						if game_map.attempt_spawn(defe[0], loc):
							cores -= game_map.type_cost(defe[0])

		if math.floor(game_map.bits_in_future()) - math.floor(game_map.get_resource("bits")) < 4:
			gamelib.debug_write("{} health:{} enemy:{}".format(game_map.turn_number, int(game_map.my_integrity), int(game_map.enemy_integrity)))

			if game_map.turn_number > 0:
				for offe in self.offe:
					game_map.attempt_spawn_multiple(offe[0], offe[self.mode])

			loc = [14,0] if self.mode == 4 else [13,0]
			while game_map.get_resource("bits") >= 1:
				game_map.attempt_spawn("EI", loc)
				game_map.attempt_spawn("SI", loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
