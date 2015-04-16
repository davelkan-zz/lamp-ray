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
    #return [min(x_walls)+.1,max(x_walls)-.1,min(y_walls)+.1,max(y_walls)-.1] use this line to avoid placing points on the walls
    return [min(x_walls),max(x_walls),min(y_walls),max(y_walls)]

def matrix_gen(bounds):
    #generate a matrix of points that cover beyond the feasable region
    #bounds = [x_min, x_max, y_min, y_max]
    res = 30
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




start_point = (1.0, 1.0)

walls = [[(0.0,0.0),(5.0,0.0)],[(5.0,0.0),(5.0,6.0)],[(5.0,6.0),(10.0,6.0)],[(10.0,6.0),(10.0,10.0)],[(10.0,10.0), (0.0,10.0)],[(0.0,10.0),(0.0,0.0)]]
bounds = x_y_min_max(walls)
raw_points = matrix_gen(bounds)
feasable_points = inside_walls(walls, raw_points, start_point)
vis.setup(walls)

sights = {}
for position in feasable_points:
    sights[position] = vis.run(position)

percentages = []

path = [0]*2
for point1 in feasable_points:
    path[0] = point1
    for point2 in feasable_points:
        path[1] = point2

        room = follow_path.follow(path, vis)
        # room contains a dictionary mapping from wall segments to the portions of it we have seen
        room.merge_visible()
        percentages.append( (path, room.percentage()) )
def min_func(thing):
    path, _ = thing
    a,b = path[0],path[1]
    dist = ( (a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
    return dist
def full_coverage(thing):
    _, perc = thing
    return perc == 1.0

print min(filter(full_coverage,percentages),key=min_func)


# pick three points -> note whether they are the same or not
# add up walls they can see -> return percentage 
# figure out distace between points -> give score based on the sum of the n-1 distances (drop the longest) between the three points






