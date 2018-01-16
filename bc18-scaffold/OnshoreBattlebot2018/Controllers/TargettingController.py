"""This is our Targetting Controller"""
import random
import sys
import traceback
#import numpy as np
import battlecode as bc

from Entities import *
from Controllers.EnemyTrackingController import *

# Given a robot, a target type to prioritize, and an enemy list
# Determines the highest priority location to move towards
# This can apply to workers looking for a build location, healers looking for allies, or rangers looking for targets
# To start, focus on simply returning the closest or most valuable target
class TargettingController:
    """This is the Targetting Controller"""
    def __init__(self, gameController, mapController, strategyController, unitController, enemyTrackingController):
        self.game_controller = gameController
        self.map_controller = mapController
        self.strategy_controller = strategyController
        self.unit_controller = unitController
        self.enemy_tracking_controller = enemyTrackingController
        self.enemy_robots = []
        self.enemy_structures = []
        self.ally = gameController.team()
        self.round_limit = 10

    # Updates units for whether they have died or if a unit needs to be added to registry
    def update_units(self):
        """This updates the units"""
        self._delete_killed_units()
        self._add_unregistered_enemy_units()
        self._remove_registered_enemy_units()

    # Deletes units that have died
    def _delete_killed_units(self):
        pass

    # Stores Robots and Structures for enemy units.
    #
    def _add_unregistered_enemy_units(self):
        if len(enemy_units) == 0:
            print("There are no enemy units on the field, nothing to add")
            return
        #print("{} enemy units found to register".format(len(enemy_units)))
        # If no enemy units have been registered, register them all
        if len(self.enemy_robots) != 0:
            for unit in enemy_units:
                for enemy_unit in self.enemy_robots:
                    if enemy_unit[0].id == unit.id:
                        print("Enemy already registered. Updating timeout")
                        enemy_unit[1] == currentRound
                        break
                else:
                    for enemy_unit in self.enemy_structures:
                        if enemy_unit[0].id == unit.id:
                            print("Structure already registered. Updating")
                            enemy_unit = unit
                            break
                        else:
                            self._register_unit(unit)
        return

    # Removes an enemy robot from the Registry
    def _remove_registered_enemy_units(self):
        if len(self.enemy_robots) == 0:
            print("There are no enemy units in the registry, nothing to remove")
            return

        print("{} enemy units found in the registry".format(len(enemy_units)))
        for enemy_unit in self.enemy_robots:
            if currentRound - enemy_unit[1] >= self.round_limit:
                print("Removing unit from registry")
                # TODO Clean-single index removal logic needs to be added here.
                pass

    # Prioritizes the enemy units for targeting.
    def __get_nearby_priority(self, unit):
        location = unit.location
        best_score = 0
        score = 0
        nearby_units = bc.sense_nearby_units(location.map_location(), 2)
        for enemy in nearby_units:
            if enemy.team != self.ally:
                if enemy.unit_type == bc.UnitType.Rocket:
                    score = 100
                elif enemy.unit_type == bc.UnitType.Knight or enemy.unit_type == bc.UnitType.Ranger or enemy.unit_type == UnitType.Mage:
                    score = 80
                elif enemy.unit_type == bc.UnitType.Worker:
                    score = 60
                else:
                    score = 40
                if score > best_score:
                    best_score = score
                    best_robot = enemy
            return best_robot

    # Sets global prioritization of enemy units
    def __get_global_priority_enemy(self):
        best_score = 0
        score = 0
        for enemy_unit in self.enemy_tracking_controller.enemy_units:
            if enemy_unit.team != self.ally:
                if enemy_unit.unit_type == bc.UnitType.Rocket:
                    score = 100
                elif enemy_unit.unit_type == bc.UnitType.Knight or enemy_unit.unit_type == bc.UnitType.Ranger or enemy_unit.unit_type == bc.UnitType.Mage:
                    score = 80
                elif enemy_unit.unit_type == bc.UnitType.Worker:
                    score = 60
                else:
                    score = 40
                if score > best_score:
                    best_score = score
                    best_robot = enemy_unit
        return best_robot

    def _register_unit(self, unit):
        if unit.unit_type == bc.UnitType.Worker:
            self.enemy_robots.append(Worker(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Knight:
            self.enemy_robots.append(Knight(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Ranger:
            self.enemy_robots.append(Ranger(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Mage:
            self.enemy_robots.append(Mage(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Healer:
            self.enemy_robots.append(Healer(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Factory:
            self.enemy_structures.append(Factory(self.game_controller, self, unit))
        elif unit.unit_type == bc.UnitType.Rocket:
            self.enemy_structures.append(Rocket(self.game_controller, self, unit))
