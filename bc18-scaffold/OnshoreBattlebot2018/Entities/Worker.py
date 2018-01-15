import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot


class Worker(IRobot):
    """This is the Worker robot"""
    # change init definition to include any controllers needed in the instructor as we need them
    # For example:  it will eventually need to access the Targeting and Pathfinding controllers
    def __init__(self, gameController, unitController, \
    pathfindingController, missionController, unit):
        super().__init__(gameController, unitController, \
        pathfindingController, missionController, unit, bc.UnitType.Worker)

    #overrides IRobot run method
    def run(self):
        #print("Worker bot with id {} run() called.".format(self.unit.id))
        self.update_mission()

        if self.mission.action == Missions.Idle:
            self.idle()

        elif self.mission.action == Missions.RandomMovement:
            self.one_random_movement()

        elif self.mission.action == Missions.Mining:

            #TODO Determine what to do when mining
            if not self.perform_second_action and self.target_location is None:
                if self.path is None or len(self.path) == 0:
                    #print("Path is null.  Making a new one")
                    self.target_location = self.mission.info

                    #print("Wants to move from {},{} to {},{}".format(\
                    # self.unit.location.map_location().x, self.unit.location.map_location().y, \
                    # self.target_location.x, self.target_location.y))
                    self.update_path_to_target()

            if self.has_reached_destination():
                # harvest at the current map location: 0 = Center
                self.try_harvest(bc.Direction.Center)
                self.reset_mission()
            else:
                self.follow_path()

        elif self.mission.action == Missions.CreateBlueprint:
            # TODO Upgrade logic with better pathfinding
            #if not self.perform_second_action and self.target_location is None:
            #    if self.path == None or len(self.path) == 0:
                    #print("Build location path is null. Making a new one.")
            #        self.target_location = self.mission.info

                    #print("Wants to move from {},{} to {},{}".format(\
                    # self.unit.location.map_location().x, self.unit.location.map_location().y, \
                    # self.target_location.x, self.target_location.y))
            #        self.update_path_to_target()

            #if self.has_reached_destination():
            self.one_random_movement()
            direction = random.choice(list(bc.Direction))
            if self.try_blueprint(bc.UnitType.Factory, direction):
                print("Worker {} created blueprint for Factory.".format(self.unit.id))
            self.reset_mission()
            #else:
            #    self.FollowPath()

        elif self.mission.action == Missions.BuildFactory:
            if not self.perform_second_action and self.target_location is None:
                if self.path is None or len(self.path) == 0:
                    #print("Build location path is null. Making a new one.")

                    self.target_location = self.mission.info.mapLocation

                    #print("Wants to move from {},{} to {},{}".\
                    # format(self.unit.location.map_location().x, \
                    # self.unit.location.map_location().y, \
                    # self.target_location.x, self.target_location.y))
                    self.update_path_to_target()

            if not self.mission.info.unit.structure_is_built() and self.has_reached_destination():
                self.try_build(self.mission.info.unitId)

            if self.mission.info.unit.structure_is_built():
                self.reset_mission()
        #print("Worker with id {} method run FINISHED.".format(self.unit.id))

    def try_blueprint(self, unit_type, direction):
        """Trys a blueprint"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_blueprint(self.unit.id, unit_type, direction):
            print("Worker [{}] cannot blueprint [{}] in direction [{}]".\
            format(self.unit.id, unit_type, direction))
            return False

        result = self.game_controller.blueprint(self.unit.id, unit_type, direction)
        #print("BLUEPRINT_RESULT: {}".format(result))
        info = MissionInfo()
        info.mapLocation = self.unit.location.map_location()
        nearby = self.game_controller.sense_nearby_units(info.mapLocation, 2)
        for other in nearby:
            print(other.unit_type)
            if bc.UnitType.Factory == other.unit_type:
                #gc.build(unit.id, other.id)
                #print('built a factory!')
                info.unitId = other.id
                info.unit = other
        self.mission_controller.AddMission(Missions.BuildFactory, MissionTypes.Worker, info)
        return True

    def try_build(self, blueprint_id):
        """Trys to build"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_build(self.unit.id, blueprint_id):
            print("Worker [{}] cannot build blueprint [{}]".format(self.unit.id, blueprint_id))
            return False

        self.game_controller.build(self.unit.id, blueprint_id)
        return True

    def try_harvest(self, direction):
        """Trys to harvest"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_harvest(self.unit.id, direction):
            print("Worker [{}] cannot harvest in direction [{}]".format(self.unit.id, direction))
            return False

        self.game_controller.harvest(self.unit.id, direction)
        return True

    def try_repair(self, structure_id):
        """Trys to repair"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_repair(self.unit.id, structure_id):
            print("Worker [{}] cannot repair structure [{}]".format(self.unit.id, structure_id))
            return False

        self.game_controller.repair(self.unit.id, structure_id)
        return True

    def try_replication(self, direction):
        """Trys to replicate"""
        if not self.game_controller.can_replicate(self.unit.id, direction):
            print("Worker [{}] cannot replicate in direction [{}]".format(self.unit.id, direction))
            return False

        self.game_controller.replicate(self.unit.id, direction)
        return True
