from events.models import Event
from core.models import Region
import time
import locale
import calendar


def generate_sport_kind_choices():
    sport_kind_choices = Event.sport_kind.field.choices.copy()
    sport_kind_choices.insert(0, ('ALL', 'Вид спорта - все'))
    return sport_kind_choices


def generate_region_choices():
    region_choices = list(Region.objects.all().values_list('id', 'title'))
    region_choices.insert(0, ('ALL', 'Регион - все'))
    return region_choices


def generate_month_choices():
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    now = time.localtime()
    year_month_raw = [
        time.localtime(
            time.mktime(
                (now.tm_year, now.tm_mon + n, 1, 0, 0, 0, 0, 0, 0),
            ),
        )[:2]
        for n in range(13)
    ]
    month_choices = [
        (
            f'{t[0]}-{t[1]}',
            f'{t[0]} {calendar.month_name[t[1]]}',
        )
        for t in year_month_raw
    ]
    month_choices.insert(0, ('ALL', 'Даты - все'))
    return month_choices
