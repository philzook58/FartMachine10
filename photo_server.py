from draw import DrawBot
import sys
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
import threading
import time
import base64

app = Flask(__name__)
app.debug = True

#bot = DrawBot("/dev/ttyUSB0")


@app.route("/")
def hello():
	return render_template("camera.html")

@app.route('/js/<path:path>')
def send_js(path):
	print path
	return send_from_directory('js', path)

@app.route("/draw")
def draw():
    bot.draw(request.args.get('gcode','').split('\r\n'))
    return '<h1>done</h1>'

@app.route("/image", methods=['POST'])
def image():
	#newjpgtxt = request.get_json().get('data','').split(",")
	newjpgtxt = request.form['data'].split(",")[1]
	g = open("out.jpg", "w")
	g.write(base64.decodestring(newjpgtxt))
	g.close()
	return '<h1>done</h1>'

app.run()
