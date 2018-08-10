import gamelib
import random
import math
from sys import maxsize

class AlgoStrategy(gamelib.AlgoCore):
	def __init__(self):
		super().__init__()
		random.seed()

	def process_config(self, config):
		gamelib.debug_write('shu config')
		self.config = config

	f1s = [[16,2],[11,2],[27,13],[0,13],[17,3],[10,3],[26,12],[1,12],[18,4],[9,4],[25,11],[2,11],[19,5],[8,5],[24,10],[3,10],[20,6],[7,6],[23,9],[4,9],[21,7],[6,7],[22,8],[5,8]]
	f2s = [[15,5],[12,5],[17,7],[10,7],[15,9],[12,9],[19,9],[8,9],[17,11],[10,11],[21,11],[6,11],[23,13],[4,13],[15,13],[12,13],[19,13],[8,13]]
	f3s = [[14,3],[13,3],[15,7],[12,7],[17,9],[10,9],[15,11],[12,11],[19,11],[8,11],[17,13],[10,13],[21,13],[6,13]]
	def step(self, game_map):
		gamelib.debug_write('shu turn {}'.format(game_map.turn_number))
		if game_map.turn_number == 0:
			game_map.attempt_spawn_multiple("FF", AlgoStrategy.f1s)
		game_map.attempt_spawn_multiple("DF", AlgoStrategy.f1s)
		game_map.attempt_spawn_multiple("DF", AlgoStrategy.f2s)
		game_map.attempt_spawn_multiple("EF", AlgoStrategy.f3s)
		self.deploy_attackers(game_map)
		game_map.send_messages()

	def deploy_attackers(self, game_map):
		#Get some variebles we will use
		starting_bits = game_map.get_resource('bits')
		bits_to_spend = starting_bits
		enemy_bits = game_map.get_resource('bits', 1)
		current_health = game_map.my_integrity
		enemy_health = game_map.enemy_integrity
		friendly_edges = game_map.get_edge_locations("bottom_left") + game_map.get_edge_locations("bottom_right")
		deploy_locations = game_map.filter_blocked_locations(friendly_edges)

		#While we still want to spend more bits, deploy a random information unit
		while bits_to_spend >= 1 and len(deploy_locations) > 0:
			ping_value = 1
			scrambler_value = 1
			emp_value = 1

			#Stop if values were set below zero
			if ping_value + scrambler_value + emp_value < 1:
				break

			#Choose a random deploy location
			deploy_index = random.randint(0, len(deploy_locations) - 1)
			deploy_location = deploy_locations[deploy_index]

			#Adjust weights slightly based on game state
			if enemy_health <= 5:
				ping_value *= 2

			if enemy_bits > starting_bits or current_health <= 5:
				scrambler_value *= 2
			if bits_to_spend < 3:
				emp_value = 0

			#Choose a random unit based on weights, higher weights are more likely to be chosen
			total_value = ping_value + scrambler_value + emp_value
			choice = random.randint(1, total_value)

			if choice <= ping_value:
				bits_to_spend -= 1
				unit_to_spawn = "PI"
			elif choice <= ping_value + scrambler_value:
				bits_to_spend -= 1
				unit_to_spawn = "SI"
			else:
				bits_to_spend -= 3
				unit_to_spawn = "EI"

			game_map.attempt_spawn(unit_to_spawn, deploy_location)

if __name__ == "__main__":
	algo = AlgoStrategy()
	algo.start()
