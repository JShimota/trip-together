import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import flightSearch
from datetime import datetime as dt
import sys
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def home_post():

	try:
		print request.form['origin'],request.form['destination'],request.form['date'],type(request.form['date'])
		sys.stdout.flush()
	except:
		print 'error with form'
		sys.stdout.flush()
	origin = request.form['origin'].split(',')
	destination = request.form['destination'].split(',')
	outbound_date = request.form['date']#.strftime('%Y-%m-%d')
		
	print 'flightSearch.comparePrices(%s,%s,%s).to_html(index = False )' % (origin,destination,outbound_date)
	sys.stdout.flush()
	
	try:
		df = flightSearch.comparePrices(origin,
		destination,
		outbound_date).to_html(index = False, classes = 'table' )
	except:
		return 'Something went wrong, tell Nathan what you did'
	#return df
	print df
	return render_template('view.html',tables=[df])


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
