import cv2
import random

import numpy as np
import matplotlib.pyplot as plt
import time

cam = cv2.VideoCapture(0)
s, im = cam.read() # captures image
s, im = cam.read()
time.sleep(.2)
s, im = cam.read()
gray_im = cv2.cvtColor( im, cv2.COLOR_BGR2GRAY );

edges = cv2.Canny(gray_im,100,200)

height, width = edges.shape
contours, hierarchy =  cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


target = open('out.gcode', 'w')


cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow("Test Picture", im)
cv2.waitKey()

pen_down = False


for contour in contours:
    for point in contour:
        target.write("G1 X" + str(point[0][0] * 1280 / width) + " Y" + str(point[0][1] * 720 / height) + "\n")
        if not pen_down:
            target.write("M03\n")
            pen_down = True
    target.write("M05\n")
    pen_down = False

'''
for contour in contours:
    for point in contour:
        print point[0]
    print
'''
