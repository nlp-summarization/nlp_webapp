from app import app
from flask import render_template, jsonify

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

@app.route('/summary/<algo_id>', methods=['GET', 'POST'])
def summary(algo_id=None):
	text = "Thomas A. Anderson is a man living two lives. By day he is an " + \
      "average computer programmer and by night a hacker known as " + \
      "Neo. Neo has always questioned his reality, but the truth is " + \
      "far beyond his imagination. Neo finds himself targeted by the " + \
      "police when he is contacted by Morpheus, a legendary computer " + \
      "hacker branded a terrorist by the government. Morpheus awakens " + \
      "Neo to the real world, a ravaged wasteland where most of " + \
      "humanity have been captured by a race of machines that live " + \
      "off of the humans' body heat and electrochemical energy and " + \
      "who imprison their minds within an artificial reality known as " + \
      "the Matrix. As a rebel against the machines, Neo must return to " + \
      "the Matrix and confront the agents: super-powerful computer " + \
      "programs devoted to snuffing out Neo and the entire human " + \
      "rebellion."

	f = {'summary': text}
	return jsonify(**f)

if __name__ == '__main__':
  app.run(debug=True)