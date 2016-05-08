from draw import DrawBot
import sys
from flask import Flask
from flask import request
from flask import render_template
import threading
import time

app = Flask(__name__)

bot = DrawBot("/dev/ttyUSB0")


@app.route("/")
def hello():
	return '<form action="/draw" method="GET"><textarea name="gcode"></textarea><input type="submit" value="Draw"></form>'

@app.route("/draw")
def draw():
    bot.draw(request.args.get('gcode','').split('\r\n'))
    return '<h1>done</h1>'

app.run(host="0.0.0.0", port=5000)
