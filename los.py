'''
Original and description found at:
http://www.redblobgames.com/articles/visibility/

ported by hand from Haxe: 
http://www.redblobgames.com/articles/visibility/Visibility.hx

Calculates area seen from given location
'''

import math


class Block(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

class Point(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Endpoint(Point):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.begin = False
        self.segment = None
        self.angle = 0.0
        self.visualize = False

    def __str__(self):
        return "x: %f, y: %f, begin: %s, angle: %f"%(self.x,self.y,self.begin,self.angle)

class Segment():
    def __init__(self,p1,p2,d=0.0):
        self.p1 = p1
        self.p2 = p2
        self.d = d


class Visibility():
    def __init__(self):
        self.segments = []
        self.endpoints = []
        self.center = Point()
        self.open = []
        self.intersections = []
        self.triangles = []

    def add_segment(self, x1, y1, x2, y2):
        p1 = Endpoint(x1,y1)
        p2 = Endpoint(x2,y2)
        p1.visible = True

        segment = Segment(p1,p2)
        p1.segment = segment
        p2.segment = segment

        self.segments.append(segment)
        self.endpoints.append(p1)
        self.endpoints.append(p2)

    def load_map_edges(self,size,margin):
        self.add_segment(margin, margin, margin, size-margin)
        self.add_segment(margin, size-margin, size-margin, size-margin)
        self.add_segment(size-margin, size-margin, size-margin, margin)
        self.add_segment(size-margin, margin, margin, margin)

    def load_map(self, size, margin, blocks = [], walls = []):
        # walls are segments
        self.load_map_edges(size, margin)
        for block in blocks:
            x = block.x
            y = block.y
            r = block.r
            self.add_segment(x-r, y-r, x-r, y+r)
            self.add_segment(x-r, y+r, x+r, y+r)
            self.add_segment(x+r, y+r, x+r, y-r)
            self.add_segment(x+r, y-r, x-r, y-r)
        for wall in walls:
            self.add_segment(wall.p1.x, wall.p1.y, wall.p2.x, wall.p2.y);

    def set_light_location(self,x,y):
        self.center.x = x
        self.center.y = y

        for segment in self.segments:
            dx = 0.5 * (segment.p1.x + segment.p2.x) - x
            dy = 0.5 * (segment.p1.y + segment.p2.y) - y
            segment.d = dx*dx + dy*dy
            segment.p1.angle = math.atan2(segment.p1.y - y, segment.p1.x - x)
            segment.p2.angle = math.atan2(segment.p2.y - y, segment.p2.x - x)
            dAngle = segment.p2.angle - segment.p1.angle
            if dAngle <= -math.pi: dAngle += 2*math.pi
            if dAngle > math.pi: dAngle -= 2*math.pi
            segment.p1.begin = dAngle > 0.0
            segment.p2.begin = not segment.p1.begin


    def _end_point_compare(self,a, b):
        if a.angle > b.angle: return 1
        if b.angle > a.angle: return -1
        if not a.begin and b.begin: return 1
        if a.begin and not b.begin: return -1
        return 0


    def left_of(self, segment, point):
        s = segment
        p = point
        cross = (s.p2.x - s.p1.x) * (p.y - s.p1.y) \
                - (s.p2.y - s.p1.y) * (p.x - s.p1.x);
        return cross < 0

    def interpolate(self, p, q, f):
        x = p.x*(1-f) + q.x*f
        y = p.y*(1-f) + q.y*f
        return Point(x,y)

    def _segment_in_front(self, a, b, relativeTo):
        A1 = self.left_of(a, self.interpolate(b.p1, b.p2, 0.01));
        A2 = self.left_of(a, self.interpolate(b.p2, b.p1, 0.01));
        A3 = self.left_of(a, relativeTo);
        B1 = self.left_of(b, self.interpolate(a.p1, a.p2, 0.01));
        B2 = self.left_of(b, self.interpolate(a.p2, a.p1, 0.01));
        B3 = self.left_of(b, relativeTo);

        if (B1 == B2 and B2 != B3): return True;
        if (A1 == A2 and A2 == A3): return True;
        if (A1 == A2 and A2 != A3): return False;
        if (B1 == B2 and B2 == B3): return False;

        self.intersections.append([a.p1, a.p2, b.p1, b.p2])
        return False

    def _segment_compare(self, a, b):
        if self._segment_in_front(a,b,self.center): return 1
        elif self._segment_in_front(b,a,self.center): return -1
        return 0

    def sweep(self, maxAngle = 999.0):
        self.endpoints.sort(self._end_point_compare)
        del self.open[:]
        begin_angle = 0.0
        for p in self.endpoints: print p

        for run in range(2):
            for p in self.endpoints:
                closest_old = self.open[0] if self.open else None
                if p.begin: 
                    self.open.append(p.segment)                    
                else: 
                    if p.segment in self.open:
                        self.open.remove(p.segment)
                    else:
                        print "not added yet?", p.x, p.y
                self.open.sort(self._segment_compare)
                closest_new = self.open[0] if self.open else None
                if closest_old != closest_new:
                    if run == 1:
                        self.add_triangle(begin_angle, p.angle, p.segment)
                    begin_angle = p.angle

    def add_triangle(self,a1,a2,segment=None):
        p1 = self.center
        p2 = Point(self.center.x + math.cos(a1), self.center.y + math.sin(a1))
        p3 = Point(segment.p1.x, segment.p1.y)
        p4 = Point(segment.p2.x, segment.p2.y)

        pBegin = self.line_intersection(p3, p4, p1, p2);
        p2.x = self.center.x + math.cos(a2);
        p2.y = self.center.y + math.sin(a2);
        pEnd = self.line_intersection(p3, p4, p1, p2);

        self.triangles.append(pBegin);
        self.triangles.append(pEnd);

    def line_intersection(self, p1, p2, p3, p4):
        s = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x))\
            / ((p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y))

        x = p1.x + s * (p2.x - p1.x)
        y = p1.y + s * (p2.y - p1.y)
        return Point(x, y)

if __name__ == "__main__":
    vis = Visibility()
    walls = [Segment(Point(5,0), Point(5,5))]
    vis.load_map(10, 1, walls=walls)
    vis.set_light_location(3,3)
    vis.sweep()
    print [(p.x,p.y) for p in vis.triangles]


