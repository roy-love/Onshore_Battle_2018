import battlecode as bc

from Entities import *

# Keeps a list of all friendly units (share with buildController - figure out which should store it)
# Loops over all units, running their "Run" methods one at a time
# Can prioritize robots by importance or any other activation order
# Responsible for putting robots back into the queue if a healer resets their cooldowns
class UnitController:
    """This is the unit controller"""
    def __init__(self, gameController, strategyController, \
    pathfindingController, missionController, mapController):
        self.game_controller = gameController
        self.strategy_controller = strategyController
        self.pathfinding_controller = pathfindingController
        self.mission_controller = missionController
        self.mapController = mapController

        self.robots = []
        self.structures = []

    def update_units(self):
        """This updates units"""
        self.__delete_killed_units()
        self.__add_unregistered_units()

        if self.game_controller.round() > 95 and self.game_controller.round() < 101:
            self.mission_controller.MustBuildRocket = True
            

    def GetWorkerCount(self):
        count = 0
        for robot in self.robots:
            if robot.unit.unit_type == bc.UnitType.Worker:
                count += 1
        return count

    # Removes robots and structures that are not found on the map any longer
    def __delete_killed_units(self):
        print("Checking for dead robots that should be removed from list")
        if len(self.robots) == 0:
            print("Robot list empty.  Nothing to remove")
            return

        # Robots that still exist are re-added to the robot list
        # Any not in the list are removed then picked up by garbage collection later
        print("Current robots registered = {}".format(len(self.robots)))
        print("Robots alive = {}".format(len(self.game_controller.my_units())))
        self.robots = [robot for robot in self.robots if any(\
        unit.id == robot.unit.id for unit in self.game_controller.my_units())]
        print("Current robots registered after removal = {}".format(len(self.robots)))

    # Creates robots and structures for all units that do not yet have them
    # Can occur when moving robots between planets or for the default starting worker
    # if a robot exists, update its unit binding to account for server side changes
    def __add_unregistered_units(self):
        friendly_units = self.game_controller.my_units()
        if len(friendly_units) == 0:
            print("There are no units on the field. Nothing to add.")
            return

        print("{} units found to register".format(len(friendly_units)))
        #If there are no robots registered, just register them all
        if len(self.robots) == 0:
            print("No robots currently in the list.  Registering them all")
            for unit in self.game_controller.my_units():
                self.__register_unit(unit)
        else:
            print("Comparing existing robots against units")
            for unit in self.game_controller.my_units():
                for friendly_unit in self.robots:
                    if friendly_unit.unit.id == unit.id:
                        print("Robot already registered. Updating")
                        friendly_unit.unit = unit
                        break
                else:
                    for friendly_unit in self.structures:
                        if friendly_unit.unit.id == unit.id:
                            print("Structure already registered. Updating")
                            friendly_unit.unit = unit
                            break
                    else:
                        self.__register_unit(unit)

    def __register_unit(self, unit):
        if unit.unit_type == bc.UnitType.Healer:
            self.robots.append(Healer(self.game_controller, \
            self, self.pathfinding_controller, self.mission_controller, unit, self.mapController))
        elif unit.unit_type == bc.UnitType.Knight:
            self.robots.append(Knight(self.game_controller, \
            self, self.pathfinding_controller, self.mission_controller, unit, self.mapController))
        elif unit.unit_type == bc.UnitType.Mage:
            self.robots.append(Mage(self.game_controller, \
            self, self.pathfinding_controller, self.mission_controller, unit, self.mapController))
        elif unit.unit_type == bc.UnitType.Ranger:
            self.robots.append(Ranger(self.game_controller, \
            self, self.pathfinding_controller, self.mission_controller, unit, self.mapController))
        elif unit.unit_type == bc.UnitType.Worker:
            self.robots.append(Worker(self.game_controller, \
            self, self.pathfinding_controller, self.mission_controller, unit, self.mapController))

        elif unit.unit_type == bc.UnitType.Factory:
            self.structures.append(Factory(self.game_controller, \
            self, unit, self.mission_controller))
        elif unit.unit_type == bc.UnitType.Rocket:
            self.structures.append(Rocket(self.game_controller, self, unit))
        else:
            print("ERROR - Attempting to register an unknown unit type [{}]".format(unit.unit_type))

    # Add prioritization of turn order
    def run_units(self):
        """This runs units"""
        robot_count = len(self.robots)
        structure_count = len(self.structures)
        gc_count = len(self.game_controller.my_units())
        #print("GC.Units {}, UC.Robots+Structures {}".format(gc_count, robot_count+structure_count))
        print("Running all structures")
        print("structures count: {}".format(structure_count))
        for structure in self.structures:
            structure.run()

        print("Running all robots")
        print("robot count: {}".format(robot_count))
        for robot in self.robots:
            robot.run()
