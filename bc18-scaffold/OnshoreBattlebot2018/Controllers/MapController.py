import random
import sys
import traceback
import json
import battlecode as bc

# Reads the Earth and Mars maps at the beginning of the game (time intensive)
# Store the two grids in a readable format
# Provides read and write access for other controllers to easily utilize
# May be responsible for keeping track of comets
class MapController:
      def __init__(self, gameController):
            self.gameController = gameController
            self.map = {}
            #access properties of earthMap like this self.earthMap[3][5]['isPassable']
            #which will access the isPassable bool for map location x = 3 y = 5
            self.earthMap = []

      # TODO have this function read the earth map from the api
      # store it into a location that's easy to read, sort, or search
      def InitializeEarthMap(self):
            try:
                  print("Initialize map here")
                  self.map = self.gameController.starting_map(bc.Planet.Earth)
                  print(self.map.width)
                  print(self.map.height)
                  self.earthMap = []
                  for mapX in range(self.map.height):
                        self.earthMap.append([])
                        earthMapPart = []
                        for mapY in range(self.map.width):
                              mapLoc = bc.MapLocation(bc.Planet.Earth,mapX, mapY)
                              self.earthMap[mapX].append({"x": mapX, "y": mapY, "isPassable": self.map.is_passable_terrain_at(mapLoc), "karboniteCount": self.map.initial_karbonite_at(mapLoc)})
                  print(self.map.planet)
            except Exception as e:
                  print('Error:', e)
                  # use this to show where the error was
                  traceback.print_exc()

      def hashCoordanates(self, inX, inY):
            hash = 23;
            hash = 29 * hash + inX;
            hash = 29 * hash + inY;
            return hash
