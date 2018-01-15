import battlecode as bc
import random
import sys
import traceback
#import numpy as np

from Entities import *
from Controllers.EnemyTrackingController import *

# Given a robot, a target type to prioritize, and an enemy list
# Determines the highest priority location to move towards
# This can apply to workers looking for a build location, healers looking for allies, or rangers looking for targets
# To start, focus on simply returning the closest or most valuable target
class TargettingController:
	def __init__(self, gameController, mapController, strategyController, unitController, enemyTrackingController):
		self.gameController = gameController
		self.mapController = mapController
		self.strategyController = strategyController
		self.unitController = unitController
		self.enemyTrackingController = enemyTrackingController
		self.enemyRobots = []
		self.enemyStructures = []
		self.ally = bc.team()
		self.roundLimit = 10

	# Updates units for whether they have died or if a unit needs to be added to registry
	def UpdateUnits(self):
		self._DeleteKilledUnits()
		self._AddUnregisteredEnemyUnits()
		self._RemoveRegisteredEnemyUnits()

	# Deletes units that have died
	def _DeleteKilledUnits(self):
		pass

	# Stores Robots and Structures for enemy units.
	# 
	def _AddUnregisteredEnemyUnits(self):
		if len(enemyUnits) == 0:
			print("There are no enemy units on the field, nothing to add")
			return
		#print("{} enemy units found to register".format(len(enemyUnits)))
		# If no enemy units have been registered, register them all
		if len(self.enemyRobots) != 0:
			for unit in enemyUnits:
				for enemyUnit in self.enemyRobots:
					if enemyUnit[0].id == unit.id:
						print("Enemy already registered. Updating timeout")
						enemyUnit[1] == currentRound
						break
				else:
					for enemyUnit in self.enemyStructures:
						if enemyUnit[0].id == unit.id:
							print("Structure already registered. Updating")
							enemyUnit = unit
							break
						else:
							self._RegisterUnit(unit)
		return

	# Removes an enemy robot from the Registry
	def _RemoveRegisteredEnemyUnits(self):
		if len(self.enemyRobots) == 0:
			print("There are no enemy units in the registry, nothing to remove")
			return

		print("{} enemy units found in the registry".format(len(enemyUnits)))
		for enemyUnit in self.enemyRobots:
			if currentRound - enemyUnit[1] >= self.roundLimit:
				print("Removing unit from registry")
				# TODO Clean-single index removal logic needs to be added here.
				pass

	# Prioritizes the enemy units for targeting.
	def __getNearbyPriority(self, unit):
		location = unit.location
		bestScore = 0
		score = 0
		nearbyUnits = bc.sense_nearby_units(location.map_location(), 2)
		for enemy in nearbyUnits:
			if enemy.team != self.ally:
				if enemy.unit_type == bc.UnitType.Rocket:
					score = 100
				elif enemy.unit_type == bc.UnitType.Knight or enemy.unit_type == bc.UnitType.Ranger or enemy.unit_type == UnitType.Mage:
					score = 80
				elif enemy.unit_type == bc.UnitType.Worker:
					score = 60
				else:
					score = 40
				if score > bestScore:
					bestScore = score
					bestRobot = enemy
			return bestRobot

	# Sets global prioritization of enemy units
	def __getGlobalPriorityEnemy():
		bestScore = 0
		score = 0
		for enemyUnit in self.enemyTrackingController.enemyUnits:
			if enemyUnit.team != self.ally:
				if enemyUnit.unit_type == bc.UnitType.Rocket:
					score = 100
				elif enemyUnit.unit_type == bc.UnitType.Knight or enemyUnit.unit_type == bc.UnitType.Ranger or enemyUnit.unit_type == bc.UnitType.Mage:
					score = 80
				elif enemyUnit.unit_type == bc.UnitType.Worker:
					score = 60
				else:
					score = 40
				if score > bestScore:
					bestScore = score
					bestRobot = enemyUnit
		return bestRobot


	def _RegisterUnit(self, unit):
		if unit.unit_type == bc.UnitType.Worker:
			self.enemyRobots.append(Worker(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Knight:
			self.enemyRobots.append(Knight(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Ranger:
			self.enemyRobots.append(Ranger(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Mage:
			self.enemyRobots.append(Mage(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Healer:
			self.enemyRobots.append(Healer(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Factory:
			self.enemyStructures.append(Factory(self.gameController, self, unit))
		elif unit.unit_type == bc.UnitType.Rocket:
			self.enemyStructures.append(Rocket(slef.gameController, self, unit))