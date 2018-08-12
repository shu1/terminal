import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()

	def process_config(self, config):
		self.config = config

	def step(self, game_map):
		wall = [[16,2],[11,2],[27,13],[0,13],[17,3],[10,3],[26,12],[1,12],[18,4],[9,4],[25,11],[2,11],[19,5],[8,5],[24,10],[3,10],[20,6],[7,6],[23,9],[4,9],[21,7],[6,7],[22,8],[5,8]]
		if game_map.turn_number == 0:
			game_map.attempt_spawn_multiple("FF", wall)
		game_map.attempt_spawn_multiple("DF", wall)
		game_map.attempt_spawn_multiple("DF", [[15,5],[12,5],[17,7],[10,7],[15,9],[12,9],[19,9],[8,9],[17,11],[10,11],[21,11],[6,11],[23,13],[4,13],[15,13],[12,13],[19,13],[8,13]])
		game_map.attempt_spawn_multiple("EF", [[15,11],[12,11],[19,11],[8,11],[17,13],[10,13],[21,13],[6,13],[17,9],[10,9],[15,7],[12,7]])
		spawn_location = random.choice([[12,1],[13,0],[14,0],[15,1]])
		while game_map.get_resource("bits") >= 1:
			game_map.attempt_spawn("EI", spawn_location)
			game_map.attempt_spawn("SI", spawn_location)
		game_map.send_messages()

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
