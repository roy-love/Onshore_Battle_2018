import battlecode as bc
import random
import sys
import traceback

from Controllers import *
from Entities import *

class RunMars:
    """This is how we run Mars"""
    # Initialize controllers
    # Initialize all class variables
    # Only include code that should be initialized once at the beginning of the match
    def __init__(self, gameController):
        self.game_controller = gameController
        self.map_controller = MapController(gameController)
        self.enemy_tracking_controller = EnemyTrackingController(gameController)
        self.strategy_controller = StrategyController(gameController, \
        self.map_controller, self.enemy_tracking_controller)
        self.research_tree_controller = ResearchTreeController(gameController, \
        self.strategy_controller)
        self.build_controller = BuildController(gameController, self.map_controller, \
        self.strategy_controller)
        self.pathfinding_controller = PathfindingController(gameController, self.map_controller)
        self.mission_controller = MissionController(gameController, self.strategy_controller, \
        self.map_controller, self.research_tree_controller)
        self.unit_controller = UnitController(gameController, self.strategy_controller, \
        self.pathfinding_controller, self.mission_controller)
        self.targetting_controller = TargettingController(gameController, \
        self.map_controller, self.strategy_controller, self.unit_controller, self.enemy_tracking_controller)

        self.round = gameController.round()

    # Runs once per turn for this planet only
    def Run(self):
        """This  runs on Marce once per turn"""
        self.round = self.game_controller.round()
        if self.round == 1:
            print("First round on Earth.  Initializing map")
            self.map_controller.InitializeMarsMap()
        print("Do mars turn things here")
