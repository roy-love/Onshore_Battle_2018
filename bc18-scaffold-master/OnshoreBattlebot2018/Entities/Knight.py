import random
import sys
import traceback

from IRobot import IRobot

class Knight(IRobot):
	def __init__(self, gameController):
		self.gameController = gameController