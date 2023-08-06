from dateutil.relativedelta import relativedelta
import dateutil.parser
import datetime
import traceback
from chatqhelper.common import constants


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def str_to_ts(timestr):
    return dateutil.parser.parse(timestr).replace(tzinfo=datetime.timezone.utc).timestamp()


class TimeSpliter:
    UNIT_MAP = {
        'h': 'hour',
        'm': 'minute',
        's': 'second',
        'D': 'day',
        'M': 'month',
        'Y': 'year',
    }

    DURATION_STRIP_ORDER = ('microsecond', 'second', 'minute', 'hour', 'day', 'month')

    TIMEDELTA_MAP = {
        'minute': (datetime.timedelta, 'minutes'),
        'hour': (datetime.timedelta, 'hours'),
        'day': (relativedelta, 'days'),
        'month': (relativedelta, 'months'),
        'year': (relativedelta, 'years'),
    }

    @staticmethod
    def _identify(identifier):
        return (int(identifier[:-1]), TimeSpliter.UNIT_MAP[identifier[-1]])

    @staticmethod
    def delta(identifier):
        size, unit = TimeSpliter._identify(identifier)
        delta_class, delta_key = TimeSpliter.TIMEDELTA_MAP[unit]
        return delta_class(**{delta_key: size})

    @staticmethod
    def generate_durations(time_identifier, size, start=None):
        duration_start = start
        if duration_start is None:
            duration_start = datetime.datetime.utcnow()

        duration_size, duration_unit = TimeSpliter._identify(time_identifier)
        if size < 0: raise ValueError('size must be positive')

        # Strip the duration start time
        # For example if duration is a hour then it will remove all minute, second and microsecond
        strip = {}
        for item in TimeSpliter.DURATION_STRIP_ORDER:
            if item == duration_unit:
                break

            if item in ['day', 'month']:
                strip[item] = 1
            else:
                strip[item] = 0

        duration_start = duration_start.replace(**strip)

        # Normalize duration base on initial duration size
        # So if current hour is 10 and duration is every 4 hour then it will normallize start duration hour  to 8
        if duration_size > 1:
            normalize = getattr(duration_start, duration_unit) // duration_size * duration_size
            if duration_unit in ['day', 'month', 'year']:
                normalize += 1

            duration_start = duration_start.replace(**{duration_unit: normalize})

        time_delta = TimeSpliter.delta(time_identifier)
        duration_end = duration_start + time_delta
        durations = [duration_end, duration_start]
        for _ in range(0, size):
            duration_start = duration_start - time_delta
            durations.append(duration_start)

        return durations


def err_to_dict(err):
    return {
        'exception': str(err.__class__.__name__),
        'message': str(err),
        'code': getattr(err, 'code', 500),
        'traceback': traceback.format_exc(),
        'service': constants.SERVICE_NAME,
        'hostname': constants.HOSTNAME
        }
