"""This is our Pathfinding Controller"""
import random
import sys
import traceback
import battlecode as bc
from collections import deque
from .GraphNode import GraphNode

# Given a robot and destination, determines the best route to take
# Returns an array of directions to the calling robot
# Robot will follow the given directions until it determines that it needs to recalculate its path
# This is far more efficient than running Pathfinding every turn and more adaptive than \
# running it once only
# May implement multiple pathfinding methods and determine which to use based upon what's \
# needed or the distance
class PathfindingController:
    """This is the Pathfinding Controller"""
    def __init__(self, gameController, mapController):
        self.game_controller = gameController
        self.map_controller = mapController
        self.plan = []
        self.directions = [bc.Direction.North, bc.Direction.East, bc.Direction.South, \
		bc.Direction.West]

    def find_path_to(self, current_location, destination):
        """This finds the path to something"""
        print("starting pathfinding")
        path = []
        explored = []
        frontier = deque([])
        starting_location = self.map_controller.GetNode(current_location.x, current_location.y)
        ending_location = self.map_controller.GetNode(destination.x, destination.y)
        node = GraphNode(starting_location, None, None)
        end_node = GraphNode(ending_location, None, None)
        frontier.append(node)
        while True:
            #print("FRONTIER LENGHT IS")
            #print(len(frontier))
            if len(frontier) == 0:
                #print("frontier is empty")
                return
            else:
                #print(frontier)
                node = frontier.popleft()
                #print("seeing if popleft is give me a dict or what i need")
                #print(node.room["x"])
            new_nodes = self.explore(node)
            explored.append(node.room)
            #new_nodes = {elem for elem in new_nodes if elem not in explored}
            for nodes in new_nodes:
                #print("PRINTING WHAT IM ADDING TO FROntier")
                #print(nodes.room)
                #print(explored[0])
                #print("Nodes in Frontier")
                #print(len(frontier))
                if self.already_explored(nodes, explored):
                    pass
                    ##print("NODE ALREADY IN eXPLORED")
                    #print(len(explored))
                    #print(len(frontier))
                else:
                    if self.already_frontier(node, frontier):
                        #print("adding to frontier")
                        frontier.append(nodes)
            #print("nodes now in frontier")
            #print(len(frontier))
            #print(node.room)
            #print(end_node.room)
            if node.room == end_node.room:
                break
        while node.Parent is not None:
            #print("setting path now XXXXCXXXCXXCXXCXCXCXCXCXCXCXCX")
            path.append(node.Action)
            node = node.Parent
        print("Printing path now")
        print(path)
        return path

    def explore(self, node):
        """This explores things"""
        discovered = []
        for direction in self.directions:
            new_node = self.transition(node, direction)
            if new_node is not None:
                discovered.append(new_node)
        return discovered

    def transition(self, node, direction):
        """This transitions between things"""
        currentnode = node
        #print("Printing the new current node")
        #print(currentnode.room)
        #print(currentnode.room["x"])
        if direction == bc.Direction.North:
            #print("PRINTING CURRENT NODE71")
            #print(currentnode.room["x"])
            new_node = self.map_controller.GetNode(currentnode.room["x"], currentnode.room["y"] + 1)
        elif direction == bc.Direction.East:
            #print("PRINTING CURRENT NODE75")
            #print(currentnode.room)
            new_node = self.map_controller.GetNode(currentnode.room["x"] + 1, currentnode.room["y"])
        elif direction == bc.Direction.South:
            #print("PRINTING CURRENT NODE79")
            #print(currentnode.room)
            new_node = self.map_controller.GetNode(currentnode.room["x"], currentnode.room["y"] - 1)
        elif direction == bc.Direction.West:
            #print("PRINTING CURRENT NODE83")
            #print(currentnode.room)
            new_node = self.map_controller.GetNode(currentnode.room["x"] - 1, currentnode.room["y"])
        #print("Printing new_node in transitions")
        #print(new_node)
        new_room = None
        if new_node is not None:
            #print("ADDING to new_room in transition")
            new_room = GraphNode(new_node, node, direction)
            #print(new_room.room)
            #print("checking if new_room is a dict not what i need")
            #print(new_room.room["x"])
        return new_room

    def already_explored(self, node, explored):
        """This keeps track of places explored"""
        isexplored = False
        for item in explored:
            if node.room["hash"] == item["hash"]:
                #print("Setting Is explored to TRUE")
                #print(node.room["hash"])
                #print(item["hash"])
                isexplored = True
                break
        return isexplored

    def already_frontier(self, node, frontier):
        """This is already the frontier"""
        not_in_frontier = True
        for item in frontier:
            if node.room["hash"] == item.room["hash"]:
                not_in_frontier = False
                break
        return not_in_frontier
