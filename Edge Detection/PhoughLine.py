#!/usr/bin/env python

import cv2
import numpy as np
import math

class cornerFinder:
	def __init__(self):
		self.img = cv2.imread('map2.jpg')
		gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,50,150,apertureSize = 3)
		minLineLength = 1
		maxLineGap = 1
		self.lineBox = []
		self.slopeList = [[0,0,0,0]]
		self.fullList = []
		self.lines = cv2.HoughLinesP(edges,1,np.pi/180,5,minLineLength,maxLineGap)
		self.circuitComplete = False

	def buildLineBox(self):
		for x1,y1,x2,y2 in self.lines[0]:
			if x1 != x2:
				m = (float(y1) - y2)/(x1-x2)
				if m == -0:
					m = 0
				b = x1 - m*y1
			else:
				#arbitarilly set to 9001 so it isn't undefinedS
				m = 9001
				b = 9001
			d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
			self.lineBox.append([m,b,d,0])
			cv2.line(self.img,(x1,y1),(x2,y2),(0,255,0),2)
		print "lineBox", self.lineBox
		self.filterLines()



#lines identified! Now i must check for overlaps!!!

#build the ranking
	def filterLines(self):
		for index,i in enumerate(self.lineBox):
			islope = i[0]
			intercept = i[1]

			for jindex,j in enumerate(self.slopeList):
				#print jindex
				#print "intercept difference", abs(j[1] - i[1])
				'''#to expand range modify the boundaries'''
				if abs(j[0] - i[0]) < 0.25 and  0.9 < float(j[1])/i[1] < 1.1:
					if j[2] > i[2]:
						self.fullList[jindex][2] = j[2]
						self.fullList[jindex][3] = index
					else:
						self.fullList[jindex][2] = i[2]
						self.fullList[jindex][3] = index
				elif jindex == len(self.slopeList)-1:
					i[3] = index
					self.fullList.append(i)
			#print "slopeList", slopeList
			#print "fullList", fullList
			self.slopeList = self.fullList
		print "fullList", self.fullList
		self.createList()

	def createList(self):
		#now finally extracting the given index
		finalList = []
		for index,item in enumerate(self.fullList):
			print "index", item[3]
			finalList.append(self.lines[0][item[3]])

		print "finalList", finalList
		cv2.imwrite('map5.jpg',self.img)
		self.circuitComplete = True

	def run(self):
		while not self.circuitComplete:
			self.buildLineBox()


if __name__ == '__main__':
	lf = cornerFinder()
	lf.run()
