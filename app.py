import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
	origin = request.form['origin']
	destination = request.form['destination']
	outbound_date = request.form['date']
	processed_text = text.upper()
	
	return processed_text


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
