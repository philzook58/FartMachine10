from flask import Flask
from flask import render_template
import threading
import time

app = Flask(__name__)

a = 1

@app.route("/")
def hello():
	return render_template('test.html', a=a)



t = threading.Thread(target=app.run)
t.start()

for i in range(1000):
	a+=1
	time.sleep(1)

