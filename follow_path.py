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



def follow(path, vis):
    room = Room(vis.segments)
    for point in path:
        current_position = point
        in_sight = vis.run(current_position)
        room.add_visible(in_sight)
    return room


def update_segment(segment, old_visable, new_visable):
    '''unfinished'''
    # *_visable: ordered list of visability start/end points
    #  v = [(s,e),(s,e)]
    pairs = old_visable + new_visable
    print pairs
    starts = [(pair[0],1) for pair in pairs]
    ends = [(pair[1], -1) for pair in pairs]
    points = starts + ends
    print points
    if segment.p1.x != segment.p2.x:
        points.sort(key=lambda p: p[0][0])
        print points
    else:
        points.sort(key=lambda p: p[0][1])
    print points
    count = 0
    final = []
    for p in points:
        print count
        print p
        count += p[1]
        if count == 1:
            final.append( p[0] )
        if count == 0:
            final[-1] = (final[-1],p[0])
    return final


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
    for v in room.visable: print v, room.visable[v]


