'''This file is an example how to use classes from this repository
'''
from argparse import ArgumentParser
from src.maze import Maze
from src.run import Run

def main(args):
    while True:
        # Create Maze object
        maze = Maze(args.source)
        # Create Run object
        run = Run(maze, args.pta, args.ptb)
        try:
            # Execute find path command on Run object to find path
            run.find_path()
            break # Path was found
        except ValueError:
            # There are no valid paths in this maze
            print('Attempt failed, no valid paths')
    return run

if __name__ == '__main__':
    # Create Argument Parser
    parser = ArgumentParser(description = 'Find shortest path in maze')
    parser.add_argument('pta',default=[None],action='store',nargs=2,
        type=int,help='Define starting point')
    parser.add_argument('ptb',default=[None],action='store',nargs=2,
        type=int,help='Define finish point')
    parser.add_argument('-rand',default=[None],action='store',nargs=2,
        type=int,help='Generate random maze')
    parser.add_argument('-file',default=None,action='store',
        type=str,help='Load maze from file')
    args = parser.parse_args()

    # Validate arguments
    if (args.rand != None) and (args.file != None):
        raise TypeError('There are two maze sources defined')
    if args.rand != None:   args.source = args.rand
    elif args.file != None: args.source = args.file
    else: raise TypeError('There is no maze source defined')

    run = main(args)

    # Save path to image
    img_path = 'Path.png'
    image = run.gen_path_img(scale=4)
    image.save(img_path)

    # Show how long it took to find a path and a path length
    print('Duration:', run.duration, '\nPath length:', run.path_length)
