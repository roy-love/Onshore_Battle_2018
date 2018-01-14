import battlecode as bc

from Entities import *

# Keeps a list of all friendly units (share with buildController - figure out which should store it)
# Loops over all units, running their "Run" methods one at a time
# Can prioritize robots by importance or any other activation order
# Responsible for putting robots back into the queue if a healer resets their cooldowns
class UnitController:
	def __init__(self, gameController, strategyController, pathfindingController, missionController):
		self.gameController = gameController
		self.strategyController = strategyController
		self.pathfindingController = pathfindingController
		self.missionController = missionController

		self.robots = []
		self.structures = []
	
	def UpdateUnits(self):
		self.__DeleteKilledUnits()
		self.__AddUnregisteredUnits()
	
	# Removes robots and structures that are not found on the map any longer
	def __DeleteKilledUnits(self):
		print("Checking for dead robots that should be removed from list")
		if len(self.robots) == 0:
			print("Robot list empty.  Nothing to remove")
			return

		# Robots that still exist are re-added to the robot list
		# Any not in the list are removed then picked up by garbage collection later
		print("Current robots registered = {}".format(len(self.robots)))
		print("Robots alive = {}".format(len(self.gameController.my_units())))
		self.robots = [robot for robot in self.robots if any(unit.id == robot.unit.id for unit in self.gameController.my_units())]
		print("Current robots registered after removal = {}".format(len(self.robots)))

	# Creates robots and structures for all units that do not yet have them
	# Can occur when moving robots between planets or for the default starting worker
	# if a robot exists, update its unit binding to account for server side changes
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

	def __RegisterUnit(self, unit):
		if unit.unit_type == bc.UnitType.Healer:
			self.robots.append(Healer(self.gameController, self, self.pathfindingController, self.missionController, unit))
		elif unit.unit_type == bc.UnitType.Knight:
			self.robots.append(Knight(self.gameController, self, self.pathfindingController, self.missionController, unit))
		elif unit.unit_type == bc.UnitType.Mage:
			self.robots.append(Mage(self.gameController, self, self.pathfindingController, self.missionController, unit))
		elif unit.unit_type == bc.UnitType.Ranger:
			self.robots.append(Ranger(self.gameController, self, self.pathfindingController, self.missionController, unit))
		elif unit.unit_type == bc.UnitType.Worker:
			self.robots.append(Worker(self.gameController, self, self.pathfindingController, self.missionController, unit))
		
		elif unit.unit_type == bc.UnitType.Factory:
			self.structures.append(Factory(self.gameController, self, unit, self.missionController))
		elif unit.unit_type == bc.UnitType.Rocket:
			self.structures.append(Rocket(self.gameController, self, unit))
		else:
			print("ERROR - Attempting to register an unknown unit type [{}]".format(unit.unit_type))
	
	# Add prioritization of turn order
	def RunUnits(self):

		print("Running all structures")
		print("structures count: {}".format(len(self.structures)))
		for structure in self.structures:
			structure.run()
			
		print("Running all robots")
		print("robot count: {}".format(len(self.robots)))
		for robot in self.robots:
			robot.run()
		
		