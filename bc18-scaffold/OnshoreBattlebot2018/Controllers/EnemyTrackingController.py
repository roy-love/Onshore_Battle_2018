import random
import sys
import traceback

# Keeps track of enemy units and structures
# Will be frequently updated by robots based upon vision range
# Nothing in this class is 100% known as the enemy is constantly moving
class EnemyTrackingController:

    """This is the Enemy Tracking Controller"""

    def __init__(self, gameController):
        self.game_controller = gameController
