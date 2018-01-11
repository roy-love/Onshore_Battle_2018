import random
import sys
import traceback

from .IRobot import IRobot

class Worker(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, robotId):
		super(Worker, self).__init__(gameController, robotId, self.gameController.unit(robotId).unit_type)

	def run(self):
		pass