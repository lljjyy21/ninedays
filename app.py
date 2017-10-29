import os
import json
from flask import Flask, request, render_template
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


app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file

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

    empty_metrics = {
        "chance-of-rise": 0,
        "average-rise-percent": 0,
        "average-continuous-days": 0
    }

    empty_response_object = {
        "average-event": empty_metrics,
        "moving-average-event": empty_metrics,
        "pass-resistance-line-event": empty_metrics,
        "small-movement-event": empty_metrics,
        "support-line-rebound-event": empty_metrics
    }

    if not type_validator.validate():
        return json.dumps(empty_response_object), 404

    # TODO: Clarify that this is the write way to get data
    try:
        stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
        data = stock_data_processor.get_stock_data()
    except Exception as e:
        print(e)
        return json.dumps(empty_response_object), 400

    # Get all prices from data-set
    open_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Open')
    close_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Close')
    high_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'High')
    low_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Low')

    input_data = DataConverter(start, end, short_ma, long_ma, range_days)

    # Initialize all events
    average_event = AverageEvent(open_price, close_price)
    moving_average_event = MovingAverageEvent(close_price,,
    pass_resistance_line_event = PassResistanceLineEvent(high_price, input_data.get_range())
    small_movement_event = SmallMovementEvent(open_price, close_price)
    support_line_rebound_event = SupportLineReboundEvent(low_price, input_data.get_range())

    average_event_metric_calculator = StockMetricCalculator(data, average_event)
    moving_average_metric_calculator = StockMetricCalculator(data, moving_average_event)
    pass_resistance_line_metric_calculator = StockMetricCalculator(data, pass_resistance_line_event)
    small_movement_metric_calculator = StockMetricCalculator(data, small_movement_event)
    support_line_rebound_metric_calculator = StockMetricCalculator(data, support_line_rebound_event)

    return json.dumps({
        "average-event": average_event_metric_calculator.get_metrics(),
        "moving-average-event": moving_average_metric_calculator.get_metrics(),
        "pass-resistance-line-event": pass_resistance_line_metric_calculator.get_metrics(),
        "small-movement-event": small_movement_metric_calculator.get_metrics(),
        "support-line-rebound-event": support_line_rebound_metric_calculator.get_metrics()
    }), 200


if __name__ == "__main__":
    app.run(use_reloader=True)
