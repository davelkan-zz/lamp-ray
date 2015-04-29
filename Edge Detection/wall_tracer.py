#!/usr/bin/env python
'''
code by David Elkan
updated 4/28/2015

Code scans an blueprint image and outputs lines representing the walls in [[x1,y1],[x2,y2]}
'''




import cv2
import math
import numpy as np

w = 700
h = 700

class cornerFinder:
	def __init__(self):
		self.img = cv2.imread('hospitalhiresblack.jpg')
		self.img2 = self.img.astype(np.uint8)

		self.lines = []
		self.line_list= []

		self.hor_points = []
		self.ver_points = []


		self.hor_lines = []
		self.ver_lines = []


	def scanImage(self):
		for i in range(0,w):
			for j in range(0,h):
				if (self.img2[j][i] == [0,0,0]).all():
					self.hor_points.append([i,j])
				if (self.img2[i][j] == [0,0,0]).all():
					self.ver_points.append([i,j])

	def buildLines(self,points,id):
		current = [points[0]]
		for index,point in enumerate(points):
		    if index > 0:
			    if point[0] == points[index-1][0] and abs(point[1] - points[index-1][1]) < 5:
			    	if len(current) == 1:
			            current.append(point)
			        elif len(current) == 2:
			            current[1] = point
			    else:
			    	#print False
			        if len(current) == 2:
						if id == 0:
							self.ver_lines.append(current)
						elif id == 1:
							self.hor_lines.append(current)
			        current = [point]
		if len(current) == 2:
			if id == 0:
				self.ver_lines.append(current)
			elif id == 1:
				self.hor_lines.append(current)
		if id == 0:
			for index,segment in enumerate(self.ver_lines):
				self.ver_lines[index][0] = segment[0][::-1]
				self.ver_lines[index][1] = segment[1][::-1]

	def mergeCorners(self):
		#print "horizontal lines: ",self.hor_lines
		#print "vertical lines: ", self.ver_lines
		for index,segment in enumerate(self.hor_lines):
			for index2,segment2 in enumerate(self.ver_lines):
				if segment[0] not in segment2 and segment[1] not in segment2:
					#print segment[0][0]
					#dist1 compares first point in segment with first point of segment2
					dist1 = math.sqrt((segment[0][0]-segment2[0][0])**2 + (segment[0][1]-segment2[0][1])**2)
					#dist2 compares first point in segment with second point of segment2
					dist2 = math.sqrt((segment[0][0]-segment2[1][0])**2 + (segment[0][1]-segment2[1][1])**2)
					#dist3 compares second point in segment with first point of segment2
					dist3 = math.sqrt((segment[1][0]-segment2[0][0])**2 + (segment[1][1]-segment2[0][1])**2)
					#dist4 compares second point in segment with second point of segment2
					dist4 = math.sqrt((segment[1][0]-segment2[1][0])**2 + (segment[1][1]-segment2[1][1])**2)
					#values in index_chart represent [horizontal,vertical]
					index_chart = [[0,0],[0,1],[1,0],[1,1]]
					dist_list = [dist1,dist2,dist3,dist4]
					for index3,distance in enumerate(dist_list):
						if 0 < distance < 5:
							#print "changed"
							#merge corners of these two points: hor_lines[index][index_chart[index3][0]] and ver_lines[index2][index_chart[index3][0]]
							intercept = [segment[index_chart[index3][0]][0],segment2[index_chart[index3][1]][1]]
							#print intercept
							#print "ver_value: ",self.ver_lines[index2][index_chart[index3][0]]
							#print "hor_value: ",self.hor_lines[index][index_chart[index3][0]]
							self.ver_lines[index2][index_chart[index3][1]] = intercept
							self.hor_lines[index][index_chart[index3][0]] = intercept
				
		self.lines = self.hor_lines+self.ver_lines

	def printMap(self):
		for segment in self.lines:
			self.line_list.append([(segment[0][0],segment[0][1]),(segment[1][0],segment[1][1])])
			cv2.line(self.img,(segment[0][0],segment[0][1]),(segment[1][0],segment[1][1]),(0,0,0),1)
			cv2.imwrite('testblack2.jpg',self.img)
		return self.line_list

	def sortLines(self,lines):
		sort_lines = [lines[0]]
		while len(sort_lines) < len(lines):
			for item in lines:
				i = len(sort_lines)
				if item[0] == sort_lines[i-1][1]:
					sort_lines.append(item)
				elif item[1] == sort_lines[i-1][1] and item[0] != sort_lines[i-1][0]:
					sort_lines.append(item[::-1])
		return sort_lines

	def run(self):
		self.scanImage()
		self.buildLines(self.ver_points,0)
		self.buildLines(self.hor_points,1)
		self.mergeCorners()
		#the final list of lines is set to final lines.
		final_lines = self.printMap()
		final_lines = self.sortLines(final_lines)
		return final_lines

if __name__ == '__main__':
	lf = cornerFinder()
	lf.run()