from los import Point

class room():
    def __init__(self, walls = []):
        self.walls = walls
        self.floor = [] # list of valid locations


    def valid_locations(self,start):
        '''
        start: x,y location
        finds all locations that are inside the walls
        but not inside objects
        '''

    def crossed_wall(self):


    def _line_intersection(self, p1, p2, p3, p4):
        '''
        taken from line_of_sight algorithm
        '''
        s = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x))\
            / ((p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y))

        x = p1.x + s * (p2.x - p1.x)
        y = p1.y + s * (p2.y - p1.y)
        return Point(x, y)





