# Wean Hall Node Mapper

# Node mapper will go through different floor plan images and, if it detects
# a red pixel, will add a Node object at that pixel (x,y) location along with
# its floor number. If the pixel is purple, it will add a Room object (subclass
# of the Node class) at that (x,y) location along with its floor number and a
# string that would correspond to its room number. There will later be a
# dictionary that maps Nodes to a corresponding letter and floor

# Maps rooms and hallway intersections as nodes. Nodes are mapped such that they
# are at the center of their respective hallways.

"""
def make2dList(rows, cols, default):
    temp = []
    for row in range(rows): temp += [default * cols]
    return temp
#####################################################################
#####################################################################
# Creates list of empty lists to represent nodes of each floor
allNodes = make2dList(9, 1, [])
"""

#####################################################################
#####################################################################

# Node Classes

class Node(object):
    # Node class to more easily create objects to represent each node
    def __init__(self, x, y, floor, name=None):
        self.coords = (x, y, floor)
        self.name = name
    def getCoords(self):
        return self.coords
    def getName(self):
        return self.name
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name==other.name
        elif isinstance(other, str):
            return self.name==other
        else:
            return False

        # return (isinstance(other, Node) and self.name==other.name)
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return str(self.name)


class Room(Node):
    # Room class as subclass of Node to store information about rooms.
    def __init__(self, x, y, floor, name, dirFromNode):
        super().__init__(x, y, floor, name)
        # self.roomName = roomName
        self.dirFromNode = dirFromNode
    
    def getDirFromNode(self):
        return self.dirFromNode


class Intersection(Node):
    # Intersection class as subclass of Node to store information about ints.
    def __init__(self, x, y, floor, name): # , dirConnections
        super().__init__(x, y, floor, name)
        # self.intName = intName
        # self.dirConnections = dirConnections
    # def getDirConnections(self):
    #     return self.dirConnections


class Elevator(Node):
    # Elevator class as subclass of Node to store information about elevators.
    def __init__(self, x, y, floor, name):
        super().__init__(x, y, floor)
        # self.elevName = elevName
   


#####################################################################
#####################################################################

# Nested dictionary where allNodes represents Wean Hall and each sub-dictionary
# represents each floor within Wean Hall

def mapAllNodes():
    WH1 = {"1Elevator": Elevator(305, 995, 1, "1Elevator"),
           "1AInt": Intersection(475, 995, 1, "1AInt"),
           "1BInt": Intersection(475, 667, 1, "1BInt"),
           "1CInt": Intersection(475, 460, 1, "1CInt"),
           "1DInt": Intersection(2015, 460, 1, "1DInt"),
           "1001": Room(375, 995, 1, "1001", "S"),
           "1004": Room(475, 815, 1, "1004", "W"),
           "1006": Room(200, 667, 1, "1006", "W"),
           "1009": Room(260, 667, 1, "1009", "N"),
           "1010": Room(200, 667, 1, "1010", "S"),
           "1011": Room(343, 667, 1, "1011", "N"),
           "1013": Room(343, 667, 1, "1013", "S"),
           "1014": Room(475, 460, 1, "1014", "W"),
           "1301": Room(590, 460, 1, "1301", "N"),
           "1302": Room(670, 460, 1, "1302", "S"),
           "1303": Room(670, 460, 1, "1303", "N"),
           "1305": Room(725, 460, 1, "1305", "N"),
           "1307": Room(850, 460, 1, "1307", "N"),
           "1309": Room(904, 460, 1, "1309", "N"),
           "1311": Room(1030, 460, 1, "1311", "N"),
           "1312": Room(950, 460, 1, "1312", "S"),
           "1313": Room(1085, 460, 1, "1313", "N"),
           "1315": Room(1200, 460, 1, "1315", "N"),
           "1317": Room(1345, 460, 1, "1317", "N"),
           "1318": Room(1030, 460, 1, "1318", "S"),
           "1319": Room(1400, 460, 1, "1319", "N"),
           "1320": Room(1185, 460, 1, "1320", "S"),
           "1321": Room(1533, 460, 1, "1321", "N"),
           "1322": Room(1475, 460, 1, "1322", "S"),
           "1323": Room(1580, 460, 1, "1323", "N"),
           "1324": Room(1620, 460, 1, "1324", "S"),
           "1325": Room(1750, 460, 1, "1325", "N"),
           "1326": Room(1722, 460, 1, "1326", "S"),
           "1329": Room(1790, 460, 1, "1329", "N"),
           "1331": Room(1845, 460, 1, "1331", "N"),
           "1333": Room(1907, 460, 1, "1333", "N"),
           "1340": Room(2015, 460, 1, "1340", "E") }
    WH2 = {} #{"2001": Room()}
    WH3 = {} #{"3001": Room()}
    WH4 = {} #{"4001": Room()}
    WH5 = {#"5Elevator": Elevator(),
           "5AInt": Intersection(1085, 675, 5, "5AInt"),
           "5BInt": Intersection(977, 675, 5, "5BInt"),
           "5CInt": Intersection(1197, 675, 5, "5CInt"),
           "5DInt": Intersection(977, 495, 5, "5DInt"),
           "5EInt": Intersection(977, 440, 5, "5EInt"),
           "5FInt": Intersection(1197, 440, 5, "5FInt"),
           "5GInt": Intersection(1197, 290, 5, "5GInt"),
           "5HInt": Intersection(2300, 290, 5, "5HInt"),
           "5IInt": Intersection(2300, 675, 5, "5IInt"),
           "5JInt": Intersection(390, 675, 5, "5JInt"),
           "5KInt": Intersection(390, 495, 5, "5KInt"),
           "5LInt": Intersection(620, 495, 5, "5LInt"),
           "5MInt": Intersection(620, 520, 5, "5MInt"),
           "5NInt": Intersection(705, 520, 5, "5NInt"),
           "5OInt": Intersection(705, 495, 5, "5OInt"),
           "5301": Room(1286, 290, 5, "5301", "N"),
           "5302": Room(1286, 290, 5, "5302", "S"),
           "5303": Room(1321, 290, 5, "5303", "N"),
           "5304": Room(1393, 290, 5, "5304", "S"),
           "5307": Room(1460, 290, 5, "5307", "N"),
           "5309": Room(1546, 290, 5, "5309", "N"),
           "5310": Room(1515, 290, 5, "5310", "S"),
           "5311": Room(1580, 290, 5, "5311", "N"),
           "5312": Room(1630, 290, 5, "5312", "S"),
           "5313": Room(1662, 290, 5, "5313", "N"),
           "5315": Room(1707, 290, 5, "5315", "N"),
           "5316": Room(1748, 290, 5, "5316", "S"),
           "5317": Room(1780, 290, 5, "5317", "N"),
           "5319": Room(1838, 290, 5, "5319", "N"),
           "5320": Room(1863, 290, 5, "5320", "S"),
           "5321": Room(1904, 290, 5, "5321", "N"),
           "5324": Room(1980, 290, 5, "5324", "S"),
           "5325": Room(2022, 290, 5, "5325", "N"),
           "5328": Room(2097, 290, 5, "5328", "S"),
           "5331": Room(2084, 290, 5, "5331", "N"),
           "5333": Room(2123, 290, 5, "5333", "N"),
           "5336": Room(2212, 290, 5, "5336", "S"),
           "5337": Room(2300, 290, 5, "5337", "N"), # Bathroom
           "5403": Room(1287, 675, 5, "5403", "N"),
           "5409": Room(1515, 675, 5, "5409", "N"),
           "5415": Room(1750, 675, 5, "5415", "N"),
           "5421": Room(2054, 675, 5, "5421", "N")}
    WH6 = {} #{"6001": Room()}
    WH7 = {} #{"7001": Room()}
    WH8 = {} #{"8001": Room()}
    WH9 = {} #{"9001": Room()}

    allNodes = {"WH1": WH1, "WH2": WH2, "WH3": WH3, "WH4": WH4, "WH5": WH5,
                    "WH6": WH6, "WH7": WH7, "WH8": WH8, "WH9": WH9}

    return allNodes

#####################################################################
#####################################################################

# Connections

def mapAllConnections():
    WH1Conns = {"1Elevator": ["2Elevator", "3Elevator", "4Elevator",
                              "5Elevator", "6Elevator", "7Elevator",
                              "8Elevator", "9Elevator", "1001", "1002"],
                "1001": ["1Elevator", "1AInt"], "1002": ["1Elevator"],
                "1AInt": ["1001", "1004"], "1004": ["1AInt", "1BInt"],
                "1BInt": ["1004", "1011", "1CInt"], "1011": ["1BInt", "1013"],
                "1013": ["1011", "1009"], "1009": ["1013", "1010"],
                "1010": ["1009", "1006"], "1006": ["1010"],
                "1CInt": ["1BInt", "1014", "1301"], "1014": ["1CInt"],
                "1301": ["1CInt", "1302"], "1302": ["1301", "1303"],
                "1303": ["1302", "1305"], "1305": ["1303", "1307"],
                "1307": ["1305", "1309"], "1309": ["1307", "1312"],
                "1312": ["1309", "1311"], "1311": ["1312", "1318"],
                "1318": ["1311", "1313"], "1313": ["1318", "1320"],
                "1320": ["1313", "1315"], "1315": ["1320", "1317"],
                "1317": ["1315", "1319"], "1319": ["1317", "1322"],
                "1322": ["1319", "1321"], "1321": ["1322", "1323"],
                "1323": ["1321", "1324"], "1324": ["1323", "1326"],
                "1326": ["1324", "1325"], "1325": ["1326", "1329"],
                "1329": ["1325", "1331"], "1331": ["1329", "1333"],
                "1333": ["1331", "1DInt"], "1DInt": ["1333", "1340"]
               }
    WH2Conns = {"2Elevator": ["1Elevator", "3Elevator", "4Elevator",
                              "5Elevator", "6Elevator", "7Elevator",
                              "8Elevator", "9Elevator", "5AInt"],
                "5AInt": ["5Elevator", "5BInt", "5CInt"],
                "5BInt": ["5AInt", "5DInt"],
                "5DInt": ["5BInt", "5EInt"],
                "5EInt": ["5DInt", "5FInt"],
                "5CInt": ["5AInt", "5FInt", "5403"],
                "5403": ["5CInt", "5409"],
                "5409": ["5403", "5415"],
                "5415": ["5409", "5421"],
                "5421": ["5415", "5IInt"],
                "5IInt": ["5421", "5HInt"],
                "5HInt": ["5IInt", "5337", "5336"],
                "5337": ["5HInt"],
                "5336": ["5HInt", "5333"],
                "5333": ["5336", "5328"],
                "5328": ["5333", "5331"],
                "5331": ["5328", "5325"],
                "5325": ["5331", "5324"],
                "5324": ["5325", "5321"],
                "5321": ["5324", "5320"],
                "5320": ["5321", "5319"],
                "5319": ["5320", "5317"],
                "5317": ["5319", "5316"],
                "5316": ["5317", "5315"],
                "5315": ["5316", "5313"],
                "5313": ["5315", "5312"],
                "5312": ["5313", "5311"],
                "5311": ["5312", "5309"],
                "5309": ["5311", "5310"],
                "5310": ["5309", "5307"],
                "5307": ["5310", "5304"],
                "5304": ["5307", "5303"],
                "5303": ["5304", "5302"],
                "5302": ["5303", "5301"],
                "5301": ["5302", "5GInt"],
                "5GInt": ["5301", "5014", "5FInt"],
                "5014": ["5GInt"]
               }
    WH3Conns = {"3Elevator": []
               }
    WH4Conns = {"4Elevator": []
               }
    WH5Conns = {"5Elevator": []
               }
    WH6Conns = {"6Elevator": []
               }
    WH7Conns = {"7Elevator": []
               }
    WH8Conns = {"8Elevator": []
               }
    WH9Conns = {"9Elevator": []
               }

    allConnections = {**WH1Conns, **WH2Conns, **WH3Conns, **WH4Conns,
                      **WH5Conns, **WH6Conns, **WH7Conns, **WH8Conns,
                      **WH9Conns}

    return allConnections


#####################################################################
#####################################################################












"""
def addNode(x, y, floor, roomName=None):
    nodeCode = str(floor) + chr(ord("A") + len(allNodes[floor-1]))
    if roomName == None:
        node = Node(x, y, floor, nodeCode)
        allNodes[floor-1].append(node)
    else:
        node = Room(x, y, floor, nodeCode, roomName)
        allNodes[floor-1].append(node)
"""


"""
def createConnections():
    for currFloor in allNodes:
        for baseNode in currFloor:
            (baseX, baseY, baseFloor) = baseNode.getCoords()
            (nearestLowX, nearestHighX) = None
            (nearestLowXNode, nearestHighXNode) = None
            (nearestLowY, nearestHighY) = None
            (nearestLowYNode, nearestHighYNode) = None
            for checkNode in currFloor:
                if baseNode == checkNode: continue # continue if same node
                (checkX, checkY, checkFloor) = checkNode.getCoords()
                if baseX == checkX: # if x-coords are same, check y coords
                elif baseY == checkY: # if 
"""







# addNode(586, 460, 1, "Wean Hall 1301")
# 586,460 --> WH 1301 (center of hall)




