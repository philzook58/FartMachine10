from draw import DrawBot
import sys

bot = DrawBot("/dev/ttyUSB0")

filename = sys.argv[1]
bot.draw(filename)
