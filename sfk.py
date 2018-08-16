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

	def step(self, game_map):
		gamelib.debug_write("turn:{} health:{}".format(game_map.turn_number, int(game_map.my_integrity)))

		wall_locs = [[25,13],[24,12],[23,11],[22,10],[21,9],[20,8],[19,7],[18,6],[17,5],[16,4],[15,3],[14,2],[13,1]]
		cores = game_map.get_resource("cores") - len(game_map.filter_blocked_locations(wall_locs)) * 1.5
		for loc in [[0,13],[1,13],[2,13],[3,13],[4,13],[1,12],[2,12],[3,12],[2,11],[5,13],[6,13]]:
			if cores >= 6:
				if game_map.attempt_spawn("DF", loc):
					cores -= 6

		bits_now = game_map.get_resource("bits")
		if math.floor(game_map.bits_in_future()) - math.floor(bits_now) < 2:
			gamelib.debug_write("attack bits:{}".format(bits_now))
			game_map.attempt_spawn_multiple("FF", wall_locs)
			game_map.attempt_spawn_multiple("EF", [[24,13],[23,12],[22,11],[21,10],[20,9],[19,8],[18,7],[17,6],[16,5],[15,4],[14,3],[13,2],[12,1]])
			spawn_loc = [13,0]
			while game_map.get_resource("bits") >= 1:
				game_map.attempt_spawn("EI", spawn_loc)
				game_map.attempt_spawn("SI", spawn_loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
