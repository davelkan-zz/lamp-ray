#!/usr/bin/env python

import cv2
import numpy as np
from matplotlib import pyplot as plt

#Read Image
img = cv2.imread('map.jpg')
#Edge detection
edges = cv2.Canny(img,100,200)

#these lines are for setting up corner detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('dst',img)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()