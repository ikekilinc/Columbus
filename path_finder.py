# Pathfinder - A* Search Algorithm

# Utilizing dictionary plotting connections between different nodes, pathfinder
# calculates the shortest path from one node (start) to another (destination).
# Pathfinder utilizes the A* search algorithm to calculate this path and then
# converts list of nodes to visit en route to destination to left/right/forward
# directions for the product user. The heuristic used by the A* algorithm is the
# direct distance from the current node being tested to the destination node.

from node_mapper import *

def pathFinder(startStr, endStr, mode=None):
    startFloor = startStr[0]
    endFloor = None
    if endStr != None:
        endFloor = endStr[0]

    if mode == "nearestRestroom":
        endStr = nearestRestroom(startStr)
        return navigateNodes(startStr, endStr)

    elif mode == "nearestPrinter":
        endStr = nearestPrinter(startStr)
        return navigateNodes(startStr, endStr)

    elif (endFloor != None) and (startFloor == endFloor):
        return navigateNodes(startStr, endStr)

    elif (endFloor != None) and (startFloor != endFloor):
        startElevatorStr = "%sElevator" % startStr[0]
        endElevatorStr = "%sElevator" % endStr[0]
        
        startSegment = navigateNodes(startStr, startElevatorStr)
        endSegment = navigateNodes(endElevatorStr, endStr)
        
        return startSegment + endSegment

    else:
        # do something maybe?
        pass

#####################################################################
#####################################################################

def directDist(nodeA, nodeB):
    # Calculates Euclidian distance between two points
    # if currNode and endNode are both elevators, do something else
    if isinstance(nodeA, Elevator) and isinstance(nodeB, Elevator):
        return 10**10
    else:
        return ((nodeA.getCoords()[0] - nodeB.getCoords()[0])**2 + \
                (nodeA.getCoords()[1] - nodeB.getCoords()[1])**2) ** 0.5

def calcFCost(currNode, endNode):
    # Total cost of getting from startNode to endNode via currNode. Calculated
    # by finding direct distance cost from currNode to endNode via utilization
    # of pythagorean theorem.
    return directDist(currNode, endNode)

def findLowestFCost(openNodes, endNode):
    # Finds the node among the currently open nodes that has the lowest F cost,
    # such that the F cost of a node is defined as cost of getting from the
    # origin to the destination via the selected node.
    bestNode = None
    bestCost = 10**42

    for node in openNodes:
        currFCost = calcFCost(node, endNode)
        if currFCost < bestCost:
            bestCost = currFCost
            bestNode = node
    return bestNode

def calcBCost(currNodeIndex, nodeList):
    # Function calculates (recursively) the distance from the current node to
    # the origin via previously visited nodes.
    if currNodeIndex == 0:
        return 0

    nodeA = nodeList[currNodeIndex-1]
    nodeB = nodeList[currNodeIndex]
    return directDist(nodeA, nodeB) + calcBCost(currNodeIndex-1, nodeList)


#####################################################################
#####################################################################

# If nodes not on same floor, then do navigateNodes from origin to elevator of
# currFloor and then do navigateNodes from elevator of destFloor to destination.

def navigateNodes(startStr, endStr): # start and end are the objects of start node and end node
    allNodesMap = mapAllNodes() # dictionary mapping each node's name to its object
    allConnsMap = mapAllConnections() # dictionary mapping each node to its connected nodes

    # allNodesSet = set(allNodesMap.values().values())

    startFloor = "WH%s" % startStr[0]
    startNode = allNodesMap[startFloor][startStr]
    
    endFloor = "WH%s" % endStr[0]
    endNode = allNodesMap[endFloor][endStr]

    # if (startNode not in allNodesSet) or (endNode not in allNodesSet):
    #     return None

    closedNodes = set()
    openNodes = set()
    openNodes.add(startNode)

    cameFrom = dict()

    print("startNode: ", startNode)
    print("endNode: ", endNode)

    while len(openNodes) != 0:
        currNode = findLowestFCost(openNodes, endNode)
        print("    currNode: ", currNode)

        if currNode == None:
            return None # there is no possible path to endNode

        openNodes.remove(currNode)
        closedNodes.add(currNode)

        if currNode == endNode: # If Columbus arrives at destination via Nodes
            # Reconstruct path taken to arrive at destination
            nodeList = reconstruct_path(currNode, startNode, cameFrom)
            return nodeList
            """
            # Convert path into directions that could be interpreted by users
            directions = "FIND HUMAN INTERPRETABLE DIRECTIONS FROM NODE LIST"
            # calculate pixel distance via nodes from start to destination
            pixelDistance = calcBCost(len(nodeList)-1, nodeList)
            # convert pixel distance to actual distance
            distance = "FIND ACTUAL DISTANCE CONVERSIONS, CREATE LIST, CONVERT"
            return [nodeList, distance]
            # return [nodeList, pixelDistance]
            """

        for neighbor in getAllConnections(allNodesMap, allConnsMap, currNode):
            if neighbor in closedNodes:
                continue # ignore already evaluated nodes
            tempFScore = calcFCost(currNode, endNode)
            if ((neighbor not in openNodes) or
                (tempFScore < calcFCost(neighbor, endNode))):
                cameFrom[neighbor] = currNode

                if neighbor not in openNodes:
                    openNodes.add(neighbor)

#####################################################################
#####################################################################

def getAllConnections(allNodesMap, allConnsMap, currNode):
    # think about how elevators affect this (specifically the floor line)
    allNeighbors = [ ]

    for neighborStr in allConnsMap[currNode.getName()]:
        floor = "WH%s" % neighborStr[0]
        neighbor = allNodesMap[floor][neighborStr]
        allNeighbors.append(neighbor)

    return allNeighbors


def reconstruct_path(currNode, startNode, cameFrom):
    # Once the A* navigateNodes algorithm has found the most efficient path from
    # the start node to the destination, this function recursively returns a 
    # list of all nodes (room, intersection, etc.) visited in this calculated 
    # path.
    if currNode == startNode:
        return [currNode]

    parentNode = cameFrom[currNode]
    return reconstruct_path(parentNode, startNode, cameFrom) + [currNode]


def findUserDirections(nodeList, startOrientation=None):
    # Takes list of nodes to visit and returns list of left, right, straight
    # directions user must take at intersections to arrive at destination.

    # DO THIS BY COMPARING X,Y COORDINATES OF NODES AND SEEING IF CHANGE
    # IN X,Y COORDINATES IS +VE OR -VE AT START AND AT EACH INTERSECTION

    if startOrientation == None:
        startOrientation = nodeList[0].getDirFromNode()

    if "at last node":
        return []
    
    if isinstance(nodeList[-2], Intersection):
        pass

def nearestRestroom(startStr):
    allNodesMap = mapAllNodes()
    currFloor = "WH%s" % startStr[0]
    startNode = allNodesMap[currFloor][startStr]


    bestDest = ""
    smallestDist = 10e42
    for node in allNodesMap[currFloor].values():
        if not isinstance(node, Restroom):
            continue
        currDist = directDist(startNode, node)
        if currDist < smallestDist:
            smallestDist = currDist
            bestDest = str(node)
    return bestDest

def nearestPrinter(startStr):
    allNodesMap = mapAllNodes()
    currFloor = "WH%s" % startStr[0]
    startNode = allNodesMap[currFloor][startStr]

    def isFeasibleFloor(currFloor, allNodesMap):
        for node in allNodesMap[currFloor].values():
            if isinstance(node, Printer):
                return True

    if not isFeasibleFloor(currFloor, allNodesMap):
        for floor in range(1, 10):
            currFloor = "WH%s" % floor
            if isFeasibleFloor(currFloor, allNodesMap):
                printerFloor = currFloor
                break

    bestDest = ""
    smallestDist = 10e42
    for node in allNodesMap[printerFloor].values():
        if not isinstance(node, Printer):
            continue
        currDist = directDist(startNode, node)
        if currDist < smallestDist:
            smallestDist = currDist
            bestDest = str(node)
    return bestDest

#####################################################################
#####################################################################

# Navigation Testing

# nodesPath = pathFinder("1001", "5301")
# print(nodesPath)

