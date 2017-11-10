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

OPEN, CLOSE = 'Open', 'Close'
TIME_PATTERN, UTF8 = '%Y-%m-%d', 'utf-8'


@app.route("/")
def index(message=''):
    return render_template("index.html", message=message)


# TODO: Write test for this call
# <basic_url>/calculate?stock=<stock_name>&start=<start_date>&end=<end_date>&
# short_ma=<short_ma>&long_ma=<long_ma>&range_days=<range>
@app.route("/calculate", methods=["GET"])
def calculate_stock_chances():

    empty_event_details = {
        "chance-of-rise": 0,
        "average-continuous-days": 0,
        "class_name": "",
        "description": ""
    }

    empty_response_object = {
        "average-event": empty_event_details,
        "moving-average-event": empty_event_details,
        "pass-resistance-line-event": empty_event_details,
        "small-movement-event": empty_event_details,
        "support-line-rebound-event": empty_event_details
    }

    # Check number of parameters and if all required are present
    try:
        end, long_ma, range_days, short_ma, start, stock_name = retrieve_parameters_from_url()
    except ValueError as e:
        print(e)
        return json.dumps(empty_response_object), 422

    # Validate parameters of input arguments
    type_validator = TypeValidator(start, end, short_ma, long_ma, range_days)
    if not type_validator.validate():
        return json.dumps(empty_response_object), 404

    # Create response with classes metadata and calculations, if possible
    try:
        input_data = DataConverter(start, end, short_ma, long_ma, range_days)
        events_based_on_user_input, data_based_on_user_input = get_events_based_on_user_input(stock_name, input_data,
                                                                                              start, end)
        events_based_on_long_ma, data_based_on_long_ma = get_events_based_on_long_ma(stock_name, input_data)

        response = create_response(data_based_on_user_input, events_based_on_long_ma, events_based_on_user_input)
    except Exception as e:
        print(e)
        return json.dumps(empty_response_object), 400

    return json.dumps(response), 200


def retrieve_parameters_from_url():
    args = request.args
    stock_name = args.get('stock')
    start = args.get('start_date')
    end = args.get('end_date')
    short_ma = args.get('short_ma')
    long_ma = args.get('long_ma')
    range_days = args.get('range')

    parameters = [stock_name, start, end, short_ma, long_ma, range_days]

    if None in parameters:
        raise ValueError('One of url parameters is missed')

    if len(args) > len(parameters):
        raise ValueError('Redundant parameters are present')

    print(args)

    return end, long_ma, range_days, short_ma, start, stock_name


def create_response(data_based_on_user_input, events_based_on_long_ma, events_based_on_user_input):
    response = dict()
    for event_based_on_user_input, event_based_on_long_ma in zip(events_based_on_user_input, events_based_on_long_ma):
        print(type(event_based_on_user_input), type(event_based_on_long_ma))
        metrics = StockMetricCalculator(data_based_on_user_input, event_based_on_user_input)

        event_response_data = dict()
        event_response_data.update(metrics.get_metrics())
        event_response_data.update(event_based_on_user_input.get_event_metadata())
        event_response_data.update({'event-was-triggered': event_based_on_long_ma.event_triggered_at_the_last_date()})

        response[event_based_on_user_input.class_name] = event_response_data
    return response


def get_events_based_on_long_ma(stock_name, input_data):
    ONE_DAY = 1
    start = (datetime.datetime.now() - datetime.timedelta(input_data.get_long_ma() + ONE_DAY)).strftime(TIME_PATTERN)\
        .decode(UTF8)
    end = (datetime.datetime.now() - datetime.timedelta(ONE_DAY)).strftime(TIME_PATTERN).decode(UTF8)

    stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
    data_based_on_long_ma = stock_data_processor.get_stock_data()

    open_price = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_long_ma, OPEN)
    close_price = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_long_ma, CLOSE)

    events_based_on_long_ma = [AverageEvent(open_price, close_price),
                               MovingAverageEvent(close_price, input_data.get_short_ma(), input_data.get_long_ma()),
                               PassResistanceLineEvent(open_price, input_data.get_range()),
                               SmallMovementEvent(open_price, close_price),
                               SupportLineReboundEvent(open_price, input_data.get_range())]
    return events_based_on_long_ma, data_based_on_long_ma


def get_events_based_on_user_input(stock_name, input_data, start, end):

    stock_data_processor = sdp.StockDataProcessor(stock_name, start, end)
    data_based_on_user_input = stock_data_processor.get_stock_data()
    open_price_based_on_user_input = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_user_input, OPEN)
    close_price_based_on_user_input = StockMetricCalculator.data_frame_to_numpy_array(data_based_on_user_input, CLOSE)

    events_based_on_user_input = [AverageEvent(open_price_based_on_user_input, close_price_based_on_user_input),
                                  MovingAverageEvent(close_price_based_on_user_input, input_data.get_short_ma(),
                                                     input_data.get_long_ma()),
                                  PassResistanceLineEvent(open_price_based_on_user_input, input_data.get_range()),
                                  SmallMovementEvent(open_price_based_on_user_input, close_price_based_on_user_input),
                                  SupportLineReboundEvent(open_price_based_on_user_input, input_data.get_range())]

    return events_based_on_user_input, data_based_on_user_input


if __name__ == "__main__":
    app.run(use_reloader=True)
