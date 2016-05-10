from flask import Flask, url_for
from flask import render_template
app = Flask(__name__)

@app.route("/")
def whathello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

url_for('static', filename='style.css')
