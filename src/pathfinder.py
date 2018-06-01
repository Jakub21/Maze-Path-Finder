'''Jakub21
May 2018
MIT License
Python 3.6
--------------------------------
Path finder
Find path between two points in 2D list
'''



################################
from math import sqrt
import logging
Log = logging.getLogger('MainLogger')



################################
def InitGlobals(Size, PtA, PtB, Values):
    '''pathfinder.InitGlobals [Size] [PtA] [PtB] [Values]
    Creates global variables that contain data from parameters.
    Function must be called before any other in this file
    --------------------------------
    Parameters
    - Size                  | Size of a maze to generate (2-tuple: width, height)
    - PtA                   | Starting point (2-tuple: x-coord, y-coord)
    - PtB                   | Starting point (2-tuple: x-coord, y-coord)
    - Values                | 2-tuple: Wall value, Blank value
    --------------------------------
    Returns None
    '''
    global SIZE, PTA, PTB
    SIZE = Size
    PTA, PTB = PtA, PtB
    global WALL, BLANK
    WALL, BLANK = Values



################################
def CheckDistance(PointA, PointB):
    '''pathfinder.CheckDistance [PointA] [PointB]
    Calculate distance between two points
    --------------------------------
    Parameters
    - PointA                | Point (2-tuple: x-coord, y-coord)
    - PointB                | Point (2-tuple: x-coord, y-coord)
    --------------------------------
    Returns
    - Distance              | Distance between points
    '''
    xa, ya = PointA
    xb, yb = PointB
    return sqrt(((xa-xb)**2)+((ya-yb)**2))



################################
def StepDir(Old, New):
    '''pathfinder.StepDir [Old] [New]
    Direction of step (only 1-axis)
    --------------------------------
    Parameters
    - Old                   | Point (2-tuple: x-coord, y-coord)
    - New                   | Point (2-tuple: x-coord, y-coord)
    --------------------------------
    Returns
    - Direction             | String
    '''
    xa, ya = Old
    xb, yb = New
    if xb > xa: step = 'Right'
    elif xb < xa: step = 'Left'
    elif yb > ya: step = 'Down'
    elif yb < ya: step = 'Up'
    else: step = 'None'
    return step



################################
def AddStep(Maze, Range):
    '''pathfinder.AddStep [Maze] [Range]
    Receive map of points that could be reached in x moves and
    create map of points that could be reached in x+1 moves.
    --------------------------------
    Parameters
    - Maze                  | 2D list only with values matching globals WALL and BLANK
    - Range                 | 2D list (booleans (reachable or not))
    --------------------------------
    Returns
    - Range                 | 2D list (booleans (reachable or not))
    '''
    width, height = SIZE
    NewRange = [[False for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            if Maze[y][x] == WALL: continue
            top, bottom, left, right = [WALL]*4
            try:
                if y-1 > 0: top = Range[y-1][x]
            except IndexError: pass
            try:
                if y+1 < height: bottom = Range[y+1][x]
            except IndexError: pass
            try:
                if x-1 > 0: left = Range[y][x-1]
            except IndexError: pass
            try:
                if x+1 < width: right = Range[y][x+1]
            except IndexError: pass
            if True in (Range[y][x], top, bottom, left, right):
                NewRange[y][x] = True
    return NewRange

################################
def GetMidPoint(Maze, ptA, ptB):
    '''pathfinder.GetMidPoint [Maze] [ptA] [ptB]
    Finds point that is as close as possible to both points.
    Distances midpoint-ptA and midpoint-ptB are equal (+-1).
    --------------------------------
    Parameters
    - Maze                  | 2D list only with values matching globals WALL and BLANK
    - ptA                   | Point (2-tuple: x-coord, y-coord)
    - ptB                   | Point (2-tuple: x-coord, y-coord)
    --------------------------------
    Returns
    - Path                  | Point (2-tuple: x-coord, y-coord)
    '''

    import src.images as img

    width, height = SIZE
    range_a = [[False for x in range(width)] for y in range(height)]
    range_b = [[False for x in range(width)] for y in range(height)]
    range_a[ptA[1]][ptA[0]] = True
    range_b[ptB[1]][ptB[0]] = True
    Matches = []
    dist = 0
    while Matches == []:
        range_a = AddStep(Maze, range_a)
        range_b = AddStep(Maze, range_b)
        dist += 1
        pts_in_a = []
        pts_in_b = []
        for y in range(height):
            for x in range(width):
                if range_a[y][x]: pts_in_a.append((x,y))
                if range_b[y][x]: pts_in_b.append((x,y))
        Matches = [el for el in pts_in_a if el in pts_in_b]
    return Matches[0]



################################
def FindPath(Maze):
    '''pathfinder.FindPath [Maze]
    Finds the shortest (?) path between pt. A and B.
    Points are global variables PTA and PTB
    --------------------------------
    Parameters
    - Maze                  | 2D list only with values matching globals WALL and BLANK
    --------------------------------
    Returns
    - Path                  | List of points (2-tuple: x-coord, y-coord)
    '''
    Log.info('Creating path')
    Path = []
    pta = PTA
    while pta != PTB:
        new = PTB
        mp_index = 0
        while CheckDistance(pta, new) > 1:
            new = GetMidPoint(Maze, pta, new)
            mp_index += 1
        Path.append(pta)
        Log.info('Direction: '+StepDir(pta, new))
        pta = new
    return Path
