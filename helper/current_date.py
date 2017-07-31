import datetime


def get_current_server_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
