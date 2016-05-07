
from parse import compile
p = compile("G{code} X{x} Y{y}")
import sys
import serial
port = '/dev/cu.wch ch341 USB=>RS232 1410'#'tty.wch'#'cu.wch ch341 USB=>RS232 1410'
ser = serial.Serial(port,38400)  # open serial port
print(ser.name)         # check which port was really used
import numpy as np
import time


def raisepen():
    ser.write('70c')
    time.sleep(0.1)
def lowerpen():
    ser.write('95c')
    time.sleep(0.1)




def move(steps):
    ser.write(str(int(steps[0])) + b'a')
    ser.write(str(int(steps[1])) + b'b')

def convertToMotor(x):
    return np.array([x[0]+x[1],x[0]-x[1]])

def draw_line(x,xend):
    x = convertToMotor(x)
    xend = convertToMotor(xend)
    deltax = (xend - x)/N
    xint = np.rint(x)
    for i in range(N):
        x = x + deltax
        #print x
        if np.any(np.rint(x) != xint):
            steps = np.rint(x) - xint
            move(steps)
            xint = np.rint(x)
            time.sleep(0.03)

x = np.zeros(2)
N=1000
raisepen()
filename = sys.argv[1]
f= open(filename)
for line in f:
    print line
    if line[0:2] == "G1":
        command = p.parse(line)
        if command != None:
            command = command.named
            xnew = np.array([float(command['x']),float(command['y'])])
            draw_line(x, xnew)
            x = xnew
    elif line[0:3] == "M05":
        raisepen()
    elif line[0:3] == "M03":
        lowerpen()

ser.close()             # close port
