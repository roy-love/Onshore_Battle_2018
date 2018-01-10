import random
import sys
import traceback

from IRobot import IRobot

class Rocket:
	def __init__(self, gameController):
		self.gameController = gameController