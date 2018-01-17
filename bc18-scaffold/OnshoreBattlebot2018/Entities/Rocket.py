import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IStructure import IStructure

class Rocket(IStructure):
    """This is the rocket"""
    def __init__(self, gameController, unitController, unit,missionController):
        super(Rocket, self).__init__(gameController, unitController, unit,missionController)

        self.passengerId = None
        self.expectedLoad = 1
        self.rocketIsFull = False
        self.rocketLauchRound = 0

    def run(self):
        team = self.game_controller.team()
        robots = self.game_controller.sense_nearby_units_by_team(self.unit.location.map_location,5,team)
        for robot in robots:
            if try_load(robot.id):
                print("Rocket {} loaded robot {}.".format(self.unit.id,robot.id))

        if not self.mission is None:
            
            if self.mission.action == Missions.Idle:
                pass # do nothing
            elif self.mission.action == Missions.LoadRocket:
                if try_load(self.mission.info.unitId):
                    print("Rocket {} loaded with unit id {}".format(self.unit.id,self.mission.info.unitId))
                    if len(self.unit.structure_garrison()) == self.unit.structure_max_capacity():
                        print("Rocket max capacity reached. Forcing rocket lauch.")
                        self.ForceLauch()
                    # elif len(self.unit.structure_garrision()) == self.expectedLoad):
                    #    print("Rocket expected capacity reached.")
                    else:
                        currentLoad = len(self.unit.structure_garrison())
                        maxCapacity = self.unit.structure_max_capacity()
                        print("Rocket load success. Capacity: {}/{}".format(currentLoad,maxCapacity))
                else:
                    print("Unable to load rocket {}".format(self.unit.id))
            elif self.mission.action == Missions.UnloadRocket:
                garrison = self.unit.structure_garrison()
                if self.try_unload(garrison[0]):
                    # print("Rocket {} unloaded unit with id {}".format(self.unit.id,self.mission.info.unitId))
                    currentLoad = len(garrison)
                    if currentLoad > 0:
                        currentLoad = len(garrison)
                        maxCapacity = self.unit.structure_max_capacity()
                        print("Rocket {} unload success. Capacity: {}/{}".format(self.unit.id,currentLoad,maxCapacity))
                    else:
                        print("Rocket {} completely unloaded.".format(self.unit.id))
                        newMission = Mission()
                        newMission.action = Missions.Idle
                        self.mission.Idle
            elif self.mission.action == Missions.LaunchRocket:
                if try_launch(mission.info):
                    print("Rocket {} LAUNCHED!".format(self.unit.id))
            else:
                pass
                # Do nothing.
       

    def ForceLauch(self):
        newMission = Mission()
        newMission.action = Missions.LaunchRocket
        newMission.info = bc.MapLocation(bc.Planet.Mars,0,0)
        # TODO enhance landing destination
        self.mission = newMission()

    def ForceUnload(self):
        newMission = Mission()
        newMission.action = Missions.UnloadRocket
        self.mission = newMission()

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

        self.game_controller.unload(self.unit.id, target_robot_id)
        return True

    def try_launch(self, destination):
        """Trys to launch the rocket"""
        if not self.game_controller.can_launch_rocket(self.unit.id, destination):
            print("Rocket [{}] could not launch to destination [{}]".format(\
            self.unit.id, destination))
            return False

        self.game_controller.launch_rocket(self.unit.id, destination)
        return True
