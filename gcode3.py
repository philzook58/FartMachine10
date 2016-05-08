#Now we're going to use control4 firmware


from parse import compile
p = compile("G{code} X{x} Y{y}")
import sys
import serial
port =  '/dev/ttyUSB0'#'/dev/cu.wch ch341 USB=>RS232 1410'#'tty.wch'#'cu.wch ch341 USB=>RS232 1410'
ser = serial.Serial(port,38400)  # open serial port
print(ser.name)         # check which port was really used
import numpy as np
import time


def raisepen():
    ser.write('50c')
    #time.sleep(0.1)
def lowerpen():
    ser.write('40c')
    #time.sleep(0.1)




def move(steps):
    ser.write(str(int(steps[0])) + b'a')
    ser.write(str(int(steps[1])) + b'b')
    ser.write(b'x')

def convertToMotor(x):
    return np.array([x[0]+x[1],x[0]-x[1]])/np.sqrt(2)
'''
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
'''

def move_to(x):
    x = convertToMotor(x)
    ser.write(str(int(x[0])) + b'a')
    ser.write(str(int(x[1])) + b'b')
    ser.write(b'x')
    print ser.readline()
    #time.sleep(.1)



x = np.zeros(2)
N=1000
raisepen()
filename = sys.argv[1]
f= open(filename)

#We need initial readline for some inexplicable reason. Seriously.
print ser.readline()

for line in f:
    #print line
    if line[0:2] == "G1":
        command = p.parse(line)
        if command != None:
            command = command.named
            x = np.array([float(command['x']),float(command['y'])])
            move_to(x)

    elif line[0:3] == "M05":
        raisepen()
    elif line[0:3] == "M03":
        lowerpen()

ser.close()             # close port
