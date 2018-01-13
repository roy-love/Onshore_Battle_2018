import random
import sys
import traceback
import battlecode as bc
from .IRobot import IRobot

class Ranger(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Ranger)

	def run(self):
		super(Ranger,self).UpdateMission()

		if self.mission == "Walk Randomly":
			print("walking randomly")
			if self.path == None or len(self.path) == 0:
				print("Path is null.  Making a new one")
				self.targetLocation = self.unit.location.map_location().clone()
				self.targetLocation.x += 3
				self.targetLocation.y += 2

				print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
				self.UpdatePathToTarget()
				self.FollowPath()
		return super(Ranger, self).run()
		
	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Ranger [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		return True
	

	def trySnipe(self, targetLocation):
		#TODO check has research

		if not self.gameController.is_begin_snipe_ready(self.unit.id):
			print("Snipe is not ready for ranger [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_begin_snipe(self.unit.id, targetLocation):
			print("Ranger [{}] cannot snipe target location".format(self.unit.id))
			return False

		self.gameController.begin_snipe(self.unit.id, targetLocation)
		return True