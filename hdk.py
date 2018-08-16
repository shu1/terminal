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

		if game_map.turn_number == 0:
			game_map.attempt_spawn_multiple("DF", [[3,13],[24,13],[7,13],[20,13],[11,13],[16,13]])

		wall_locs = [[24,13],[23,12],[22,11],[21,10],[20,9],[19,8],[18,7],[17,6],[16,5],[15,4],[14,3],[13,2],[12,1]]
		cores = game_map.get_resource("cores") - len(game_map.filter_blocked_locations(wall_locs)) * 1.5
		for loc in [[13,13],[14,13],[12,12],[15,12],[13,12],[14,12],[11,11],[16,11],[12,11],[15,11],[13,11],[14,11]]:
			if cores >= 6:
				if game_map.attempt_spawn("DF", loc):
					cores -= 6

		bits_now = game_map.get_resource("bits")
		if math.floor(game_map.bits_in_future()) - math.floor(bits_now) < 2:
			gamelib.debug_write("attack bits:{}".format(bits_now))
			game_map.attempt_spawn_multiple("FF", wall_locs)
			game_map.attempt_spawn_multiple("EF", [[25,13],[24,12],[23,11],[22,10],[21,9],[20,8],[19,7],[18,6],[17,5],[16,4],[15,3],[14,2],[13,1]])
			spawn_loc = [13,0]
			while game_map.get_resource("bits") >= 1:
				game_map.attempt_spawn("EI", spawn_loc)
				game_map.attempt_spawn("SI", spawn_loc)

		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
