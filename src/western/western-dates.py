import json
from datetime import date, timedelta
from enum import Enum

#utility

def calculate_offset(base_date, offset_days):
    return base_date + timedelta(days=offset_days)

def get_fixed_date(year, month, day):
    return date(year, month, day)

def get_sunday_of(holiday):
    offset_days = (6 - holiday.weekday()) % 7
    return calculate_offset(holiday, offset_days)

#liturgy

class Holiday(Enum):
    EASTER = "easter"
    CHRISTMAS = "christmas"
    PENTECOST = "pentecost"
    EPIPHANY = "epiphany"
    LENT_START = "lent_start"
    LENT_END = "lent_end"
    HOLY_WEEK_START = "holy_week_start"
    MAUNDY_THURSDAY = "maundy_thursday"
    GOOD_FRIDAY = "good_friday"
    ADVENT_START = "advent_start"
    ADVENT_END = "advent_end"
    TRANSFIGURATION = "transfiguration"
    TRINITY_SUNDAY = "trinity_sunday"
    PENTECOST_END = "pentecost_end"
    ALL_SAINTS = "all_saints"
    THANKSGIVING = "thanksgiving"
    THANKSGIVING_CA = "thanksgiving_ca"

def get_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def get_advent_start(year):
    christmas = get_fixed_date(year, 12, 25)
    fourth_sunday_before_christmas = christmas - timedelta(days=(christmas.weekday() + 22) % 7)
    advent_start = fourth_sunday_before_christmas - timedelta(weeks=3)
    return advent_start

def get_thanksgiving(year, canada=False):
    if canada:
        first_day = date(year, 10, 1)
        first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
        return first_monday + timedelta(weeks=1)
    first_day = date(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    return first_thursday + timedelta(weeks=3)

def get_holiday(year, holiday):
    with open('liturgical-rules.json', 'r') as f:
        rules = json.load(f)
    holiday_data = rules.get(holiday.value)

    if not holiday_data:
        raise ValueError(f"Unrecognized or unsupported holiday rule for: {holiday}")
    #dependent holidays
    if "depends_on" in holiday_data:
        base_holiday = Holiday[holiday_data["depends_on"].upper()]
        base_date = get_holiday(year, base_holiday)
        offset_days = holiday_data.get("offset_days", 0)
        return calculate_offset(base_date, offset_days)
    #fixed holidays
    elif "fixed_date" in holiday_data:
        month = holiday_data["fixed_date"]["month"]
        day = holiday_data["fixed_date"]["day"]
        return get_fixed_date(year, month, day)
    #special holidays
    elif holiday == Holiday.EASTER: return get_easter(year)
    elif holiday == Holiday.ADVENT_START: return get_advent_start(year)
    elif holiday == (Holiday.THANKSGIVING): return get_thanksgiving(year)
    elif holiday == (Holiday.THANKSGIVING_CA): return get_thanksgiving(year, True)
    raise ValueError(f"Unrecognized or unsupported holiday rule for: {holiday}")

#debug

def debug_holidays(year):
    print(f"Liturgical calendar for {year}:\n")
    for holiday in Holiday:
        try:
            holiday_date = get_holiday(year, holiday)
            print(f"{holiday.name.replace('_', ' ').title()}: {holiday_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{holiday.name.replace('_', ' ').title()}: Error - {e}")

year = int(input("Enter the year for which you want to debug holidays: "))
debug_holidays(year)