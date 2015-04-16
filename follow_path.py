import los


class Room():
    def __init__(self,segments):
        self.segments = segments
        self.visable = {}
        for s in segments:
            self.visable[s] = []

    def add_visible(self,new_views):
        # new_views = [(p1,p2, s), ... ]
        for p1,p2,seg in new_views:
            view_range = (p1,p2)
            self.visable[seg].append(view_range)

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


def follow(path, vis):
    room = Room(vis.segments)
    for point in path:
        current_position = point
        in_sight = vis.run(current_position)
        room.add_visible(in_sight)
    return room


if __name__ == '__main__':
    path = [(1.0,1.0),(5.0,1.0),(9.0,1.0)]
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
    room.merge_visible()
    # for v in room.visable: print v, room.visable[v]
    room.percentage()



