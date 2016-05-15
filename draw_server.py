from draw import DrawBot
import sys
from flask import Flask
from flask import request
from flask import render_template
import threading
import time
from photo import PhotoConverter
app = Flask(__name__)
#app.debug = True
bot = DrawBot()



@app.route("/gcode")
def hello():
	return '<form action="/draw" method="GET"><textarea name="gcode"></textarea><input type="submit" value="Draw"></form>'


@app.route('/')
def root():
	return app.send_static_file('index.html')

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
	return '<h1>done</h1>'



@app.route("/draw")
def draw():
	bot.draw(request.args.get('gcode','').split('\r\n'))
	return '<h1>done</h1>'

@app.route("/photo")
def photo():
	photo = PhotoConverter()
	photo.takePhoto()
	gcode = photo.convertContourstoGcode().split('\r\n')
	photo.closeCamera()
	photo.saveContour('static/contour.jpg')
	photo.saveFrame('static/frame.jpg')
	bot.draw(gcode)
	return '<h1>done</h1>' 

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
	return '<h1>done</h1>' 

@app.route('/stop')
def stop():
	bot.setStop(True)
	return '<h1>done</h1>' 




app.run(host="0.0.0.0", port=5000)
