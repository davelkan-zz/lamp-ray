#!/usr/bin/env python

import cv2
import numpy as np
import math

img = cv2.imread('map2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 1
maxLineGap = 1
lineBox = []
slopeList = [[0,0,0,0]]
fullList = []
lines = cv2.HoughLinesP(edges,1,np.pi/180,5,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
	if x1 != x2:
		m = (float(y1) - y2)/(x1-float(x2))
		if m == -0:
			m = 0
	else:
		#arbitarilly set to 9001 so it isn't undefinedS
		m = 9001
	if m == 9001:
		b = 9001
	else:
		b = x1 - m*y1
	d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
	lineBox.append([m,b,d,0])
	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

#lines identified! Now i must check for overlaps!!!

print "lineBox", lineBox

#build the ranking
for index,i in enumerate(lineBox):
	islope = i[0]
	intercept = i[1]

	for jindex,j in enumerate(slopeList):
		#print jindex
		#print "intercept difference", abs(j[1] - i[1])
		'''TODO: change to intercept comparison to percentage '''
		if abs(j[0] - i[0]) < 0.25 and  abs(j[1] - i[1]) < 4:
			#print "no penis"
			if j[2] > i[2]:
				fullList[jindex][2] = j[2]
				fullList[jindex][3] = index
			else:
				fullList[jindex][2] = i[2]
				fullList[jindex][3] = index
		elif jindex == len(slopeList)-1:
			#print "penis"
			i.append(index)
			fullList.append(i)
	#print "slopeList", slopeList
	#print "fullList", fullList
	slopeList = fullList

print "fullList", fullList

#now finally extracting the given index
finalList = []
for index,item in enumerate(fullList):
	print "Penis", item[3]
	finalList.append(lines[0][item[3]])

print "finalList", finalList
	
'''
	for jinndex,j in enumerate(lineBox):



		#compare slope and y-intercept
		if math.abs(j[0] - i[0]) < 0.25 and  math.abs(j[1] - i[1]) < 4:
			#if j is bigger, give its index a point, take one from ib
			if j[2] > i[2]:
				lineBox[jindex][3]+=1
				lineBox[index][3]-=1
			#if i is bigger it gets the points!
			else:
				lineBox[index][3]+=1
				lineBox[jindex][3]-=1

#given a ranking, we need to build final box
for index,i in enumerate(lineBox):
	for jinndex,j in enumerate(lineBox):
'''


cv2.imwrite('map5.jpg',img)