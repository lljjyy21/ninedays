import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from finance import stock_processor as sc
from finance import stock_data_processor as sdp
from finance.metrics.stock_metric_calculator import StockMetricCalculator

from helper import current_date
from helper.input_type_validator import TypeValidator
from helper.data_converter import DataConverter

from finance.events.average_event import AverageEvent
from finance.events.moving_average_event import MovingAverageEvent
from finance.events.pass_resistance_line_event import PassResistanceLineEvent
from finance.events.small_movement_event import SmallMovementEvent
from finance.events.support_line_rebound_event import SupportLineReboundEvent
from finance.stock_calculator import StockCalculator


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

app.jinja_env.globals.update(current_date=current_date.get_current_server_date)


@app.route("/")
def index(message=''):
    return render_template("index.html", message=message)


# TODO: Write test for this call
# <basic_url>/calculate?stock=<stock_name>&start=<start_date>&end=<end_date>&
# short_ma=<short_ma>&long_ma=<long_ma>&range_days=<range>
@app.route("/calculate", methods=["GET"])
def calculate_stock_chances():

    # WARNING: This can be true if someone sends request directly (trying to hack the website)
    stock_name = request.args.get('stock')
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    short_ma = request.args.get('short_ma')
    long_ma = request.args.get('long_ma')
    range_days = request.args.get('range')

    # Data validator
    type_validator = TypeValidator(start, end, short_ma, long_ma, range_days)
    if not type_validator.validate():
        return json.dumps({
            "error": "Sorry, the input data is in a wrong format!"
        })

    # Data converter
    input_data = DataConverter(start, end, short_ma, long_ma, range_days)

    # TODO: Clarify that this this the write way to get data
    stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
    data = stock_data_processor.get_stock_data()

    # Get all prices from dataset
    open_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Open')
    close_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Close')
    high_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'High')
    low_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Low')

    # Initialize all events
    average_event = AverageEvent(open_price, close_price)
    # moving_average_event = MovingAverageEvent(open_price, close_price, high_price, input_data.get_short_ma(), input_data.get_long_ma())
    pass_resistance_line_event = PassResistanceLineEvent(high_price, input_data.get_range())
    small_movement_event = SmallMovementEvent(open_price, close_price)
    support_line_rebound_event = SupportLineReboundEvent(low_price, input_data.get_range())

    average_event_metric_calculator = StockMetricCalculator(data, average_event)
    # moving_average_metric_calculator = StockMetricCalculator(data, moving_average_event)
    pass_resistance_line_metric_calculator = StockMetricCalculator(data, pass_resistance_line_event)
    small_movement_metric_calculator = StockMetricCalculator(data, small_movement_event)
    support_line_rebound_metric_calculator = StockMetricCalculator(data, support_line_rebound_event)

    return json.dumps({
        "average-event": average_event_metric_calculator.get_metrics(),
        "moving-average-event": {}, #moving_average_metric_calculator.get_metrics(),
        "pass-resistance-line-event": pass_resistance_line_metric_calculator.get_metrics(),
        "small-movement-event": small_movement_metric_calculator.get_metrics(),
        "support-line-rebound-event": support_line_rebound_metric_calculator.get_metrics()
    })


if __name__ == "__main__":
    app.run(use_reloader=True)
