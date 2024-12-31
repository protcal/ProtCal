import json
from datetime import date, timedelta

#Utility

def calculate_offset(base_date, offset_days):
    return base_date + timedelta(days=offset_days)

def get_fixed_date(year, month, day):
    return date(year, month, day)

def get_sunday_of(holiday):
    # Useful for All Saints' Sunday and other holidays
    offset_days = (6 - holiday.weekday()) % 7
    return calculate_offset(holiday, offset_days)

#Liturgy

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
    holiday_data = rules.get(holiday)

    if not holiday_data:
        raise ValueError(f"Unrecognized or unsupported holiday rule for: {holiday}")

    #Dependent holidays
    if "depends_on" in holiday_data:
        base_holiday = holiday_data["depends_on"]
        base_date = get_holiday(year, base_holiday)
        offset_days = holiday_data.get("offset_days", 0)
        return calculate_offset(base_date, offset_days)

    #Fixed holidays
    elif "fixed_date" in holiday_data:
        month = holiday_data["fixed_date"]["month"]
        day = holiday_data["fixed_date"]["day"]
        return get_fixed_date(year, month, day)

    #Complicated holidays
    elif "complex" in holiday_data:
        if holiday == "easter":
            return get_easter(year)
        elif holiday == "advent_start":
            return get_advent_start(year)
        elif holiday == "thanksgiving":
            return get_thanksgiving(year)
        elif holiday == "thanksgiving_ca":
            return get_thanksgiving(year, True)
    else:
        raise ValueError(f"Complex holiday found without function for: {holiday}")

    raise ValueError(f"Unrecognized or unsupported holiday rule for: {holiday}")

#Debug function
def debug_holidays(year):
    print(f"Liturgical calendar for A.D. {year}:")
    with open('liturgical-rules.json', 'r') as f:
        rules = json.load(f)
    
    for holiday_key, holiday_data in rules.items():
        try:
            holiday_date = get_holiday(year, holiday_key)
            holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
            alt_name = holiday_data.get("alt_name")
            if alt_name:
                holiday_name += f" ({alt_name})"
            print(f"{holiday_name}: {holiday_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")

#IO Debug
year = int(input("Enter the year for which you want to debug holidays: "))
print()
debug_holidays(year)
