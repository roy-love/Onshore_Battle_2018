import random
import sys
import traceback

from .IRobot import IRobot

class Healer(IRobot):
	def __init__(self, gameController):
		self.gameController = gameController