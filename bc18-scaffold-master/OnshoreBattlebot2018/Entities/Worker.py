import battlecode as bc
import random
import sys
import traceback

class Worker(IRobot):
	def __init__(self, gameController):
		self.gameController = gameController