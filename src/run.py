from PIL import Image
from PIL.ImageColor import getrgb as get_rgb
from src.pathfinder import PathFinder

class Run(PathFinder):
    '''Run class
    Run is an attempt to generate a path in supplied maze
    '''
    def __init__(self, maze, pta, ptb):
        '''Constructor
        Parameters:
        maze [Maze Class]
            A maze a path is to be found in
        pta [tuple]
            2-Tuple, x and y coordinate
        ptb [tuple]
            2-Tuple, x and y coordinate
        '''
        self.WALL, self.BLANK = maze.WALL, maze.BLANK
        self.maze_object = maze
        self.maze = maze.board
        self.size = maze.size
        self.pta, self.ptb = pta, ptb
        if not self.validate_points():
            raise IndexError('At least one point is outside maze boundaries')

    def __repr__(self, max_size=(50,50), show_info=True, path_char='O', wall_char='+',
        blank_char=' ', bound_char='|'):
        '''Representation string of a Run object
        Parameters:
        max_size [2-tuple of ints] ((50, 50))
            If board size exceeds this limit, repr will not be added to text
        show_info [boolean] (True)
            If set to True, there will be added general info about the object
        path_char [str]
            Character to put in cells that are in the path
        wall_char [str] ('+')
            Character to put in cells with Wall value
        blank_char [str] (' ')
            Character to put in cells with Blank value
        bound_char [str] ('|')
            Character appended to every line
        '''
        try:
            path_map = self.mark_points(self.path)
            width, height = self.size
            maxw, maxh = max_size
            text = ''
            if ((width <= maxw) or (maxw == -1)) or \
                ((height <= maxh) or (maxh == -1)):
                for board_row, path_row in zip(self.maze, path_map):
                    for board_cell, path_cell in zip(board_row, path_row):
                        if path_cell == True:
                            text += path_char
                        else:
                            if board_cell == self.WALL: text += wall_char
                            elif board_cell == self.BLANK: text += blank_char
                    text += bound_char+'\n'
            if show_info:
                text += 'Maze size: '+str(width)+' x '+str(height)+' cells\n'
                text += 'Maze source: '+str(self.maze_object.src_type.upper())+'\n'
                text += 'Path length: '+str(self.path_length)+'\n'
                text += 'Path find time: '+str(self.duration)+'\n'
        except AttributeError: # Path was not generated
            text = self.maze_object.__repr__(max_size, show_info, wall_char,
                blank_char, bound_char)
            if show_info: text += '\nPath was not generated'
        return text

    def validate_points(self):
        '''Check if both points are in maze boundaries'''
        xa, ya = self.pta
        xb, yb = self.ptb
        w, h = self.size
        if (xa >= w) or (xb >= w) or (ya >= h) or (yb >= h): return False
        return True

    def gen_path_img(self, **kwargs):
        '''Generate path image'''
        try:
            path_map = self.mark_points(self.path)
        except AttributeError: raise TypeError('Please generate a path first')
        image = self.gen_img(self.maze, path_map, **kwargs)
        return image


    def gen_img(self, background, *layers, scale=1,
        blank_color=(255,255,255), wall_color=(0,0,0)):
        '''Generate an image (PIL's Image class)
        Parameters:
        background [2D List]
            Preferably board attribute of Maze object
        layers [2D List]
            A list with booleans. Cells with True will be marked on image.
        scale [float/int] (1)
            Image can be scalled with a factor
        blank_color [3-tuple] (255,255,255)
            Color for cells where backgr. has BLANK value and no layer has True
        wall_color [3-tuple] (0,0,0)
            Color for cells where backgr. has WALL value and no layer as True
        '''
        bcgr_colors = {
            self.BLANK: blank_color,
            self.WALL: wall_color,
        }
        width, height = self.size
        image = Image.new('RGB', self.size)
        pixels = image.load()

        saturation = 40
        lightness = 50
        hue_step = int(360/(len(layers)+1))
        hue_list = [hue for hue in range(0, 361, hue_step)][1:]
        color_list = ['hsl(' + str(hue) + ', ' + str(saturation)+'%, ' +\
            str(lightness) + '%)' for hue in hue_list]

        for y in range(height):
            for x in range(width):
                pixels[x,y] = bcgr_colors[background[y][x]]
                for layer, color in zip(layers, color_list):
                    if layer[y][x]: pixels[x,y] = get_rgb(color)
        if scale != 1:
            image = image.resize((width*scale, height*scale))

        return image
