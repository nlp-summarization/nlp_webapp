from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/<name>')
def hello_name(name):
  return "Hello {}!".format(name)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

if __name__ == '__main__':
  app.run()