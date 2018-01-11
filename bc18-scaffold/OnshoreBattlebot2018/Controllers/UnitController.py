import battlecode as bc

from Entities import *

# Keeps a list of all friendly units (share with buildController - figure out which should store it)
# Loops over all units, running their "Run" methods one at a time
# Can prioritize robots by importance or any other activation order
# Responsible for putting robots back into the queue if a healer resets their cooldowns
class UnitController:
	def __init__(self, gameController, strategyController, pathfindingController):
		self.gameController = gameController
		self.strategyController = strategyController
		self.pathfindingController = pathfindingController

		self.robots = []
		self.structures = []
		self.missions = []
	
	def UpdateUnits(self):
		self.__DeleteKilledUnits()
		self.__AddUnregisteredUnits()
	
	# Removes robots and structures that are not found on the map any longer
	def __DeleteKilledUnits(self):
		pass

	# Creates robots and structures for all units that do not yet have them
	# Can occur when moving robots between planets or for the default starting worker
	# TODO need a more efficient way to check unit existence.  This is brute force
	def __AddUnregisteredUnits(self):
		friendlyUnits = self.gameController.my_units()
		if len(friendlyUnits) == 0:
			print("There are no units on the field. Nothing to add.")
			return

		print("{} units found to register".format(len(friendlyUnits)))
		#If there are no robots registered, just register them all
		if len(self.robots) == 0:
			print("No robots currently in the list.  Registering them all")
			for unit in self.gameController.my_units():
				self.__RegisterUnit(unit)
		else:
			print("Comparing existing robots against units")
			for unit in self.gameController.my_units():
				for friendlyUnit in self.robots:
					if friendlyUnit.unit.id == unit.id:
						print("Robot already registered. Updating")
						friendlyUnit.unit = unit
						break
				else:
					for friendlyUnit in self.structures:
						if friendlyUnit.unit.id == unit.id:
							print("Structure already registered. Updating")
							friendlyUnit.unit = unit
							break
					else:
						self.__RegisterUnit(unit)

	#TODO expand to use all unit types.
	# put rockets and factories into structures
	def __RegisterUnit(self, unit):
		if unit.unit_type == bc.UnitType.Worker:
			self.robots.append(Worker(self.gameController, self, self.pathfindingController, unit))
			
	#TODO figure out format of missions
	# must contain information on what the mission type is (enum)
	# which entities can pick up said mission
	# any information relevant to the mission.  Target Unit or location?
	def UpdateMissions(self):
		if len(self.missions) == 0:
			print("Adding 'walk randomly' to the mission queue")
			self.missions.append("Walk Randomly")

	#Allows other robots or controllers to add missions to the list
	def AddMission(self):
		pass

	#Pops the highest priority mission for the given unit off the queue and returns it
	def GetMission(self, unitType):
		if len(self.missions) > 0:
			print("Returning first mission to the worker")
			return self.missions.pop(0)
	
	# Add prioritization of turn order
	def RunUnits(self):
		print("Running all robots")
		for robot in self.robots:
			robot.run()
		
		print("Running all structures")
		for structure in self.structures:
			structure.run()