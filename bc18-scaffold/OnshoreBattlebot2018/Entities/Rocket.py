import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IStructure import IStructure

class Rocket(IStructure):
    """This is the rocket"""
    def __init__(self, gameController, unitController, unit):
        super(Rocket, self).__init__(gameController, unitController, unit)

        self.passengerId = None
        self.expectedLoad = 1

    def run(self):
        
        if self.mission.action == Missions.Idle:
            pass # do nothing
        elif self.mission.action == Missions.LoadRocket:
            if try_load(self.mission.info.unitId):
                print("Rocket {} loaded with unit id {}".format(self.unit.id,self.mission.info.unitId))
                if len(self.unit.structure_garrison()) == self.unit.structure_max_capacity():
                    print("Rocket max capacity reached.")
                elif len(self.unit.structure_garrision()) == self.expectedLoad)
                    print("Rocket expected capacity reached.")
                else:
                    currentLoad = len(self.unit.structure_garrision())
                    maxCapacity = self.unit.structure_max_capacity()
                    print("Rocket load success. Capacity: {}/{}".format(currentLoad,maxCapacity))
            else:
                print("Unable to load rocket {}".format(self.unit.id))
        elif self.mission.action == Missions.UnloadRocket:
            if self.try_unload():
                print("")
        """This runs the rocket"""
        pass


    def try_load(self, target_robot_id):
        """Trys to load the rocket"""
        #TODO check heat of target unit is low enough
        if not self.game_controller.can_load(self.unit.id, target_robot_id):
            print("Rocket [{}] cannot load the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.load(self.unit.id, target_robot_id)
        self.passengerId = target_robot_id
        
        return True

    def try_unload(self, target_robot_id):
        """Trys to unload the rocket"""
        #TODO check heat of target unit is low enough
        if not self.game_controller.can_unload(self.unit.id, target_robot_id):
            print("Rocket [{}] cannot unload the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.unload(self.unit.id, passengerId)
        return True

    def try_launch(self, destination):
        """Trys to launch the rocket"""
        if not self.game_controller.can_launch_rocket(self.unit.id, destination):
            print("Rocket [{}] could not launch to destination [{}]".format(\
            self.unit.id, destination))
            return False

        self.game_controller.launch_rocket(self.unit.id, destination)
        return True
