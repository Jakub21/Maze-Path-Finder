'''Jakub21
May 2018
MIT License
Python 3.6
--------------------------------
Program generates a maze or, if path is supplied, loads it from file.
Then program finds shortest path between two points.
'''



################################
from argparse import ArgumentParser
import src.maze as maze
import src.images as img
import src.pathfinder as pf
import logging



################################
def MarkPoints(PointList):
    '''main.MarkPoints [PointList]
    Creates 2D list, filled with False.
    Value is changed to True if coordinate is in supplied list
    --------------------------------
    Parameters
    - PointList             | List of points to mark
    --------------------------------
    Returns
    - Map                   | 2D list with booleans
    '''
    width, height = SIZE
    Map = [[False for x in range(width)] for y in range(height)]
    for pt in PointList:
        x, y = pt
        Map[y][x] = True
    return Map



################################
def GetParser():
    '''main.GetParser
    Prepares ArgumentParser object
    --------------------------------
    No parameters
    --------------------------------
    Returns
    - argparse.ArgumentParser object
    '''
    parser = ArgumentParser(description = 'Find shortest path in maze')
    parser.add_argument('width', type=int, help='Width of the maze')
    parser.add_argument('height', type=int, help='Height of the maze')
    parser.add_argument('pta_x', type=int, help='Start point: x coord.')
    parser.add_argument('pta_y', type=int, help='Start point: y coord.')
    parser.add_argument('ptb_x', type=int, help='Finish point: x coord')
    parser.add_argument('ptb_y', type=int, help='Finish point: y coord')
    #parser.add_argument('--path', type=str, action='store_const',
    #    help='Load maze from file instead')
    return parser


################################
def Main(Arg):
    '''main.Main [Arg]
    Calls all functions in order that depends on user's input
    --------------------------------
    Parameters
    - Arg (argparse namespace):
        - width             | Width of a maze
        - height            | Height of a maze
        - pta_x             | X coordinate of starting point
        - pta_y             | Y coordinate of starting point
        - ptb_x             | X coordinate of finish point
        - ptb_y             | Y coordinate of finish point
        - path              | [Optional] Path to image to load maze from
    --------------------------------
    Returns
    - Path, list of points
    '''
    Log.info('Arguments:\n  '+'\n  '.join([str(key)+': '+str(value)
        for key, value in Arg.__dict__.items()]))
    global SIZE, PTA, PTB
    SIZE = (Arg.width, Arg.height)
    PTA = (Arg.pta_x, Arg.pta_y)
    PTB = (Arg.ptb_x, Arg.ptb_y)
    WALL, BLANK = False, True

    Log.info('Points: '+str(PTA)+' '+str(PTB))
    Log.info('Straight line distance: '+str(round(pf.CheckDistance(PTA, PTB),1)))

    maze.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    img.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    pf.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))

    Maze = maze.GetMaze()
    Path = pf.FindPath(Maze)

    Log.info('Path length: '+str(len(Path)))
    return (Maze, Path)



################################
if __name__ == '__main__':
    logging_level = logging.INFO
    Log = logging.getLogger('MainLogger')
    Log.setLevel(logging_level)
    formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d] %(message)s', '%H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)
    Log.addHandler(console_handler)
    Log.info('Program starts')

    parser = GetParser()
    args = parser.parse_args()

    maze, path = Main(args)

    path_map = MarkPoints(path)
    image = img.GenerateImage(maze, path_map, Scale=4)
    image.save('path.png')
