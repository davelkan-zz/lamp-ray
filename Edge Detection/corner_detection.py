#!/usr/bin/env python

import cv2
import numpy as np
import math


factor = 0.5
corners = {}
temp_corners = {}
final_corners = {}
min_dist = 5
sideLength = 10
blank_image = np.zeros((sideLength,sideLength,3), np.uint8)

filename = 'map2.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

limitX = gray.size[0]
limitY = gray.size[1]

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,3,3,0.1)
maxima = dst.max()

for (x,y), value in np.ndenumerate(dst):
	if value > factor*maxima:
		index_tuple = (x,y)
		corners[index_tuple] = value


for index, value in corners.iteritems():
	prev_index = index
	prev_value = value
	temp_corners = {prev_index:prev_value}
	for index, value in corners.iteritems():
		x_dist = math.fabs(prev_index[0] - index[0])
		y_dist = math.fabs(prev_index[1] - index[1])
		if x_dist < min_dist and y_dist < min_dist:
			temp_corners[index] = value

		#distance = math.sqrt(prev_index[0]-index)
	sum_x = 0
	sum_y = 0
	sum_value = 0
	for index,value in temp_corners.iteritems():
		sum_x += index[0]
		sum_y += index[1]
		sum_value += value
	avg_x = sum_x/len(temp_corners)
	avg_y = sum_y/len(temp_corners)
	avg_value = sum_value/len(temp_corners)
	final_corners[(avg_x,avg_y)] = avg_value

print final_corners


'''
Start in top left corner, perform bitwiseand or just 
 of that and the blank_image


'''


#define maximum range for scan
maxRange = sideLength/5

for i in xrange(0,maxRange):
	j = i+1
	if sum(gray[sideLength*i:sideLength*j,sideLength*i:sideLength*j]) > 
	




'''
#check each direction around corner to find direction of line
for prev_index,prev_value in final_corners.iteritems():
	temp_corners = {}
	#to the right
	if gray[prev_index[0],prev_value[0]+min_dist] < 10:
		zero = 9001
		champion = None
		for index,value in final_corners.iteritems():
			if math.abs(prev_index[0] - index[0]) < min_dist:
				temp_corners[prev_index] = index
		for temp_index,temp_value in temp_corners.iteritems():
			if prev_index[1] -temp_index[1] < zero:
				zero = prev_index[1] -temp_index[1]
				champion = temp_index
		if champion:



	#to the left
	if gray[prev_index[0],prev_value[0]+min_dist] < 10:
		zero = 9001
		champion = None
	#North
	if gray[prev_index[0],prev_value[0]+min_dist] < 10:
		zero = 9001
		champion = None
	#South
	if gray[prev_index[0],prev_value[0]+min_dist] < 10:
		zero = 9001
		champion = None
	
	temp_corners = {}
		for index, value in corners.iteritems():
			x_dist = math.fabs(prev_index[0] - index[0])
			y_dist = math.fabs(prev_index[1] - index[1])
			if x_dist < min_dist != y_dist < min_dist:
				temp_corners[index] = value
		for new_index,new_value in temp_corners.iteritems():
			if prev_index 
'''



#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>factor*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()