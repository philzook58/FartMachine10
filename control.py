import serial
port = '/dev/cu.wch ch341 USB=>RS232 1410'#'tty.wch'#'cu.wch ch341 USB=>RS232 1410'
ser = serial.Serial(port,38400)  # open serial port
print(ser.name)         # check which port was really used
import numpy as np
import time


x = np.zeros(2)

N=1000

globalsteps = np.array([0,0])

def raisepen():
    pass
def lowerpen():
    pass


def move(steps):
    #print steps
    global globalsteps
    ser.write(str(int(steps[0])) + b'a')
    ser.write(str(int(steps[1])) + b'b')
    globalsteps = globalsteps + steps
    #print globalsteps



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


pos = np.array([[-10.,-10.], [10.,-10.],[-10.,-10.], [-10.,10.]])*3
i = 0
while(1):

    draw_line(x,pos[i,:])
    x = pos[i,:]
    print x
    time.sleep(.5)
    print("YO")
    #print(ser.read(100))
    i+= 1
    i = i%4
ser.close()             # close port
