import random
import battlecode as bc
from .IRobot import IRobot

class Mage(IRobot):

	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Mage)

	def run(self):
		super(Mage,self).UpdateMission()

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
		return super(Mage, self).run()

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Mage [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		return True

	def tryBlink(self, destination):
		#TODO check has research

		#Check cooldown of Blink ability
		if not self.gameController.is_blink_ready(self.unit.id):
			print("Blink is not ready for Mage [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_blink(self.unit.id, destination):
			print("Mage [{}] cannot blink to the target location")
			return False

		self.gameController.blink(self.unit.id, destination)
		return True