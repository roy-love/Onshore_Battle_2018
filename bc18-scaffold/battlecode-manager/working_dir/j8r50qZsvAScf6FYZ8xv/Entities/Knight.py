import random
import sys
import traceback
import battlecode as bc
from .IRobot import IRobot

class Knight(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Knight)
		self.mission = None
		self.targetLocation = None
		self.path = None


	def run(self):
		super(Knight,self).UpdateMission()

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
		if self.mission == "DestroyTarget":
			print("DestroyTarget")
			#TODO implement move and destroy	
		return super(Knight, self).run()

	def IsEnemySighted(self):
		#TODO determine if this unit is able to see an enemy.
		#TODO refactor code to IRobot so that all robots can sight enemies.
		pass

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Knight [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		return True
	

	def tryJavelin(self, targetRobotId):
		#TODO check has research

		if not self.gameController.is_javelin_ready(self.unit.id):
			print("Javelin is not ready for knight [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_javelin(self.unit.id, targetRobotId):
			print("Knight [{}] cannot javelin target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.javelin(self.unit.id, targetRobotId)
		return True