import battlecode as bc
import random
import sys
import traceback

class IStructure:
	def __init__(self, gameController, unitController, unit):
		self.gameController = gameController
		self.unitController = unitController
		self.unit = unit