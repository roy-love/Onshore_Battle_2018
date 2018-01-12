import random
import sys
import traceback

from .IRobot import IRobot

class Knight(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, unit):
		super().__init__(gameController, unitController, pathfindingController, unit)
		self.mission = None
		self.targetLocation = None
		self.path = None


	def run(self):
		self.__GetMission()

		if self.mission == "Walk Randomly":
			print("walking randomly")
			#TODO rework this section to include pathfinding as well as path traversal.
				

	def __GetMission(self):
		if self.mission == None:
			print("Knight has no mission.")
			self.mission = self.unitController.GetMission(self.unit.unit_type)
			print("New mission is ({})".format(self.mission))
		else:
			print("Current mission is ({})".format(self.mission))

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