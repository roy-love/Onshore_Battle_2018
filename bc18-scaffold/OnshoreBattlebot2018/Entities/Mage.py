import random
from .IRobot import IRobot

class Mage(IRobot):

	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		self.gameController = gameController
		self.robotId = robotId
		print("Mage [{}] created".format(self.robotId))

	def run(self):
		# Actions that the mage should perform each turn
		# Change method to accept whatever options are needed from other controllers to make its decisions
		print("Do mage turn things")
		
		direction = random.randint(0,8)
		print("Moving randomly in direction {}".format(direction))
		self.tryMove(direction)

		chance = random.randint(0,100)
		if chance == 0:
			print("Randomly self destructing    1% chance")
			self.selfDestruct()

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.robotId, targetRobotId):
			print("Mage [{}] cannot attack the target [{}]".format(self.robotId, targetRobotId))
			return False
		
		self.gameController.attack(self.robotId, targetRobotId)
		return True

	def tryMove(self, direction) :
		if not self.gameController.is_move_ready(self.robotId):
			print("Move for Mage [{}] is not ready".format(self.robotId))
			return False
		if not self.gameController.can_move(self.robotId, direction):
			print("Mage [{}] cannot move in direction {}".format(self.robotId, direction))
			return False
		
		self.gameController.move_robot(self.robotId, direction)
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
	
	def selfDestruct(self):
		"Mage [{}] self destructing".format(self.robotId)
		self.gameController.disintegrate_unit(self.robotId)