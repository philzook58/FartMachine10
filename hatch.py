


import numpy as np
import cv2


import sys
import serial
port =  '/dev/cu.wch ch341 USB=>RS232 1410'#'tty.wch'#'cu.wch ch341 USB=>RS232 1410'
ser = serial.Serial(port,38400)  # open serial port
print(ser.name)         # check which port was really used
import numpy as np
import time


def raisepen():
    ser.write('55c')
    time.sleep(0.1)
def lowerpen():
    ser.write('40c')
    time.sleep(0.1)

def convertToMotor(x):
    return np.array([x[0]+x[1],x[0]-x[1]])*5/np.sqrt(2)

def move_to(x):
    x = convertToMotor(x)
    ser.write(str(int(x[0])) + b'a')
    ser.write(str(int(x[1])) + b'b')
    ser.write(b'x')
    print ser.readline()
    time.sleep(.1)

print ser.readline()
grayimg = cv2.imread('./dogman.jpg',0)

#cv2.imshow('dogman',grayimg)
#cv2.waitKey(0)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
grayimg = cv2.pyrDown(grayimg)
print grayimg.shape

scale = 6.
maxval = np.max(grayimg)

for i in range(grayimg.shape[0]):
    for j in range(grayimg.shape[1]):
        lowerpen()
        move_to( np.array([i , j + grayimg[i,j]/maxval] ) * scale)
        raisepen()
        move_to( np.array([i, j+1]) * scale  )
