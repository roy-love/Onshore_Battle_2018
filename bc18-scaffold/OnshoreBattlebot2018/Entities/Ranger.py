import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Ranger(IRobot):
	"""This is the Ranger robot"""
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, \
	pathfindingController, missionController, unit, mapController):
		super().__init__(gameController, unitController, \
		pathfindingController, missionController, unit, bc.UnitType.Ranger,mapController)

	def run(self):
		if not self.unit.location.is_in_garrison():
			self.update_mission()
			#First priority is to kill enemy troops
			if not self.mission is None:
				if self.mission.action == Missions.Idle:
					self.idle()

				elif self.mission.action == Missions.RandomMovement:
					self.one_random_movement()

				elif self.mission.action == Missions.DestroyTarget:
					self.destroy_target()

				#Attacks nearby units
				nearby = self.game_controller.sense_nearby_units(self.unit.location.map_location(), 50)
				for other in nearby:
					if other.team != self.game_controller.team() \
					and self.game_controller.is_attack_ready(self.unit.id) \
					and self.game_controller.can_attack(self.unit.id, other.id):
						print('Knight {} attacked a thing!'.format(self.unit.id))
						self.game_controller.attack(self.unit.id, other.id)
						break

	def try_attack(self, target_robot_id):
		"""Trys to attack"""
		# Checks to see if Ranger has enough heat to attack
		if not self.game_controller.is_attack_ready(self.unit.id):
			print("Ranger[{}] attack is not ready. Not enough heat".format(self.unit.id))
			return False

		if not self.game_controller.can_attack(self.unit.id, target_robot_id):
			print("Ranger [{}] cannot attack the target [{}]".format(self.unit.id, target_robot_id))
			return False

		self.game_controller.attack(self.unit.id, target_robot_id)
		return True

	def try_snipe(self, target_location):
		"""Trys to snipe"""
		# Checks that the Ranger has fully been researched so that it can now Snipe at enemy units
		level = bc.research_info.get_level(bc.UnitType.Ranger)
		if level != 3:
			return False

		if not self.game_controller.is_begin_snipe_ready(self.unit.id):
			print("Snipe is not ready for ranger [{}]".format(self.unit.id))
			return False

		if not self.game_controller.can_begin_snipe(self.unit.id, target_location):
			print("Ranger [{}] cannot snipe target location".format(self.unit.id))
			return False

		self.game_controller.begin_snipe(self.unit.id, target_location)
		return True

	# Sends Rangers to a defensive waypoint between our starting location and the enemy starting location
	def SetDefenderWaypoint(self):
		currentLocation = mapController.my_team_start
		enemyDirection = currentLocation.direction_to(mapController.enemy_team_start[0])
		target_location = currentLocation.clone()

		for i in range (0, 9):
			if enemyDirection == bc.Direction.North:
				target_location.y + 1
			elif enemyDirection == bc.Direction.Northeast:
				target_location.x + 1, target_location.y + 1
			elif enemyDirection == bc.Direction.East:
				target_location.x + 1
			elif  enemyDirection == bc.Direction.Southeast:
				target_location.y - 1, target_location.x +1
			elif enemyDirection == bc.Direction.South:
				target_location.y + 1
			elif enemyDirection == bc.Direction.Southwest:
				target_location.y - 1, target_location.x - 1
			elif enemyDirection == bc.Direction.West:
				target_location.x - 1
			elif enemyDirection == bc.Direction.Northwest:
				target_location.y + 1, target_location.x - 1
			print("Ranger adjusting target location to [{}]".format(self.target_location))

		# Randomizes an offest for x and y coordinations
		offset = random.randint(-5, 5)
		target_location.x = target_location.x + offset
		offset = random.randint(-5, 5)
		target_location.y = target_location.y + offset
		# Assisgns target location for our rangers to defend
		self.target_location = bc.MapLocation(bc.Planet.Earth, target_location.x, target_location.y)
		enemyDirection = direction_to(self.target_location)
		self.try_move(enemyDirection)