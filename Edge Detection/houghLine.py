#!/usr/bin/env python

import cv2
import numpy as np
import math

img = cv2.imread('map2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

#lines = cv2.HoughLines(gray,1,np.pi/180,200)
lines2 = cv2.HoughLinesP(edges,rho=1.0,theta=math.pi/180.0,threshold=1,minLineLength = 30)
'''for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('map4.jpg',img)
'''
for x1,y1,x2,y2 in lines2[0]:
	cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
cv2.imwrite('map5.jpg',img)