import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import Missions
from .IRobot import IRobot


class Worker(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Worker)

		

	#overrides IRobot run method
	def run(self):
		super(Worker,self).UpdateMission()
		
		if self.mission == Missions.Idle:
			print("worker idle!")
			if  self.gameController.round >= self.missionStartRound + 10:
				self.mission = None

		if self.mission == Missions.RandomMovement:
			print("walking randomly")
			if self.path == None or len(self.path) == 0:
				print("Path is null.  Making a new one")
				self.targetLocation = self.unit.location.map_location().clone()
				self.targetLocation.x += 3
				self.targetLocation.y += 2

				print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
				self.UpdatePathToTarget()
			self.FollowPath()
		

		if self.mission == Missions.Mining:
			#TODO Determine what to do when mining
			pass

		if self.mission == Missions.BuildFactory:
			# TODO Upgrade logic with better pathfinding
			if self.path == None or len(self.path == 0):
				print("Build location path is null. Making a new one.")
				self.targetLocation = self.mission.location.clone()
			self.FollowPath()
			if self.mission == None:
				
				self.tryBlueprint(UnitType.Factory,bc.Direction.Left)
			

		return super(Worker, self).run()

	def tryBlueprint(self, unitType, direction):
		if self.unit.worker_has_acted():
			print("Worker [{}] has already acted this turn".format(self.unit.id))
			return False

		if not self.gameController.can_blueprint(self.unit.id, unitType, direction):
			print("Worker [{}] cannot blueprint [{}] in direction [{}]".format(self.unit.id, unitType, direction))
			return False

		self.gameController.blueprint(self.unit.id, unitType, direction)
		self.missionController.AddMission(Missions.BuildFactory)
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