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
    def __str__(self):
        return "x: %.2f, y: %.2f"%(self.x,self.y)

class Endpoint(Point):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.begin = False
        self.segment = None
        self.angle = 0.0
        self.visualize = False

    def __str__(self):
        return "x: %f, y: %f, begin: %s, angle: %f"%(self.x,self.y,self.begin,math.degrees(self.angle))

class Segment():
    def __init__(self,p1,p2,d=0.0):
        self.p1 = p1
        self.p2 = p2
        self.d = d
    def __str__(self):
        return "p1: %s\np2: %s"%(self.p1,self.p2)


class Visibility():
    def __init__(self):
        self.segments = []
        self.endpoints = []
        self.center = Point()
        self.open = []
        # self.intersections = []
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
        # self.load_map_edges(size, margin)
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

        # self.intersections.append([a.p1, a.p2, b.p1, b.p2])
        return False

    def _endpoint_compare(self,a, b):
        if a.angle > b.angle: return 1
        if b.angle > a.angle: return -1
        if not a.begin and b.begin: return 1
        if a.begin and not b.begin: return -1
        # if self._segment_in_front(a.segment,b.segment,self.center): return 1
        # if self._segment_in_front(b.segment,a.segment,self.center): return -1
        return 0

    def _segment_compare(self, a, b):
        if self._segment_in_front(a,b,self.center): return 1
        elif self._segment_in_front(b,a,self.center): return -1
        # if a.d > b.d: return -1
        # if a.d < b.d: return 1
        return 0

    def sweep(self, maxAngle = 999.0):
        self.endpoints.sort(self._endpoint_compare)

        del self.open[:]
        begin_angle = 0.0

        for run in range(2):
            for p in self.endpoints:
                closest_old = self.open[0] if self.open else None
                if p.begin: 
                    self.open.append(p.segment)                    
                else: 
                    if p.segment in self.open:
                        self.open.remove(p.segment)
                self.open.sort(self._segment_compare)
                closest_new = self.open[0] if self.open else None
                if closest_old != closest_new and begin_angle != p.angle:
                    if run == 1:
                        self.add_triangle(begin_angle, p.angle, closest_old)
                    begin_angle = p.angle


    def add_triangle(self,angle1,angle2,segment):
        a1 = self.center
        a2 = Point(self.center.x + math.cos(angle1), self.center.y + math.sin(angle1))
        b1 = Point(segment.p1.x, segment.p1.y)
        b2 = Point(segment.p2.x, segment.p2.y)

        pBegin = self.line_intersection(b1, b2, a1, a2);
        a2.x = self.center.x + math.cos(angle2)
        a2.y = self.center.y + math.sin(angle2)
        pEnd = self.line_intersection(b1, b2, a1, a2);

        self.triangles.append((pBegin,pEnd))
        # self.triangles.append(pEnd);

    def line_intersection(self, p1, p2, p3, p4):
        s = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x))\
            / ((p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y))

        x = p1.x + s * (p2.x - p1.x)
        y = p1.y + s * (p2.y - p1.y)
        return Point(x, y)

    def setup(self,wall_points):
        walls = []
        i = 0
        while i+1 < len(wall_points):
            p1,p2 = wall_points[i],wall_points[i+1]
            s = Segment(Point(*p1),Point(*p2))
            walls.append(s)
            i+=1
        p1,p2 = wall_points[-1],wall_points[0]
        walls.append(Segment(Point(*p1),Point(*p2)))

        self.load_map(10,0,walls=walls)

    def run(self,location):
        self.set_light_location(*location)
        self.sweep()
        seen = []
        for p1,p2 in self.triangles:
            seen.append(((p1.x, p1.y),(p2.x,p2.y)))
        return seen

if __name__ == "__main__":
    vis = Visibility()
    complex_walls = [Segment(Point(0.0,0.0), Point(15.0,0.0)),
                     Segment(Point(15.0,0.0), Point(15.0,10.0)),
                     Segment(Point(15.0,10.0), Point(11.0,10.0)),
                     Segment(Point(11.0,10.0), Point(11.0,8.0)),
                     Segment(Point(11.0,8.0), Point(7.0,8.0)),
                     Segment(Point(7.0,8.0), Point(7.0,10.0)),
                     Segment(Point(7.0,10.0), Point(2.0,10.0)),
                     Segment(Point(2.0,10.0), Point(2.0,2.0)),
                     Segment(Point(2.0,2.0), Point(0.0,2.0)),
                     Segment(Point(0.0,2.0), Point(0.0,0.0))]
    simple_walls = [Segment(Point(0.0,0.0), Point(5.0,0.0)),
                    Segment(Point(5.0,0.0), Point(5.0,6.0)),
                    Segment(Point(5.0,6.0), Point(10.0,6.0)),
                    Segment(Point(10.0,6.0), Point(10.0,10.0)),
                    Segment(Point(10.0,10.0), Point(0.0,10.0)),
                    Segment(Point(0.0,10.0), Point(0.0,0.0))]
    square_walls = [Segment(Point(0.0,0.0), Point(0.0,10.0)),
                    Segment(Point(0.0,10.0), Point(10.0,10.0)),
                    Segment(Point(10.0,10.0), Point(10.0,0.0)),
                    Segment(Point(10.0,0.0), Point(0.0,0.0))]
    vis.load_map(10, 0,walls=simple_walls)
    vis.set_light_location(3.0,5.9)
    vis.sweep()

    print "result"
    for p1,p2 in vis.triangles: print p1,"\t", p2

