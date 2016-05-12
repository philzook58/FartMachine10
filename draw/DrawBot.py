import numpy as np
import time
from parse import compile
import sys
import serial
import serial.tools.list_ports

class DrawBot:
    def __init__(self, port=None, baud=38400):
        if port:
            self.port = port
        else:
            self.port = serial.tools.list_ports.comports()[-1][0]
        self.ser = serial.Serial(self.port, baud)  # open serial port
        self.p = compile("G{code} X{x} Y{y}")
        print self.ser.readline()
        self.offset = 0

        self.homepen()
    def drawFromFile(self, file_name):
        file = open(file_name)
        self.draw(file)
        file.close()
    def draw(self,gcode):
        x = np.zeros(2)
        self.raisepen()


        self.ser.timeout=0.5
        print self.ser.readline()
        self.ser.timeout =0.

        for line in gcode:
            print line
            if line[0:2] == "G1":
		command = self.p.parse(line)
		print command
                if command != None:
                    command = command.named
                    x = np.array([float(command['x']),float(command['y'])])
                    self.move_to(x)

            elif line[0:3] == "M05":
                self.raisepen()
            elif line[0:3] == "M03":
                self.lowerpen()
    def __del__(self):
        self.ser.close()
    def raisepen(self):
        self.ser.write(str(self.penAngle + 10 + self.offset) + 'c')
        print str(self.penAngle + self.offset + 10)
    def lowerpen(self):
        self.ser.write(str(self.penAngle + self.offset) + 'c')
        print str(self.penAngle + self.offset)
    def homepen(self):
        self.ser.write('h');
        self.penAngle = int(self.ser.readline())
    def reset(self):
        self.ser.write('r');
    def move(self,steps):
        self.ser.write(str(int(steps[0])) + b'a')
        self.ser.write(str(int(steps[1])) + b'b')
        self.ser.write(b'x')
    def convertToMotor(self,x):
        return np.array([x[0]+x[1],x[0]-x[1]])/np.sqrt(2)
    def move_to(self,x):
        x = self.convertToMotor(x)
        self.ser.write(str(int(x[0])) + b'a')
        self.ser.write(str(int(x[1])) + b'b')
        self.ser.write(b'x')
        print self.ser.readline()
