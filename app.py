import os
import json
import datetime
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

# Flask app minimal configurations
app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.globals.update(current_date=current_date.get_current_server_date)


# Routes
@app.route("/")
def index(message=''):
    return render_template("index.html", message=message)


# TODO: Refactor!
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


    # TODO: Rewrite fail message
    empty_metrics = {
        "chance-of-rise": 0,
        "average-continuous-days": 0,
        "class_name": "",
        "description": ""
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
        print(type(start), type(end))
        stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
        data_based_on_user_input = stock_data_processor.get_stock_data()
        open_price_based_on_user_input = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_user_input, 'Open')
        close_price_based_on_user_input = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_user_input, 'Close')
    except Exception as e:
        print("1!")
        print(e)
        return json.dumps(empty_response_object), 400

    input_data = DataConverter(start, end, short_ma, long_ma, range_days)
    events_based_on_user_input = [AverageEvent(open_price_based_on_user_input, close_price_based_on_user_input),
                                  MovingAverageEvent(close_price_based_on_user_input, input_data.get_short_ma(),
                                                     input_data.get_long_ma()),
                                  PassResistanceLineEvent(open_price_based_on_user_input, input_data.get_range()),
                                  SmallMovementEvent(open_price_based_on_user_input, close_price_based_on_user_input),
                                  SupportLineReboundEvent(open_price_based_on_user_input, input_data.get_range())]

    try:
        ONE_DAY = 1
        start = (datetime.datetime.now() - datetime.timedelta(input_data.get_long_ma() + ONE_DAY))\
            .strftime("%Y-%m-%d")\
            .decode("utf-8")
        end = (datetime.datetime.now() - datetime.timedelta(ONE_DAY))\
            .strftime("%Y-%m-%d")\
            .decode("utf-8")

        print(type(start), type(end))
        print(start, end)

        stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
        data_based_on_long_ma = stock_data_processor.get_stock_data()
        # TODO: Move 'Open' and 'Close' to constants
        open_price = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_long_ma, 'Open')
        close_price = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_long_ma, 'Close')
    except Exception as e:
        print("2!")
        print(e)
        return json.dumps(empty_metrics), 400

    events_based_on_long_ma = [AverageEvent(open_price, close_price),
                               MovingAverageEvent(close_price, input_data.get_short_ma(), input_data.get_long_ma()),
                               PassResistanceLineEvent(open_price, input_data.get_range()),
                               SmallMovementEvent(open_price, close_price),
                               SupportLineReboundEvent(open_price, input_data.get_range())]


    response = dict()
    for event_based_on_user_input, event_based_on_long_ma in zip(events_based_on_user_input, events_based_on_long_ma):
        print(type(event_based_on_user_input), type(event_based_on_long_ma))
        metrics = StockMetricCalculator(data_based_on_user_input, event_based_on_user_input)

        event_response_data = dict()
        event_response_data.update(metrics.get_metrics())
        event_response_data.update(event_based_on_user_input.get_event_metadata())
        event_response_data.update({'event-was-triggered': event_based_on_long_ma.event_triggered_at_the_last_date()})

        response[event_based_on_user_input.class_name] = event_response_data

    # TODO: Remove
    print(response)

    return json.dumps(response), 200


if __name__ == "__main__":
    app.run(use_reloader=True)
