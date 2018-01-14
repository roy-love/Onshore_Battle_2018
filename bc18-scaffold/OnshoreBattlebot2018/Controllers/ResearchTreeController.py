import random
import sys
import traceback

import battlecode as bc
from .StrategyController import *

# Keeps track of the current tech tree progress
# Uses the strategy selected to determine the build order
# TODO Determine which planet is in charge of the research tree and how to pass to Mars with the 50 turn delay
# Items can be added to the queue individually
# Items can only be removed from the queue all at once, cancelling any progress
class ResearchTreeController:
	def __init__(self, gameController, strategyController):
		self.gameController = gameController
		self.strategyController = strategyController

	def UpdateQueue(self):
		if self.strategyController.macroStrategy == MacroStrategies.Default:
			if not self.gameController.research_info().has_next_in_queue():
				self.AddResearchToQueue(bc.UnitType.Worker)

	def AddResearchToQueue(self, branch):
		branchName = self.GetBranchName(branch)
		researchInfo = self.gameController.research_info()
		level = researchInfo.get_level(branch)
		print("Added [{}] research level [{}].".format(branchName,level))
		self.gameController.queue_research(branch)

	def ClearResearchQueue(self):
		print("Research queue cleared.")
		self.gameController.reset_research()

	def IsCurrentResearchNearCompletion(self):
	# Returns a bool if the current number of rounds left for the current
	# research is less than or equal to a percentage.
	# rType: bool
	    
	    researchInfo = self.gameController.research_info(self.gameController)
	    branch = researchInfo.queue.__getItem__(0)
	    level = researchInfo.get_level(branch)
	    currentLevelTotalTurns = self.GetResearchBranchTurns(branch,level)
	    if researchInfo.rounds_left(researchInfo) / currentLevelTotalTurns <= .25:
		    return True
	    else:
		    return False

	def GetResearchBranchTurns(self,branch,level):
	    if branch == 0: # Worker
		    if level == 1:
			    return 25
		    elif level == 2:
			    return 75
		    elif level == 3:
			    return 75
		    elif level == 4:
			    return 75
		    else:
			    return 0
	    if branch == 1: # Knight
		    if level == 1:
			    return 25
		    elif level == 2:
			    return 75
		    elif level == 3:
			    return 150
		    else:
			    return 0
	    if branch == 2: # Ranger
		    if level == 1:
			    return 25
		    elif level == 2:
			    return 100
		    elif level == 3:
			    return 200
		    else:
			    return 0
	    if branch == 3: # Mage
		    if level == 1:
			    return 25
		    elif level == 2:
			    return 75
		    elif level == 3:
			    return 100
		    elif level == 4:
			    return 200
		    else:
			    return 0
	    if branch == 4: # Healer
		    if level == 1:
			    return 25
		    elif level == 2:
			    return 100
		    elif level == 3:
			    return 200
		    else:
			    return 0
	    if branch == 6: # Rocket
		    if level == 1:
			    return 100
		    elif level == 2:
			    return 100
		    elif level == 3:
			    return 100
		    else:
			    return 0
	    else:
		    return 0

	def GetBranchName(self,branch):
	    if branch == 0:
		    return "Worker"
	    elif branch == 1:
		    return "Knight"
	    elif branch == 2:
		    return "Ranger"
	    elif branch == 3:
		    return "Mage"
	    elif branch == 4:
		    return "Healer"
	    elif branch == 6:
		    return "Rocket"
	    else:
		    return "Not a research Branch"
