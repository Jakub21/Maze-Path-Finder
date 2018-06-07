'''Jakub21
May 2018
MIT License
Python 3.6
--------------------------------
Maze generator
Generates a maze that consists of 3x3 chunks
'''



################################
from random import randrange
from math import ceil
import logging
Log = logging.getLogger('MainLogger')



################################
def InitGlobals(Size, PtA, PtB, Values):
    '''maze.InitGlobals [Size] [PtA] [PtB] [Values]
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
def GenerateChunk(Variant):
    '''maze.GenerateChunk [Variant]
    Generate 3x3 chunk, basing on seed
    --------------------------------
    Parameters
    - Variant               | Chunk variant (int: min=0, max=10)
    --------------------------------
    Returns
    - Chunk                 | Chunk, 2D list (3x3)
    '''
    W, B = WALL, BLANK
    if   Variant == 0 : return[[B,B,B],[W,W,W],[B,B,B]]
    elif Variant == 1 : return[[B,W,B],[B,W,B],[B,W,B]]
    elif Variant == 2 : return[[B,W,B],[W,W,B],[B,B,B]]
    elif Variant == 3 : return[[B,W,B],[B,W,W],[B,B,B]]
    elif Variant == 4 : return[[B,B,B],[W,W,B],[B,W,B]]
    elif Variant == 5 : return[[B,B,B],[B,W,W],[B,W,B]]
    elif Variant == 6 : return[[B,B,B],[W,W,W],[B,W,B]]
    elif Variant == 7 : return[[B,W,B],[W,W,W],[B,B,B]]
    elif Variant == 8 : return[[B,W,B],[B,W,W],[B,W,B]]
    elif Variant == 9 : return[[B,W,B],[W,W,B],[B,W,B]]
    elif Variant == 10: return[[B,W,B],[W,W,W],[B,W,B]]



################################
def GetMaze():
    '''maze.GetMaze
    Generates maze. Merges chunks in random order
    --------------------------------
    No parameters
    --------------------------------
    Returns
    - Maze                  | 2D list only with values matching WALL and BLANK
    '''
    Log.info('Generating maze')
    width, height = [el+1 for el in SIZE]
    num_of_chunks = ceil(width * height /9)
    max_chunk_id = 10

    id_list = []
    while len(id_list)<num_of_chunks: id_list.append(randrange(max_chunk_id+1))
    id_list = [ id_list[x:x+ceil(width/3)]
        for x in range(0, len(id_list), (width//3))]
    chunks = {id:GenerateChunk(id) for id in range(max_chunk_id+1)}

    Result = []
    for id_row in id_list:
        for row_index in range(3):
            row = []
            for id in id_row: row += chunks[id][row_index]
            row = row[:width]
            Result.append(row)
    Result = Result[:height]
    Result[PTA[1]][PTA[0]] = BLANK
    Result[PTB[1]][PTB[0]] = BLANK
    return Result
