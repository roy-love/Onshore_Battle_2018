import battlecode as bc
import random
import sys
import traceback
from Controllers.MissionController import *

class IRobot:
    """This is the IRobot"""
    def __init__(self, gameController, unitController, \
    pathfindingController, missionController, unit, unitType, mapController):
        self.game_controller = gameController
        self.unit_controller = unitController
        self.pathfinding_controller = pathfindingController
        self.mission_controller = missionController
        self.map_controller = mapController

        #Reference to the BattleCode unit object that the server side code tracks
        self.unit = unit
        self.unit_type = unitType

        #Current mission dictates the robot's actions for the turn
        self.mission = None

        #Location that the robot will move to, regardless of what the mission type is
        self.target_location = None

        #List of directions to reach the target location
        self.path = None

        #Round that the current mission started on.
        self.mission_start_round = 0

        #To allow for Missions that have a secondary action
        self.perform_second_action = False

        #last position
        self.lastPosition = None
        
        self.directions = list(bc.Direction)

    #Actions that will be run at the end of every robot's turn
    def run(self):
        """This runs actions at the end of the turn"""
        pass

    def update_mission(self):
        """This updates the mission"""
        if self.mission is None:
            self.mission = self.mission_controller.get_mission(self.unit_type)
            self.mission_start_round = self.game_controller.round()
            self.target_location = None
            if not self.mission.action == Missions.Mining:
                print("Robot with id {} obtaining new mission {}".\
                format(self.unit.id, self.mission.action))

    def reset_mission(self):
        """This resets the mission"""
        self.perform_second_action = False
        self.mission = None

    #TODO Check that the next direction is still possible.  If not, recalculate
    def update_path_to_target(self):
        """This updates path to target"""
        if not self.unit.location.is_in_garrison() and self.target_location is not None and (self.path is None or len(self.path) == 0):
            #print("Creating new path from {},{} to {},{}".format\
            #(self.unit.location.map_location().x, self.unit.location.map_location().y, \
            #self.target_location.x, self.target_location.y))
            self.path = self.pathfinding_controller.FindPathTo(\
            self.unit.location.map_location().planet, self.unit.location.map_location(), self.target_location)

    def follow_path(self):
        """Allows you to follow the path"""
        if not self.path is None:
            if len(self.path) > 0:
                direction = self.path[-1]
                #print("Walking in direction {}".format(direction))
                if not self.unit.location.is_in_garrison() and self.try_move(direction):
                    self.path.pop()
                else:
                    self.one_random_movement()
                    self.update_path_to_target()
            else:
                #print("Robot {} path length 0.".format(self.unit.id))
                pass
    def isStuck(self):
        if self.lastPosition is None:
            self.lastPosition = self.unit.location.map_location()
            return False

        currentLocation = self.unit.location.map_location()
        if self.lastPosition.x == currentLocation.x and \
        self.lastPosition.y == currentLocation.y:
            return True
        else:
            return False

    def has_reached_destination(self):
        """Shows if you have reached the destination"""
        if self.target_location is None:
            #print("Robot {} targetLocation is None.".format(self.unit.id))
            return False
        else:
            if self.unit.location.map_location().x == self.target_location.x and \
                self.unit.location.map_location().y == self.target_location.y:
                self.target_location = None
                self.perform_second_action = True
                #print("Robot with id {} has reached it's destination.".format(self.unit.id))
                return True
            else:
                #print("Robot with id {} still moving to destination.".format(self.unit.id))
                return False

    def try_move(self, direction):
        """Lets you try to move"""
        if not self.game_controller.is_move_ready(self.unit.id):
            #print("Move for Robot [{}] is not ready".format(self.unit.id))
            return False
        if not self.game_controller.can_move(self.unit.id, direction):
            print("Robot [{}] cannot move in direction {}".format(self.unit.id, direction))
            return False

        self.game_controller.move_robot(self.unit.id, direction)
        return True

    def try_attack(self, target_robot_id):
        """Lets you try to attack"""
        #TODO check heat is low enough
        if not self.game_controller.can_attack(self.unit.id, target_robot_id):
            print("Bot [{}] cannot attack the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.attack(self.unit.id, target_robot_id)
        print("Bot [{}] attacked the target [{}]".format(self.unit.id, target_robot_id))
        return True

    def self_destruct(self):
        "Robot [{}] self destructing".format(self.unit.id)
        self.game_controller.disintegrate_unit(self.unit.id)

# Default Missions
    def idle(self):
        """Checks if you are idle"""
        print("bot idle!")
        if  self.game_controller.round >= self.mission_start_round + 10:
            self.reset_mission()

    def one_random_movement(self):
        """Gives you one random movement"""
        #print("Robot [{}] moved randomly.".format(self.unit.id))
        direction = random.choice(list(bc.Direction))
        if self.game_controller.is_move_ready(self.unit.id) \
        and self.game_controller.can_move(self.unit.id, direction):
            self.game_controller.move_robot(self.unit.id, direction)
        self.map_location = None

    def random_movement(self):
        """Walks the robot randomly"""
        print("bot walking randomly")
        if self.target_location is None:
            if self.path is None or len(self.path) == 0:
                #print("Path is null.  Making a new one")
                self.target_location = self.unit.location.map_location().clone()
                x = random.randint(-5, 5)
                y = random.randint(-5, 5)
                self.target_location.x += x
                self.target_location.y += y

                #print("Wants to move from {},{} to {},{}".format(\
                # self.unit.location.map_location().x, self.unit.location.map_location().y,\
                #  self.target_location.x, self.target_location.y))
                self.update_path_to_target()

        self.follow_path()
        if self.has_reached_destination():
            self.reset_mission()

    def destroy_target(self):
        """Attempts to destroy the target"""
        if not self.perform_second_action and self.target_location is None:
            if self.path is None or len(self.path) == 0:
                #print("Path is null.  Making a new one")
                self.target_location = self.mission.info.mapLocation

                #print("Wants to move from {},{} to {},{}".format(\
                # self.unit.location.map_location().x,
                # self.unit.location.map_location().y, self.target_location.x, \
                # self.target_location.y))
                self.update_path_to_target()

        if self.has_reached_destination():
            # harvest at the current map location: 0 = Center
            self.try_attack(self.mission.info.unitId)
            self.reset_mission()
        else:
            self.follow_path()
