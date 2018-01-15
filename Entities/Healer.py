import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Healer(IRobot):
    # change init definition to include any controllers needed in the instructor as we need them
    # For example:  it will eventually need to access the Targeting and Pathfinding controllers
    def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
        super().__init__(gameController, unitController, pathfindingController, missionController, unit, bc.UnitType.Healer)

    def run(self):
        self.update_mission()

        if not self.mission is None:
            if self.mission.action == Missions.Idle:
                self.idle()

            elif self.mission.action == Missions.RandomMovement:
                self.one_random_movement()

            elif self.mission.action == Missions.HealTarget:
                if not self.perform_second_action and self.target_location is None:
                    if self.path is None or len(self.path) == 0:
                        #print("Path is null.  Making a new one")
                        self.target_location = self.mission.info.mapLocation

                        #print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.target_location.x, self.target_location.y))
                        self.update_path_to_target()

                if self.has_reached_destination():
                    # harvest at the current map location: 0 = Center
                    if self.try_heal(self.mission.info.unitId):
                        self.reset_mission()
                else:
                    self.follow_path()

            #Attacks nearby units
            nearby = self.game_controller.sense_nearby_units(self.unit.location.map_location(), 2)
            for other in nearby:
                if other.team != self.game_controller.team() and self.game_controller.is_attack_ready(self.unit.id) \
                and self.game_controller.can_attack(self.unit.id, other.id):
                    print('Knight {} attacked a thing!'.format(self.unit.id))
                    self.game_controller.attack(self.unit.id, other.id)
                    break

    def try_heal(self, target_unit_id):
        """This trys to heal units"""
        #TODO check heat is low enough
        if not self.game_controller.can_heal(self.unit.id, target_unit_id):
            print ("Healer [{}] cannot heal the target [{}]".format(self.unit.id, target_unit_id))
            return False

        self.game_controller.heal(self.unit.id, target_unit_id)
        return True

    def try_overcharge(self, target_unit_id):
        """This trys to overcharge"""
        #TODO check has research

        #Check cooldown of Overcharge ability
        if not self.game_controller.is_overcharge_ready(self.unit.id):
            print("Overcharge is not ready for Healer [{}]".format(self.unit.id))
            return False

        if not self.game_controller.can_overcharge(self.unit.id, target_unit_id):
            print("Healer [{}] cannot Overcharge the target [{}]".format(self.unit.id, target_unit_id))
            return False

        self.game_controller.overcharge(self.unit.id, target_unit_id)
        return True
