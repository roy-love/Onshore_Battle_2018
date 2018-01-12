import random
import sys
import traceback

from .IRobot import IRobot

class Worker(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, unit):
		super().__init__(gameController, unitController, pathfindingController, unit)

		self.mission = None
		self.targetLocation = None
		self.path = None

	#overrides IRobot run method
	def run(self):
		self.__GetMission()

		if self.mission == "Walk Randomly":
			print("walking randomly")
			if self.path == None or len(self.path) == 0:
				print("Path is null.  Making a new one")
				self.targetLocation = self.unit.location.map_location().clone()
				self.targetLocation.x += 3
				self.targetLocation.y += 2

				print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
				self.path = self.pathfindingController.FindPathTo(self.unit.location.map_location(), self.targetLocation)
			
			#TODO extract this bit to the IRobot super class, as it's common to all robots
			if len(self.path) > 0:
				direction = self.path[-1]
				print("Walking in direction {}".format(direction))
				if self.tryMove(direction):
					self.path.pop()
			else:
				print("destination reached")
				self.mission = None

	def __GetMission(self):
		if self.mission == None:
			print("Worker has no mission.")
			self.mission = self.unitController.GetMission(self.unit.unit_type)
			print("New mission is ({})".format(self.mission))
		else:
			print("Current mission is ({})".format(self.mission))

	def tryBlueprint(self, unitType, direction):
		if self.unit.worker_has_acted():
			print("Worker [{}] has already acted this turn".format(self.unit.id))
			return False

		if not self.gameController.can_blueprint(self.unit.id, unitType, direction):
			print("Worker [{}] cannot blueprint [{}] in direction [{}]".format(self.unit.id, unitType, direction))
			return False

		self.gameController.blueprint(self.unit.id, unitType, direction)
		return True

	def tryBuild(self, blueprintId):
		if self.unit.worker_has_acted():
			print("Worker [{}] has already acted this turn".format(self.unit.id))
			return False

		if not self.gameController.can_build(self.unit.id):
			print("Worker [{}] cannot build blueprint [{}]".format(self.unit.id, blueprintId))
			return False

		self.gameController.build(self.unit.id, blueprintId)
		return True

	def tryHarvest(self, direction):
		if self.unit.worker_has_acted():
			print("Worker [{}] has already acted this turn".format(self.unit.id))
			return False

		if not self.gameController.can_harvest(self.unit.id, direction):
			print("Worker [{}] cannot harvest in direction [{}]".format(self.unit.id, direction))
			return False

		self.gameController.harvest(self.unit.id, direction)
		return True

	def tryRepair(self, structureId):
		if self.unit.worker_has_acted():
			print("Worker [{}] has already acted this turn".format(self.unit.id))
			return False

		if not self.gameController.can_repair(self.unit.id, structureId):
			print("Worker [{}] cannot repair structure [{}]".format(self.unit.id, structureId))
			return False

		self.gameController.repair(self.unit.id, structureId)
		return True

	def tryReplication(self, direction):
		if not self.gameController.can_replicate(self.unit.id, direction):
			print("Worker [{}] cannot replicate in direction [{}]".format(self.unit.id, direction))
			return False

		self.gameController.replicate(self.unit.id, direction)
		return True