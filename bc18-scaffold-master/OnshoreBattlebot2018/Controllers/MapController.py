import random
import sys
import traceback

# Reads the Earth and Mars maps at the beginning of the game (time intensive)
# Store the two grids in a readable format
# Provides read and write access for other controllers to easily utilize
# May be responsible for keeping track of comets
class MapController:
      def __init__(self, gameController):
            self.gameController = gameController