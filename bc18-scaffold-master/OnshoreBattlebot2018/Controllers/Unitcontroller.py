import battlecode as bc
import random
import sys
import traceback

# Keeps a list of all friendly units (share with buildController - figure out which should store it)
# Loops over all units, running their "Run" methods one at a time
# Can prioritize robots by importance or any other activation order
# Responsible for putting robots back into the queue if a healer resets their cooldowns
class UnitController:
	def __init__(self, gameController, strategyController):
      self.gameController = gameController
	  self.strategyController = strategyController