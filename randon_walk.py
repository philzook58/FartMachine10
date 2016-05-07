import numpy as np
import cv2


grayimg = cv2.imread('./dogman.jpg',0)
maxval = np.max(grayimg)
img = np.zeros((512,512,3), np.uint8)


def inbounds(pos):
    if pos[0] < 0:
        return False
    if pos[1] < 0:
        return False
    if pos[0] > grayimg.shape[0]:
        return False
    if pos[1] > grayimg.shape[1]:
        return False
    return True


def move_to(pos):
    #cv2.line(img,(int(x[1]),int(x[0])),(int(pos[1]),int(pos[0])),(255,0,0),1)
    cv2.circle(img,(int(pos[1]),int(pos[0])),1,(255,0,0),1)

def accept(pos):
    return inbounds(pos) and np.random.random()*maxval > grayimg[ int(pos[0]), int(pos[1])]
x = np.zeros(2)


for i in range(100000):
    angle = np.random.random()*2*np.pi
    r = 50
    pos = x + np.array([np.cos(angle), np.sin(angle)]) * r

    if accept(pos):
        move_to(pos)
        x = pos

cv2.imshow('lineman',img)
cv2.imshow('dogman',grayimg)
cv2.waitKey(0)
