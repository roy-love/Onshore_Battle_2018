import battlecode as bc
import random
import sys
import traceback

class IStructure:
    """This is the IStructure"""
    def __init__(self, gameController, unitController, unit, missionController):
        self.game_controller = gameController
        self.unit_controller = unitController
        self.mission_controller = missionController
        self.unit = unit
        self.mission = None

    def update_mission(self):
        """Updates the mission"""
        if self.unit.structure_is_built() and self.mission == None:
            self.mission = self.mission_controller.get_mission(self.unit.unit_type)
            self.mission_start_round = self.game_controller.round()
            self.target_location = None
            print("Structure with id {} obtaining new mission {}".format(\
            self.unit.id, self.mission.action))
