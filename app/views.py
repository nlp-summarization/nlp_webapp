from app import app
from flask import render_template, jsonify, request
from summarizers import gensim_summarize, baseline_summary

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

@app.route('/summary/', methods=['POST', 'GET'])
def summary():

  post = request.get_json()
  raw_text = post.get('raw_text')
  algo_id = post.get('id')

  f = {'summary': baseline_summary(raw_text)}
  return jsonify(**f)

if __name__ == '__main__':
  app.run(debug=True)