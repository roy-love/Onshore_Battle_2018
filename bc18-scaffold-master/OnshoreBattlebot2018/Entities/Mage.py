import random
import sys
import traceback

from IRobot import IRobot

class Mage(IRobot):
	def __init__(self, gameController):
		self.gameController = gameController