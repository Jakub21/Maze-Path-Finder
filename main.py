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
def getLogger():
    '''main.getLogger
    Creates Logger object
    --------------------------------
    No parameters
    --------------------------------
    Returns
    - logging.Logger object
    '''
    logging_level = logging.INFO
    Log = logging.getLogger('MainLogger')
    Log.setLevel(logging_level)
    formatter_string = '[%(asctime)s][%(filename)s:%(lineno)d] %(message)s'
    formatter = logging.Formatter(formatter_string, '%H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)
    Log.addHandler(console_handler)
    return Log



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
    parser.add_argument('pta',default=[None],action='store',nargs=2,
        type=int,help='Define starting point')
    parser.add_argument('ptb',default=[None],action='store',nargs=2,
        type=int,help='Define finish point')
    parser.add_argument('-rand',default=[None],action='store',nargs=2,
        type=int,help='Generate random maze')
    parser.add_argument('-file',default=None,action='store',
        type=str,help='Load maze from file')
    return parser



################################
if __name__ == '__main__':
    # Logs
    Log = getLogger()
    Log.info('Program starts')

    # Arguments
    parser = GetParser()
    args = parser.parse_args()
    Log.debug('Arguments:\n  '+'\n  '.join([str(key)+': '+str(value)
        for key, value in args.__dict__.items()]))

    # Arguments validation
    if (args.pta == [None]) or (args.ptb == [None]):
        Log.error('Points are not defined. Use -pta[x][y] and -ptb[x][y]')
        exit()
    if (args.rand == [None]) and (args.file == None):
        Log.error('There is no maze source defined. '+\
            'Use -rand[x][y] or -file[path]')
        exit()
    if (args.rand != [None]) and (args.file != None):
        Log.error('There are two maze sources defined. Please remove one')
        exit()

    # Maze size and source
    if (args.rand != [None]):
        width, height = args.rand
        source = 'R'
    else:
        width, height = img.GetSize(args.file)
        source = 'F'

    # Global variables
    global SIZE, PTA, PTB, WALL, BLANK
    SIZE = (width, height)
    PTA = tuple(args.pta)
    PTB = tuple(args.ptb)
    WALL, BLANK = False, True

    # Info
    Log.info('Maze size: '+str(SIZE))
    Log.info('Points: '+str(PTA)+' '+str(PTB))
    Log.info('Straight line distance: '+str(round(pf.CheckDistance(PTA,PTB),1)))

    # Points validation (check if in boundaries)
    if (PTA[0] >= width) or (PTB[0] >= width) or\
        (PTA[1] >= height) or (PTB[1] >= height):
        Log.error('At least one point is out of boundaries')
        exit()

    # Global variables in other files
    maze.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    img.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    pf.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))

    # Load / Generate maze
    if   source == 'R': Maze = maze.GetMaze()
    elif source == 'F': Maze = img.GetMazeImg('maze.png')

    # Find path
    Path = pf.FindPath(Maze)
    Log.info('Path length: '+str(len(Path)))

    # Create path image
    path_map = pf.MarkPoints(Path)
    image = img.GenerateImage(Maze, path_map, Scale=4)
    image.save('path.png')
