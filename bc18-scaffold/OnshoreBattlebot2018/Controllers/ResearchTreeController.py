import random
import sys
import traceback

# Keeps track of the current tech tree progress
# Uses the strategy selected to determine the build order
# TODO Determine which planet is in charge of the research tree and how to pass to Mars with the 50 turn delay
# Items can be added to the queue individually
# Items can only be removed from the queue all at once, cancelling any progress
class ResearchTreeController:
	def __init__(self, gameController, strategyController):
		self.gameController = gameController
		self.strategyController = strategyController