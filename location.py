#!/usr/bin/env python

import random

import los
import follow_path

vis = los.Visibility()

# Find x and y min
# Generate matrix
# check wether points are in the walls
# feed the rest to los

def x_y_min_max(walls):
    #calculate the bounds of the feasable region
    x_walls = []
    y_walls = []
    for segment in walls:
        for point in segment:
            x_walls.append(point[0])
            y_walls.append(point[1])
    return [min(x_walls)+1,max(x_walls)-1,min(y_walls)+1,max(y_walls)-1] 
    # use this line to avoid placing points on the walls
    # return [min(x_walls),max(x_walls),min(y_walls),max(y_walls)]

def matrix_gen(bounds):
    #generate a matrix of points that cover beyond the feasable region
    #bounds = [x_min, x_max, y_min, y_max]
    res = 20
    raw_points = []
    for i in range(res):
        x = bounds[0]+((bounds[1]-bounds[0])/res)*i
        for j in range(res):
            y = bounds[2]+((bounds[3]-bounds[2])/res)*j
            raw_points.append((x,y))
    #raw_matrix = [[(bounds[0]+((bounds[1]-bounds[0])/res)*i,bounds[2]+((bounds[3]-bounds[2])/res)*j) for i in range(res)] for j in range(res)]
    return raw_points

#for checking if segments intersect
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def inside_walls(walls, raw_points, start_point):
    #eliminate pooints from the matrix that are outside the walls
    feasable_points  = []
    #wall_segments = []
    #or i in range(len(walls)-2):
    #    wall_segments.append([walls[i],walls[i+1]])
    #wall_segments.append([walls[len(walls)-1],walls[0]])

    for point in raw_points:
        intersected_segments = 0
        for wall in walls:
            A = [start_point[0],start_point[1]]
            B = [point[0],point[1]]
            C = [wall[0][0],wall[0][1]]
            D = [wall[1][0],wall[1][1]]
            if intersect(A,B,C,D):
                intersected_segments += 1
        if ((intersected_segments % 2) == 0):
            feasable_points.append(point)
    return feasable_points

def get_points(start_point, walls):
    bounds = x_y_min_max(walls)
    raw_points = matrix_gen(bounds)
    feasable_points = inside_walls(walls, raw_points, start_point)
    return feasable_points

def dist_func(thing):
    path, _ = thing
    # path = [np.array(i) for i in path]
    dist = 0
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]
        dist += (a**2 + b**2)**0.5
        # dist += np.linalg.norm(a-b)
    return dist

def find_start(thing):
    path, _ = thing
    if start in path:
        return True
    return False


def main(start_point, walls):
    
    feasable_points = get_points(start_point, walls)
    vis.setup(walls)

    print "brute forcing"
    percentages = []
    for point1 in feasable_points:
        for point2 in feasable_points:
            for point3 in feasable_points:
                path = [point1, point2, point3]

                room = follow_path.follow(path, vis)
                room.merge_visible()
                percent_visable = room.percentage()
                percentages.append( (path, percent_visable) )
                room.clear()

    print "finding best"
    max_visible = max(percentages, key=lambda x: x[1])
    # best_seen = filter(lambda x: x[1]==max_visible[1],percentages) 
    best_seen = [p for p in percentages if p[1] == max_visible[1]]
    include_start = [p for p in best_seen if start_point in p[0]]
    if include_start:
        best_locations = min(include_start, key=dist_func)
    else:
        best_locations = min(best_seen, key=dist_func)
    return best_locations[0], room, vis


# pick three points -> note whether they are the same or not
# add up walls they can see -> return percentage 
# figure out distace between points -> give score based on the sum of the n-1 distances (drop the longest) between the three points

if __name__ == '__main__':
    start_point = (1.0, 1.0)

    walls = [[(0.0,0.0),(5.0,0.0)],[(5.0,0.0),(5.0,6.0)],[(5.0,6.0),(10.0,6.0)],[(10.0,6.0),(10.0,10.0)],[(10.0,10.0), (0.0,10.0)],[(0.0,10.0),(0.0,0.0)]]
    main(start_point, walls)
    # # ros setup
    # rospy.init_node('main')
    # pub_room = rospy.Publisher('room', PolygonStamped, queue_size=10)
    # rospy.sleep(1)

    # # room setup

    # # publish room
    # layout = PolygonStamped()
    # layout.header.frame_id = "map"
    # layout.polygon.points = [Point32(0,0,0), Point32(0,10,0),Point32(10,10,0),Point32(10,0,0)]
    # pub_room.publish(layout)

    # # run simulation






