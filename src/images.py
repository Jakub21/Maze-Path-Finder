'''Jakub21
May 2018
MIT License
Python 3.6
--------------------------------
Images related functions
'''



################################
from PIL import Image as ImageClass
from PIL.ImageColor import getrgb as GetRGB
from os.path import isfile
import imageio
import logging
Log = logging.getLogger('MainLogger')



################################
def InitGlobals(Size, PtA, PtB, Values):
    '''images.InitGlobals [Size] [PtA] [PtB] [Values]
    Creates global variables that contain data from parameters.
    Function must be called before any other in this file
    --------------------------------
    Parameters
    - Size                  | Size of a maze to generate (2-tpl.: width, height)
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
def GetSize(FileName):
    '''images.GetSize [FileName]
    Reads size of image
    --------------------------------
    Parateters
    - FileName              | Name of file to load data from
    --------------------------------
    Returns
    - Size                  | 2-tuple: width, height
    '''
    Image = ImageClass.open(FileName)
    return Image.size



################################
def GetMazeImg(FileName):
    '''images.GetMazeImg [FileName]
    Loads image and converts is to a 2D list.
    Black pixels are mapped to walls and white to empty points.
    No support for 32-bit images (color is a 3-tuple, no alpha chanel)
    Pixels that are not black neither white are mapped to empty points.
    --------------------------------
    Parateters
    - FileName              | Name of file to load data from
    --------------------------------
    Returns
    - Maze                  | 2D list only with values matching WALL and BLANK
    '''
    Log.info('Loading maze')
    width, height = SIZE
    Image = ImageClass.open(FileName)
    pixels = Image.load()
    Result = [[True for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            if pixels[x,y] == (0,0,0): Result[y][x] = False
    return Result



################################
def GenerateImage(Background, *Layers, Scale=1, MarkOrigPoints=True,
        BlankColor=(255,255,255), WallColor=(0,0,0)):
    '''images.GenerateImage [Background] {*Layers} {Scale} {MarkOrigPoints}
        {BlankColor} {WallColor}
    Generates an image from multiple 2D lists.
    In other layers, in cells with value 'False' pixel is not changed
    and in cells with value 'True',
    pixel is changed to color based on layer index.
    --------------------------------
    Parameters
    - Background            | 2D list only with values matching WALL and BLANK
    - *Layers               | 2D list only with booleans.
    - Scale                 | Image scaling factor, default is 1 (int)
    - BlankColor            | [Optnl.] Color for cells with BLANK (3-tuple:RGB)
    - WallColor             | [Optional] Color for cells with WALL (3-tuple:RGB)
    --------------------------------
    Returns
    - Image                 | Object of PIL.Image class
    '''
    color_map = {
        WALL: WallColor,
        BLANK: BlankColor,
    }
    width, height = SIZE
    Image = ImageClass.new('RGB', SIZE)
    pixels = Image.load()

    sat = 40
    lum = 50
    hue_step = int(360/(len(Layers)+1))
    hue_list = [i for i in range(0,361,hue_step)][1:]
    hsl_list = ['hsl('+str(hue)+', '+str(sat)+'%, '+str(lum)+'%)'
        for hue in hue_list]

    for y in range(height):
        for x in range(width):
            pixels[x,y] = color_map[Background[y][x]]
            for layer, hsl in zip(Layers, hsl_list):
                if layer[y][x]: pixels[x,y] = GetRGB(hsl)

    if Scale != 1:
        Scale = int(Scale)
        Image = Image.resize((width*Scale, height*Scale))

    return Image



################################
def MakeGif(baseName, DirName='data'):
    '''images.MakeGif [?]
    Create a GIF
    --------------------------------
    TODO
    '''
    Log.info('Generating GIF')
    filename = ''
    nameIndex = 0
    while isfile(filename) or filename=='':
        nameIndex += 1
        filename = 'gifs/Animation'+str(nameIndex)+'.gif'
    with imageio.get_writer(filename, mode='I') as writer:
        for index in range(1,int(5e2)):
            filename = baseName+str(index)+'.png'
            try:
                image = imageio.imread(DirName+'/'+filename)
                writer.append_data(image)
            except: pass
