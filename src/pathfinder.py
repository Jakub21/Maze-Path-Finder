from datetime import datetime
from math import sqrt

class PathFinder:
    '''PathFinder class
    Function set inherited by Run class
    Used to find paths in maze
    '''

    def get_time(self):
        return datetime.now()

    def make_2d_list(self, size, fill):
        width, height = size
        return [[fill for x in range(width)] for y in range(height)]

    def mark_points(self, list_of_points):
        width, height = self.size
        result = self.make_2d_list(self.size, fill=False)
        for point in list_of_points:
            x, y = point
            result[y][x] = True
        return result

    def check_dist(self, pta, ptb):
        xa, ya = pta
        xb, yb = ptb
        return sqrt( (xa-xb)**2 + (ya-yb)**2 )

    def step_direction(self, pta, ptb):
        xa, ya = pta
        xb, yb = ptb
        if xa == xb:
            if ya == yb: return 'None'
            if ya > yb: return 'Up'
            if ya < yb: return 'Down'
        else:
            if ya != yb: return 'Complex'
            if xa > xb: return 'Left'
            if xa < xb: return 'Right'
        raise TypeError('Undefined direction'+str(pta)+', '+str(ptb))

    def add_step(self, inrange):
        width, height = self.size
        W, B = self.WALL, self.BLANK
        result = self.make_2d_list(self.size, fill=False)
        for y in range(height):
            for x in range(width):
                if self.maze[y][x] == W: continue
                top, bottom, left, right = [W]*4
                if y-1 > 0: top = inrange[y-1][x]
                if y+1 < height: bottom = inrange[y+1][x]
                if x-1 > 0: left = inrange[y][x-1]
                if x+1 < width: right = inrange[y][x+1]
                if True in (inrange[y][x], top, bottom, left, right):
                    result[y][x] = True
        return result

    def get_mid_point(self, pta, ptb):
        width, height = self.size
        inrange_a = self.make_2d_list(self.size, fill=False)
        inrange_b = self.make_2d_list(self.size, fill=False)
        inrange_a[pta[1]][pta[0]] = True
        inrange_b[ptb[1]][ptb[0]] = True
        match = ()
        while match == ():
            oldrange_a, oldrange_b = inrange_a, inrange_b
            inrange_a = self.add_step(inrange_a)
            inrange_b = self.add_step(inrange_b)
            if (oldrange_a == inrange_a) or (oldrange_b == inrange_b):
                return # No valid path exists
            for y in range(height):
                for x in range(width):
                    if inrange_a[y][x] and inrange_b[y][x]:
                        match = (x,y)
        return match

    def find_path(self):
        start_time = self.get_time()
        current = self.pta
        path = []
        while current != self.ptb:
            midpoint = self.ptb
            u = 0
            while self.check_dist(current, midpoint) > 1:
                u += 1
                midpoint = self.get_mid_point(current, midpoint)
                if midpoint == None:
                    raise ValueError('There are no valid paths')
            path += [current]
            current = midpoint
        end_time = self.get_time()
        self.duration = end_time - start_time
        self.path_length = len(path)
        self.path = path
        return path
