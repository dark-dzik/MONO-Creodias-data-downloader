import datetime
import dateutil


def add_one_day(date):
    if date.hour == 0 and date.minute == 0 and date.second == 0:
        date = date + datetime.timedelta(hours=47, minutes=59, seconds=59)
        return date
    return date


def parse_date(date):
    if isinstance(date, datetime.datetime):
        return date
    try:
        return dateutil.parser.parse(date)
    except ValueError:
        raise ValueError('Date {date} is not in a valid format. Use Datetime object or iso string')