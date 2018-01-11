import random
import sys
import traceback

from .IRobot import IRobot

class Knight(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Knight, self).__init__(gameController, robotId)

	def run(self):
		pass

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.robotId, targetRobotId):
			print("Knight [{}] cannot attack the target [{}]".format(self.unit.robotId, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.robotId, targetRobotId)
		return True
	

	def tryJavelin(self, targetRobotId):
		#TODO check has research

		if not self.gameController.is_javelin_ready(self.unit.robotId):
			print("Javelin is not ready for knight [{}]".format(self.unit.robotId))
			return False

		if not self.gameController.can_javelin(self.unit.robotId, targetRobotId):
			print("Knight [{}] cannot javelin target [{}]".format(self.unit.robotId, targetRobotId))
			return False

		self.gameController.javelin(self.unit.robotId, targetRobotId)
		return True