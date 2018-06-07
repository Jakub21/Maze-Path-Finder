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
def main(Args, isinRecursion=False):
    '''main.Main [Arg] {isinRecursion}
    Calls all functions in order that depends on user's input
    --------------------------------
    Parameters
    - Arg                   | argparse namespace
    - isinRecursion         | default is False
    --------------------------------
    Returns
    - Maze                  | 2D list only with values matching WALL and BLANK
    - Path                  | List of points
    '''
    # Logger
    Log = getLogger()
    if not isinRecursion: Log.info('Program starts')
    Log.debug('Arguments:\n  '+'\n  '.join([str(key)+': '+str(value)
        for key, value in Args.__dict__.items()]))

    # Arguments validation
    if (Args.pta == [None]) or (Args.ptb == [None]):
        Log.error('Points are not defined')
        raise ValueError('Points are not defined')
    if (Args.rand == [None]) and (Args.file == None):
        Log.error('There is no maze source defined. '+\
            'Use -rand[x][y] or -file[path]')
        raise ValueError('There is no maze source defined')
    if (Args.rand != [None]) and (Args.file != None):
        Log.error('There are two maze sources defined. Please remove one')
        raise ValueError('There are two maze sources defined. Please remove one')

    # Maze size and source
    if (Args.rand != [None]):
        width, height = Args.rand
        source = 'R'
    else:
        width, height = img.GetSize(Args.file)
        source = 'F'

    # Global variables
    global SIZE, PTA, PTB, WALL, BLANK
    SIZE = (width, height)
    PTA = tuple(Args.pta)
    PTB = tuple(Args.ptb)
    WALL, BLANK = False, True

    # Info
    Log.info('Maze size: '+str(SIZE))
    Log.info('Points: '+str(PTA)+' '+str(PTB))
    Log.info('Straight line distance: '+str(round(pf.CheckDistance(PTA,PTB),1)))

    # Points validation (check if in boundaries)
    if (PTA[0] >= width) or (PTB[0] >= width) or\
        (PTA[1] >= height) or (PTB[1] >= height):
        Log.error('At least one point is out of boundaries')
        raise ValueError('At least one point is out of boundaries')

    # Global variables in other files
    maze.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    img.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))
    pf.InitGlobals(SIZE, PTA, PTB, (WALL, BLANK))

    # Load / Generate maze
    if   source == 'R': Maze = maze.GetMaze()
    elif source == 'F': Maze = img.GetMazeImg(Args.file)

    # Find path
    Path = pf.FindPath(Maze)
    if (Path == None) and (source == 'R'):
        Log.info('Re-generating maze. There were no paths.')
        return main(Args, isinRecursion=True)
    if (Path == None) and (source == 'F'):
        Log.error('There is not any path between these points in selected maze')
        raise ValueError('There is not any path between these points in selected maze')
    Log.info('Path length: '+str(len(Path)))

    return (Maze, Path)



################################
if __name__ == '__main__':
    # Arguments
    parser = GetParser()
    args = parser.parse_args()

    # Execute
    Maze, Path = main(args)

    # Create path image
    image_path = 'path.png'
    path_map = pf.MarkPoints(Path)
    image = img.GenerateImage(Maze, path_map, Scale=4)
    image.save(image_path)
