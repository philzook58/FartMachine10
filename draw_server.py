from draw import DrawBot
import sys
#from flask import Flask
#from flask import render_template
import threading
import time

bot = DrawBot("/dev/ttyUSB0")



filename = sys.argv[1]
gcode = '''
G90

G21

G1 F3000

G1 X0.5702 Y0.5702

G1 X0 Y0

G1 X0.5 Y0.5
'''


bot.draw(gcode.split('\n'))
#bot.drawFromFile(filename)
