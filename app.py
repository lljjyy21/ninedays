import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from finance import stock_processor as sc

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'finance.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FINANCE_SETTINGS', silent=True)


# connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/")
def index(message=''):
    return render_template("index.html", message=message)


# TODO: Write test for this call
# <basic_url>/calculate?stock=<stock_name>&start=<start_date>&end=<end_date>&
# short_ma=<short_ma>&long_ma=<long_ma>&range_days=<range>
@app.route("/calculate", methods=["GET"])
def calculate_stock_chances():
    stock_name = request.args.get('stock')
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    short_ma = request.args.get('short_ma')
    long_ma = request.args.get('long_ma')
    range_days = request.args.get('range')

    stock = sc.StockProcessor(stock_name, start, end, short_ma, long_ma, range_days)

    message = stock.info()
    return json.dumps({
        "message": message
    })


if __name__ == "__main__":
    # init_db()
    app.run()
