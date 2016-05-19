from draw import DrawBot
import sys
from flask import Flask
from flask import request
from flask import render_template
import threading
import time
import json
from photo import PhotoConverter
app = Flask(__name__)
#app.debug = True
bot = DrawBot()
#bot = False
gcode = ""



@app.route("/gcode")
def hello():
	return '<form action="/draw" method="GET"><textarea name="gcode"></textarea><input type="submit" value="Draw"></form>'


@app.route('/')
def root():
	return render_template('index.html')

@app.route('/contour')
def contour():
	return app.send_static_file('contour.jpg')

@app.route('/frame')
def frame():
	return app.send_static_file('frame.jpg')

'''
@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)
'''

@app.route("/home")
def home():
	bot.homepen()
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



@app.route("/draw")
def draw():
	bot.draw(request.args.get('gcode','').split('\r\n'))
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/photo")
def photo():
	photo = PhotoConverter()
	photo.takePhoto()
	gcode = photo.convertContourstoGcode().split('\r\n')
	photo.closeCamera()
	photo.saveContour('static/contour.jpg')
	photo.saveFrame('static/frame.jpg')
	photo.sortContours()
	photo.scaleContours(1500,1100)
	status = bot.draw(gcode)
	if status == "busy":
		return json.dumps({'success':False}), 200, {'ContentType':'application/json'}
	else:
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/takephoto")
def takePhoto():
	photo = PhotoConverter()
	photo.takePhoto()
	global gcode
	gcode = photo.convertContourstoGcode().split('\r\n')
	photo.closeCamera()
	photo.saveContour('static/contour.jpg')
	photo.saveFrame('static/frame.jpg')
	photo.sortContours()
	photo.scaleContours(1500,1100)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/drawphoto")
def drawPhoto():
	print gcode
	bot.draw(gcode)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

'''

@app.route('/offset/<int:offset>')
def set_offset(offset):
	bot.offset = offset
	print offset
	print type(offset)
	return 'New offset'
'''

@app.route('/move', methods=['GET', 'POST'])
def move():
	if request.method == 'POST':
		bot.move_to( [int(request.form['x']), int(request.form['y'])] )
	return '<form action="/move" method="POST"> x<input type="text" name="x"><br>y <input type="text" name="y"> <br><input type="submit" value="Move"></form>'


@app.route('/reset')
def reset():
	bot.reset()
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/stop')
def stop():
	bot.setStop(True)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}




app.run(host="0.0.0.0", port=5000)
