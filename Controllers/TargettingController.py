import battlecode as bc
import random
import sys
import traceback
import numpy as np

from Entities import *

# Given a robot, a target type to prioritize, and an enemy list
# Determines the highest priority location to move towards
# This can apply to workers looking for a build location, healers looking for allies, or rangers looking for targets
# To start, focus on simply returning the closest or most valuable target
class TargettingController:
    """This is the targetting controller"""
    def __init__(self, gameController, mapController, strategyController, unitController):
        self.game_controller = gameController
        self.map_controller = mapController
        self.strategy_controller = strategyController
        self.unit_controller = unitController

        self.enemy_robots = []
        self.enemy_structures = []
        self.ally = bc.team()

    enemyUnits = not ally
    roundLimit = 10


    # Updates units for whether they have died or if a unit needs to be added to registry
    def update_units(self):
        """This updates unites"""
        self._DeleteKilledUnits()
        self._AddUnregisteredEnemy_units()
        self._RemoveRegisteredEnemy_units()

    # Deletes units that have died
    def _delete_killed_units(self):
        """This deletes killed units"""
        pass

    # Stores Robots and Structures for enemy units.
    def _add_unregistered_enemy_units(self):
        """This adds unregistered enemy units"""
        if len(enemyUnits) == 0:
            print("There are no enemy units on the field, nothing to add")
            return

        print("{} enemy units found to register".format(len(enemyUnits)))
        # If no enemy units have been registered, register them all
        if len(self.enemy_robots) != 0:
            for unit in enemyUnits:
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
                            self._RegisterUnit(unit)

    # Removes an enemy robot from the Registry
    def _remove_registered_enemy_units(self):
        if len(self.enemy_robots) == 0:
            print("There are no enemy units in the registry, nothing to remove")
            return

        print("{} enemy units found in the registry".format(len(enemyUnits)))
        for enemy_unit in self.enemy_robots:
            if currentRound - enemy_unit[1] >= roundLimit:
                print("Removing unit from registry")
                # TODO Clean-single index removal logic needs to be added here.
                pass


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
            self.enemy_structures.append(Rocket(slef.gameController, self, unit))
