import random
from .IRobot import IRobot

class Mage(IRobot):

	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Mage, self).__init__(gameController, robotId, self.gameController.unit(robotId).unit_type)

	def run(self):
		pass

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.robotId, targetRobotId):
			print("Mage [{}] cannot attack the target [{}]".format(self.robotId, targetRobotId))
			return False
		
		self.gameController.attack(self.robotId, targetRobotId)
		return True

	def tryBlink(self, destination):
		#TODO check has research
		#TODO check destination on map
		#TODO check destination in range
		#TODO check destination visible
		#TODO check location is empty

		#Check cooldown of Blink ability
		if not self.gameController.is_blink_ready(self.robotId):
			print("Blink is not ready for Mage [{}]".format(self.robotId))
			return False

		self.gameController.blink(self.robotId, destination)
		return True