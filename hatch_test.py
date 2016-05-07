


import numpy as np
import cv2


pendown = False
img = np.zeros((512,512,3), np.uint8)
x = np.array([0,0])
def raisepen():
    global pendown
    pendown = False
def lowerpen():
    global pendown
    pendown = True
def move_to(xnew):
    global img
    global x
    xnew = np.rint(xnew).astype(int)
    if pendown:
        cv2.line(img,(x[1],x[0]),(xnew[1],xnew[0]),(255,0,0),5)
    x = xnew

grayimg = cv2.imread('./dogman.jpg',0)

#cv2.imshow('dogman',grayimg)
#cv2.waitKey(0)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
print grayimg.shape

scale = 20.
maxval = float(np.max(grayimg))
#cv2.line(img,(0,0),(511,511),(255,0,0),5)
print maxval
print grayimg
for i in range(grayimg.shape[0]):
    move_to( np.array([i , 0] ) * scale)
    for j in range(grayimg.shape[1]):
        raisepen()
        move_to( np.array([i , j + grayimg[i,j]/maxval] ) * scale)
        lowerpen()
        move_to( np.array([i, j+1]) * scale  )
    raisepen()

cv2.imshow('lineman',img)
cv2.imshow('dogman',grayimg)
cv2.waitKey(0)
