import random
import sys
import traceback

from .IStructure import IStructure

class Rocket(IStructure):
	def __init__(self, gameController, unitController, pathfindingController, unit):
		super(Rocket, self).__init__(gameController, unitController, pathfindingController, unit)

	def run(self):
		pass

	def tryLoad(self, targetRobotId):
		#TODO check heat of target unit is low enough
		if not self.gameController.can_load(self.unit.id, targetRobotId):
			print ("Rocket [{}] cannot load the target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.load(self.unit.id, targetRobotId)
		return True

	def tryUnload(self, targetRobotId):
		#TODO check heat of target unit is low enough
		if not self.gameController.can_unload(self.unit.id, targetRobotId):
			print ("Rocket [{}] cannot unload the target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.unload(self.unit.id, targetRobotId)
		return True

	def tryLaunch(self, destination):
		if not self.gameController.can_launch_rocket(self.unit.id, destination):
			print ("Rocket [{}] could not launch to destination [{}]".format(self.unit.id, destination))
			return False

		self.gameController.launch_rocket(self.unit.id, destination)
		return True