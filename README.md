# Maze-Path-Finder
Program generates a maze and finds the shortest path between two points.
An image with a path drawn is saved to `Path.png`.

#### Arguments
Positional arguments:
- start point X (int),
- start point Y (int),
- finish point X (int),
- finish point Y (int),

Define maze source:
- `-rand [width: int] [height: int]` Create random maze,
- `-file [path: str]` Load maze from image,

Both start and finish points should fit in maze boundaries.

Program will not start with no (or both) maze sources defined.

#### Maze source images
Maze source images are parsed with PIL package. Black pixels in image (Tuples
of length 3 or 4 that contain only zeros) are mapped to walls in maze. Pixels
of other colors are mapped to blank cells.
