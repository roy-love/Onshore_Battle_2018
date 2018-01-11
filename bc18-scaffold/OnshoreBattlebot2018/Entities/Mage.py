import random
from .IRobot import IRobot

class Mage(IRobot):

	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Mage, self).__init__(gameController, robotId)

	def run(self):
		pass

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