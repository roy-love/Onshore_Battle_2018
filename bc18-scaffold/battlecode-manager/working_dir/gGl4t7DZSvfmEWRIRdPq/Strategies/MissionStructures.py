from enum import Enum

class Missions(Enum):
    Idle = 0 
    RandomMovement = 1 # Assign location to move to
    Mining = 2 # Assign location to mine
    FollowUnit = 3 # Assign Unit to follow
    Scout = 4 # Assign location to scout
    Patrol = 5 # Assign two locations to partrol 
    DestroyTarget = 6 # Assign unit to destroy
    DefendTarget = 7 # Assign unit to defend
    BuildFactory = 8 # Assign location to build a factory
    CreateBlueprint = 9 # Assign location to lay down blueprint
    TrainBot = 10 # Instruct Factory to build a bot
    BuildRocket = 11 # Instruct Factory to build a rocket
    Garrison = 12 # Assign target factory to garrison
    HealTarget = 13 # Assign target to heal
    
    
class MissionTypes(Enum):
    Worker = 0
    Healer = 1
    Combat = 2
    Factory = 3

class Mission:
    def __init__(self):
        self.action = None
        self.info = None

class MissionInfo: 
    def __init__(self):
        self.mapLocation = None
        self.unitId = None  
        self.unit = None