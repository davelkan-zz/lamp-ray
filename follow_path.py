from copy import deepcopy
import los
import datetime


class Room():
    def __init__(self,segments):
        self.segments = segments
        self.visable = {}
        for seg in segments:
            self.visable[seg] = []

    def clear(self):
        self.visable = {}
        for s in self.segments:
            self.visable[s] = []
        self.merge_visible()
        # print self.visable


    def get_walls(self):
        walls = []
        for seg in self.segments:
            p  = seg.p1.x, seg.p1.y
            walls.append( p )
        return walls

    def get_merged(self):
        self.merge_visible()
        merged = []
        for seg in self.visable:
            for view in self.visable[seg]:
                merged.append(view)
        return merged


    def add_visible(self,new_views):
        # new_views = [(p1,p2, s), ... ]
        visable = []
        for p1,p2,seg in new_views:
            view_range = (p1,p2)
            self.visable[seg].append(view_range)
            visable.append(view_range)
        return visable

    def percentage(self):
        full_dist = 0
        seen_dist = 0
        for segment in self.visable:
            seg_a,seg_b = segment.p1, segment.p2
            seg_dist = ( (seg_a.x - seg_b.x)**2+(seg_a.y-seg_b.y)**2 )**0.5
            full_dist += seg_dist
            seeing = self.visable[segment]
            for view in seeing:
                a,b = view
                dist = ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
                seen_dist += dist
        return seen_dist/full_dist

    def merge_visible(self):
        for segment in self.visable:
            viewable = self.visable[segment]
            merged = []
            for view in viewable:
                a,b = view
                if a[0] < b[0]:
                    merged.append((a,b))
                elif a[0] > b[0]:
                    merged.append((b,a))
                elif a[1] < b[1]:
                    merged.append((a,b))
                else:
                    merged.append((b,a))
            merged.sort()
            i = 0
            while i < len(merged)-1:
                a = merged[i]
                b = merged[i+1]
                if a[1][0] > b[0][0] or a[1][0] == b[0][0] and a[1][1] > b[0][1]:
                    new = (a[0], b[1])
                    merged.remove(a)
                    merged.remove(b)
                    merged.insert(i,new)
                else:
                    i+=1
            self.visable[segment] = merged

    def extend_path(self, point, vis):
        current_position = point
        in_sight = vis.run(current_position)
        visable =  self.add_visible(in_sight)
        self.merge_visible
        return visable



def follow(path, vis):
    room = Room(vis.segments)
    for point in path:
        current_position = point
        in_sight = vis.run(current_position)
        room.add_visible(in_sight)
    return room


if __name__ == '__main__':
    path = [(1.0,1.0),(5.0,1.0),(9.0,1.0)]
    # path = [(1.0,1.0),(1.0,1.0)]
    walls = [[(0.0,0.0),(10.0,0.0)],
            [(10.0,0.0),(10.0,10.0)],
            [(10.0,10.0),(0.0,10.0)],
            [(0.0,10.0),(0.0,0.0)],
            [(4.0,4.0),(4.0,6.0)],
            [(4.0,6.0),(6.0,6.0)],
            [(6.0,6.0),(6.0,4.0)],
            [(6.0,4.0),(4.0,4.0)]]
    vis = los.Visibility()
    vis.setup(walls)

    room = follow(path,vis)
    # for v in room.visable: print v, room.visable[v]
    room.merge_visible()
    print room.percentage()



