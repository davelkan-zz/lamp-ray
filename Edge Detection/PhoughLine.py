#!/usr/bin/env python

import cv2
import numpy as np
import math

class cornerFinder:
	def __init__(self):
		self.img = cv2.imread('box.jpg')
		gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,50,150,apertureSize = 3)
		self.minLineLength = 4
		self.maxLineGap = 1
		self.lineBox = []
		self.longLines = []
		self.slopeList = [[0,0,0,0]]
		self.fullList = []
		self.filterList = []
		self.sameList = []
		self.lines = cv2.HoughLinesP(edges,1,np.pi/180,5,self.minLineLength,self.maxLineGap)
		self.circuitComplete = False
		print "self.lines", self.lines

	''''buildLineBox works with no known bugs.
		outputs lineBox, an array where each element
		is a list representing each found line:
		[slope, y or x intercept, length, 0]

	'''
	def buildLineBox(self):
		for x1,y1,x2,y2 in self.lines[0]:
			d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
			'''start by filtering out very short lines'''
			if d > self.minLineLength:
				self.longLines.append([x1,y1,x2,y2])
				if x1 != x2:
					m = (float(y1) - y2)/(x1-x2)
					if m == -0:
						m = 0
					b = x1 - m*y1
				else:
					#arbitarilly set m 9001 so it isn't undefined, and set b to x-intercept
					m = 9001
					b = x1
				self.lineBox.append([m,b,d,0])
			#cv2.line(self.img,(x1,y1),(x2,y2),(0,255,0),2)
		print "longLines(42)", self.longLines
		#print "linBox Size(36)", len(self.lineBox)
		#cv2.imwrite('map5.jpg',self.img)
		self.compareLines()


	#filterList [[index1,index2,x1_comparison,y1_comparison,21_comparison,y2_comparison],[index1,index2,x1_comparison,y1_comparison,x2_comparison,y2_comparison]...]
	def compareLines(self):
		for index,item in enumerate(self.longLines):
			for index2,item2 in enumerate(self.longLines):
				if index < index2:
					same = [index,index2]
					for index3,value in enumerate(item):
						#they are the same line
						if abs(value - item2[index3]) < 6:
							same.append(True)

						#they are not the same line
						else:
							same.append(False)
					if False not in same:
						self.sameList.append([index,index2])
					self.filterList.append(same)
		#print self.filterList
		print self.sameList
		self.filterLines()

	def filterLines(self):
		pairedIndex = []
		for index,element in enumerate(self.sameList):
			pairedIndex.append(self.sameList[index][0])
			pairedIndex.append(self.sameList[index][1])
			if self.lineBox[element[0]] > self.lineBox[element[1]]:
				self.fullList.append(self.longLines[element[0]])
			else:
				self.fullList.append(self.longLines[element[1]])
		print "pairedIndex",pairedIndex
		for i in range(len(self.longLines)):
			if i not in pairedIndex:
				self.fullList.append(self.longLines[i])
		print "self.fullList",self.fullList
		self.circuitComplete = True

	def run(self):
		while not self.circuitComplete:
			self.buildLineBox()


if __name__ == '__main__':
	lf = cornerFinder()
	lf.run()
