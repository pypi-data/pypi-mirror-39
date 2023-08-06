from datetime import datetime, timedelta
from dateutil import parser
import sys
import traceback
from enum import IntEnum
from random import randrange
from dateutil.relativedelta import relativedelta, SU, SA
from math import ceil


class Days(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def convert_date(str_date):
    try:
        if str_date:
            
            if not isinstance(str_date, str):
                return str_date
            
            date = parser.parse(str_date)
            if date.year + 100 > datetime.today().year:
                return date
        return datetime.today()
    except:
        traceback.print_exc(file=sys.stdout)
        return datetime.today()


def last_day_of_month(month):
    next_month = month.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def first_day_of_month(month):
    return month.replace(day=1)


def get_previous_sunday(day):
    return day + relativedelta(weekday=SU(-1 if day.weekday() != Days.SUNDAY else -2))


# diff = (day.weekday() + 1) % 7
# return day - timedelta(7 + diff)


def get_next_sunday(day):
    return day + relativedelta(weekday=SA(1 if day.weekday() != Days.SATURDAY else 2))


# diff = (day.weekday() + 1) % 7
# return day - timedelta(7 + diff)


def random_date_between(begin_date, end_date):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end_date - begin_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    if int_delta > 0:
        random_second = randrange(int_delta)
        return begin_date + timedelta(seconds=random_second)
    return begin_date


def round_time(dt, round_to=60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object
    round_to : Closest number of seconds to round to, default 1 minute.
    """
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def daterange(start_date, end_date):
    """Itera datas em um periodo especifico"""
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def hourrange(start_hour, end_hour):
    """Itera Horas em um periodo especifico"""
    for n in range(0, int((end_hour - start_hour).seconds + 3600), 3600):
        yield start_hour + timedelta(seconds=n)


def count_sundays(begin_date, end_date):
    """Retorna a quantidade de domingos dentro de um periodo especifico"""
    count = 0
    for date in daterange(begin_date, end_date):
        if date.weekday() == int(Days.SUNDAY):
            count += 1
    return count


def month_subtract(date, count_months):
    """ Subtrai meses de uma data"""
    day = date.day
    new_date = date
    for i in range(count_months):
        new_date = new_date.replace(day=1) - timedelta(days=1)
    return new_date.replace(day=day)


def week_sum(date, count_weeks):
    """ Soma semanas em uma determinada data, considerando que uma semana possui 7 dias"""
    new_date = date
    for i in range(count_weeks):
        new_date += timedelta(7)
    return new_date


def date_to_float(date):
    if type(date) is timedelta:
        return date.seconds // 3600 + (date.seconds // 60) % 60 / 100
    return date.hour + date.minute / 100


def first_day_of_week(date):
    first_day = date
    while first_day.weekday() != Days.SUNDAY:
        first_day -= timedelta(1)
    return first_day


def last_day_of_week(date):
    last_day = date
    while last_day.weekday() != Days.SATURDAY:
        last_day += timedelta(1)
    return last_day


def count_days_of_month(month):
    count = 0
    for day in daterange(first_day_of_month(month), last_day_of_month(month)):
        count += 1
    return count


def convert_timedelta_to_time(date_timedelta):
    return (datetime.min + date_timedelta).time()


def week_of_month(date):
    """ Returns the week of the month for the specified date. """
    first_day = date.replace(day=1)
    dom = date.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom / 7.0))


def timedelta_to_str(dt_timedelta):
    """ Converte timedelta para string, colocando os dias, horas, minutos e segundos"""
    timedelta_str = ''
    days, hours, = dt_timedelta.days, dt_timedelta.seconds // 3600
    minutes, seconds = (dt_timedelta.seconds // 60) % 60, dt_timedelta.seconds % 60
    timedelta_str += str(days) + ' dia :' if days > 0 else ''
    timedelta_str += str(hours) + ' h : ' if hours > 0 else ''
    timedelta_str += str(minutes) + ' m :' if minutes > 0 else ''
    timedelta_str += ' ' + str(seconds) + ' s ' if seconds > 0 else ''
    return timedelta_str[0:-1]
