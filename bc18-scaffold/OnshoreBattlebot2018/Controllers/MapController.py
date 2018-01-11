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

      # TODO have this function read the earth map from the api
      # store it into a location that's easy to read, sort, or search
      def InitializeEarthMap(self):
            print("Initialize map here")