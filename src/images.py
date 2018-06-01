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
def GenerateImage(Background, *Layers, Scale=1, MarkOrigPoints=True, BlankColor=(255,255,255), WallColor=(0,0,0)):
    '''images.GenerateImage [Background] {*Layers} {Scale} {MarkOrigPoints} {BlankColor} {WallColor}
    Generates an image from multiple 2D lists.
    In other layers, in cells with value 'False' pixel is not changed
    and in cells with value 'True' pixel is changed to color based on layer index.
    --------------------------------
    Parameters
    - Background            | 2D list only with values matching globals WALL and BLANK
    - *Layers               | 2D list only with booleans.
    - Scale                 | Image scaling factor, default is 1 (int)
    - BlankColor            | [Optional] Color for cells with BLANK (3-tuple:RGB)
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

    for y in range(height):
        for x in range(width):
            try: pixels[x,y] = color_map[Background[y][x]]
            except: pixels[x,y] = (255,0,0)

    hue_step = int(360/(len(Layers)+1))
    hue_list = [i for i in range(0,361,hue_step)][1:]

    for layer, hue in zip(Layers, hue_list):
        hsl = 'hsl('+str(hue)+', '+str(sat)+'%, '+str(lum)+'%)'
        for y in range(height):
            for x in range(width):
                if layer[y][x]: pixels[x,y] = GetRGB(hsl)

    if Scale != 1:
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
