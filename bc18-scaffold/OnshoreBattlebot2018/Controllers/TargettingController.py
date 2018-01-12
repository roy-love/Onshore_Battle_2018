import random
import sys
import traceback

# Given a robot, a target type to prioritize, and an enemy list
# Determines the highest priority location to move towards
# This can apply to workers looking for a build location, healers looking for allies, or rangers looking for targets
# To start, focus on simply returning the closest or most valuable target
class TargettingController:
    def __init__(self, gameController, mapController, strategyController):
        self.game_controller = gameController
        self.map_controller = mapController
        self.strategy_controller = strategyController
