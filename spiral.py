
from parse import compile
p = compile("G{code} X{x} Y{y}")
import sys
import serial
port =  '/dev/cu.wch ch341 USB=>RS232 1410'#'tty.wch'#'cu.wch ch341 USB=>RS232 1410'
ser = serial.Serial(port,38400)  # open serial port
print(ser.name)         # check which port was really used
import numpy as np
import time


def raisepen():
    ser.write('30c')
    #time.sleep(0.1)
def lowerpen():
    ser.write('20c')
    #time.sleep(0.1)


def convertToMotor(x):
    return np.array([x[0]+x[1],x[0]-x[1]])/np.sqrt(2)


def move_to(x):
    x = convertToMotor(x)
    ser.write(str(int(x[0])) + b'a')
    ser.write(str(int(x[1])) + b'b')
    ser.write(b'x')
    print ser.readline()
    #time.sleep(.1)
print ser.readline()

radius = 400
N = 14
maxangle = 2 * np.pi * N
deltaangle = 2 * np.pi / 6
angles = np.arange(0,maxangle,deltaangle)
r = angles * radius / maxangle
x = r * np.cos(angles)
y = r * np.sin(angles)

lowerpen()
for i in range(len(x)):
    move_to(np.array([x[i],y[i]]))

ser.close()
