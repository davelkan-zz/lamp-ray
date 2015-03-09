#!/usr/bin/env python

import cv2
import numpy as np
import math

class BallFinder:
	def __init__(self):
		self.factor = 0.5
		self.sideLength = 10 #sets the size for box scans to 10 pixels on side
		self.corners = {}
		self.tempCorners = {}
		self.finalConers = {}
		#checkedPose is used to track boxes that have been checked already
		#key is x,y of top left corner, value is 0 for nothing, 1 for wall, 2 for corner
		#walls may become corners, sideLength set box size
		self.checkedPose = {}
		self.minDist = 5
		blank_image = np.zeros((sideLength,sideLength,3), np.uint8)
		filename = 'map2.jpg'
		img = cv2.imread(filename)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		limit = [gray.size[0],gray.size[1]]
		pose = [0,0]
		gray = np.float32(gray)




	def boxScan(self):
		poseEdge = [self.pose[0]+self.sidelength,self.pose[1]+self.sidelength]

		area = sum(gray[self.pose[0]:poseEdge[0], self.pose[1]:poseEdge[1]]))
		#if some does not indicate only black, there is a wall detected.
		
		#given that a wall was detected begin search pattern!
		#search pattern starts at 0, rotates at 45 degrees intervals clockwise

		#given that no wall detected, continue scanning right until edge
		#if at edge drop a layer and keep scanning the next row



	def run(self):
		while not circuitComplete:
			boxScan()


if __name__ == '__main__':
	lf = BallFinder()
	lf.run()
