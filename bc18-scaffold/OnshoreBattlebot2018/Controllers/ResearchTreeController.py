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
    """"This is the research tree controller"""
    def __init__(self, gameController, strategyController):
        self.game_controller = gameController
        self.strategy_controller = strategyController

        #hard coded research queue
        

    def is_rocket_researched(self):
        research_info = self.game_controller.research_info()
        level = research_info.get_level(bc.UnitType.Rocket)
        if level > 0:
            return True
        else:
            return False

    def update_queue(self):
        pass
        #if self.strategy_controller.macro_strategy == MacroStrategies.Default:
        #    if not self.game_controller.research_info().has_next_in_queue():
        #        self.add_research_to_queue(bc.UnitType.Worker)

    def add_research_to_queue(self, branch):
        branch_name = self.get_branch_name(branch)
        research_info = self.game_controller.research_info()
        level = research_info.get_level(branch)
        print("Added [{}] research level [{}].".format(branch_name, level))
        self.game_controller.queue_research(branch)

    def clear_research_queue(self):
        print("Research queue cleared.")
        self.game_controller.reset_research()

    def is_current_research_near_completion(self):
    # Returns a bool if the current number of rounds left for the current
    # research is less than or equal to a percentage.
    # rType: bool

        research_info = self.game_controller.research_info(self.game_controller)
        branch = research_info.queue.__getItem__(0)
        level = research_info.get_level(branch)
        current_level_total_turns = self.get_research_branch_turns(branch, level)
        if research_info.rounds_left(research_info) / current_level_total_turns <= .25:
            return True
        else:
            return False

    def get_research_branch_turns(self, branch, level):
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

    def get_branch_name(self, branch):
        """This gets the branch name"""
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
