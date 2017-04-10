import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def home_post():
	origin = request.form['origin']
	destination = request.form['destination']
	outbound_date = request.form['date']
	processed_text = origin.upper()
	return pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e']).to_frame().to_html()


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
