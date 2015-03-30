import los

vis = los.Visibility()

def x_y_min_max(walls):
	#calculate the bounds of the feasable region
	x_walls = []
	y_walls = []
	for point in walls:
		x_walls.append(point[0])
		y_walls.append(point[1])
	return [min(x_walls),max(x_walls),min(y_walls),max(y_walls)]

def matrix_gen(bounds):
	#generate a matrix of points that cover beyond the feasable region
	#bounds = [x_min, x_max, y_min, y_max]
	res = 10
	raw_matrix = [[(bounds[0]+((bounds[1]-bounds[0])/res)*i,bounds[2]+((bounds[3]-bounds[2])/res)*j) for i in range(res)] for j in range(res)]
	return raw_matrix

walls = [(0.0,0.0),(5.0,0.0),(5.0,6.0),(10.0,6.0),(10.0,10.0),(0.0,10.0)]
bounds = x_y_min_max(walls)
print bounds
raw_matrix = matrix_gen(bounds)


# Find x and y min
# Generate matrix
# check wether points are in the walls
# feed the rest to los

#vis.setup(walls)
#while running:
#    current_position = (3,3)
#    walls_seen = vis.run(current_position)
#    print walls_seen




