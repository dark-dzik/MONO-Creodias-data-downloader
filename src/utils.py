import datetime
import dateutil


def add_one_day(date):
    if date.hour == 0 and date.minute == 0 and date.second == 0:
        date = date + datetime.timedelta(hours=24, minutes=00, seconds=00)
        return date
    return date


##
# This should receive number of days to add as argument, but at this point,
# when whole code is trashy af, it doesn't matter.
# Don't touch my garbage.
def add_seven_days(date):
    if date.hour == 0 and date.minute == 0 and date.second == 0:
        date = date + datetime.timedelta(hours=191, minutes=59, seconds=59)
        return date
    return date


def parse_date(date):
    if isinstance(date, datetime.datetime):
        return date
    try:
        return dateutil.parser.parse(date)
    except ValueError:
        raise ValueError('Date {date} is not in a valid format. Use Datetime object or iso string')


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
