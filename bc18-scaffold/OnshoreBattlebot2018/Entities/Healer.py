import random
import sys
import traceback

from .IRobot import IRobot


class Healer(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Healer, self).__init__(gameController, robotId)

	def run(self):
		pass

	def tryHeal(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_heal(self.unit.id, targetRobotId):
			print ("Healer [{}] cannot heal the target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.heal(self.unit.id, targetRobotId)
		return True

	def tryOvercharge(self, targetRobotId):
		#TODO check has research
		
		#Check cooldown of Overcharge ability
		if not self.gameController.is_overcharge_ready(self.unit.id):
			print("Overcharge is not ready for Healer [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_overcharge(self.unit.id, targetRobotId):
			print("Healer [{}] cannot Overcharge the target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.overcharge(self.unit.id, targetRobotId)
		return True
