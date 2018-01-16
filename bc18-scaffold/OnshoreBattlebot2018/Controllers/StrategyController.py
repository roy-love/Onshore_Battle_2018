from enum import Enum

# Uses all known information from various controllers to determine the current strategy
# Stores the values from enums, for easy access
# Start by simply returning {"Default"} until we get the basics finished.
class StrategyController:
    """This is the strategy controller"""
    def __init__(self, gameController, mapController, enemyTrackingController):
        self.game_controller = gameController
        self.map_controller = mapController
        self.enemy_tracking_controller = enemyTrackingController

        self.macro_strategy = MacroStrategies.Default
        self.unit_strategy = UnitStrategies.Default

    #TODO set default strategy based upon the current map
    def set_default_strategy(self):
        """This sets default strategy"""
        self.macro_strategy = MacroStrategies.Default
        self.unitStrategy = UnitStrategies.Default

    #TODO update strategy based upon changes to the map, enemies seen, or any other criteria
    def update_strategy(self):
        """This updates strategy"""
        pass

#Add more strategy types as needed
class MacroStrategies(Enum):
    """These are macro-strategies"""
    Default = 0
    ZergRush = 1
    Turtle = 2
    MarsRush = 3

class UnitStrategies(Enum):
    """These are unit strategies"""
    Default = 0
    WorkerRush = 1
    KnightRush = 2
    MageRush = 3
    RangerRush = 4
    HealerRush = 5
