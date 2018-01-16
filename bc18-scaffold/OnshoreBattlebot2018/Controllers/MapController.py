"""This is our Map Controller"""
import random
import sys
import traceback
import battlecode as bc

# Reads the Earth and Mars maps at the beginning of the game (time intensive)
# Store the two grids in a readable format
# Provides read and write access for other controllers to easily utilize
# May be responsible for keeping track of comets
class MapController:

    """This is the Map Controller"""
    def __init__(self, gameController):
        self.game_controller = gameController
        self.map = {}
        #access properties of earthMap like this self.earth_map[3][5]['isPassable']
        #which will access the isPassable bool for map location x = 3 y = 5
        self.earth_map = []

      # TODO have this function read the earth map from the api
      # store it into a location that's easy to read, sort, or search
    def initialize_earth_map(self):
        """This initializes the Earth's Map"""
        try:
            print("Initialize map here")
            self.map = self.game_controller.starting_map(bc.Planet.Earth)
            print(self.map.width)
            print(self.map.height)
            self.earth_map = []
            for map_x in range(self.map.height):
                self.earth_map.append([])
                for map_y in range(self.map.width):
                    map_loc = bc.MapLocation(bc.Planet.Earth, map_x, map_y)
                    self.earth_map[map_x].append({"x": map_x, "y": map_y, \
                    "hash": self.hash_coordanates(map_x, map_y), "isPassable": \
                    self.map.is_passable_terrain_at(map_loc), "karboniteCount": \
                    self.map.initial_karbonite_at(map_loc)})
            print(self.map.planet)
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            traceback.print_exc()

    def hash_coordanates(self, in_x, in_y):
        """These are the Hash Coordanates"""
        hash = 23
        hash = 29 * hash + in_x
        hash = 29 * hash + in_y
        return hash

    def get_node(self, map_x, map_y):
        """This gets the node"""
        if (map_x <= self.map.width - 1 and map_y <= self.map.height - 1 and map_x > -1 and map_y > -1):
            node = self.earth_map[map_x][map_y]
            return node
        return None
