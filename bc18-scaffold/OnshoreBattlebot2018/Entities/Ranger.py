import random
import sys
import traceback

from .IRobot import IRobot

class Ranger(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Ranger, self).__init__(gameController, robotId)

	def run(self):
		pass
		
	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.robotId, targetRobotId):
			print("Ranger [{}] cannot attack the target [{}]".format(self.unit.robotId, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.robotId, targetRobotId)
		return True
	

	def trySnipe(self, targetLocation):
		#TODO check has research

		if not self.gameController.is_begin_snipe_ready(self.unit.robotId):
			print("Snipe is not ready for ranger [{}]".format(self.unit.robotId))
			return False

		if not self.gameController.can_begin_snipe(self.unit.robotId, targetLocation):
			print("Ranger [{}] cannot snipe target location".format(self.unit.robotId))
			return False

		self.gameController.begin_snipe(self.unit.robotId, targetLocation)
		return True