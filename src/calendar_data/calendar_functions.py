from datetime import date, timedelta
from utilities import get_rules, calculate_offset, get_closest_sunday

def get_easter(year):
    """
    Preforms the computus paschalis formula to get Easter. 
    """
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
    """
    Finds the start of Advent.
    """
    christmas = date(year, 12, 25)
    fourth_sunday_before_christmas = christmas - timedelta(days=(christmas.weekday() + 22) % 7)
    advent_start = fourth_sunday_before_christmas - timedelta(weeks=3)
    return advent_start

def get_thanksgiving(year, canada=False):
    """
    Returns the date of Thanksgiving depending on which North American country
    """
    if canada:
        first_day = date(year, 10, 1)
        first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
        return first_monday + timedelta(weeks=1)
    first_day = date(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    return first_thursday + timedelta(weeks=3)

def get_holiday(year, holiday, tradition, flags):
    """
    Given the name of the holiday, determines the date it is on
    depending on the given year.
    """
    rules = get_rules("dates", tradition, flags)
    holiday_data = rules.get(holiday)

    if not holiday_data:
        raise ValueError(f"Unrecognized or unsupported holiday rule for: {holiday}")

    #Dependent holidays
    if "depends_on" in holiday_data:
        base_holiday = holiday_data["depends_on"]
        base_date = get_holiday(year, base_holiday, tradition, flags)
        offset_days = holiday_data.get("offset_days", 0)
        return calculate_offset(base_date, offset_days)

    #Fixed holidays
    elif "fixed_date" in holiday_data:
        month = holiday_data["fixed_date"]["month"]
        day = holiday_data["fixed_date"]["day"]
        return date(year, month, day)

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

def get_season(year, season, tradition, flags):
    """
    Depending on the year, determines the liturgical seasons for that year
    """
    rules = get_rules("seasons", tradition, flags)

    season_data = rules.get(season)

    if not season_data:
        raise ValueError(f"Unrecognized or unsupported season rules for: {season}")
    
    start_day = get_holiday(year, season_data["start"], tradition, flags)
    end_day = get_holiday(year, season_data["end"], tradition, flags)

    if start_day > end_day: #if the start date is after the end date, then it is the prior year (christmastide)
        end_day = end_day.replace(year=year + 1)

    if season_data.get("offset", False): #end of a season is the start of another season
        end_day -= timedelta(days=1)

    return start_day, end_day

def get_saint(year, saint, tradition, flags):
    """
    Gets the name and date for a saint 
    """
    rules = get_rules("saints", tradition, flags)
    saint_data = rules.get(saint)
    return saint_data["name"], date(year, saint_data["month"], saint_data["day"])

#debug tools. TODO: Refactor this into debug.py once .csv is fully working, but leave it here for now

#TODO: Add flags to the input of each of these functions so it shows in the cmd title
#TODO: Refactor all of these into just one big monolithic function

def display_holidays(year, tradition, flags):
    """
    Displays the holidays on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} liturgical holidays for A.D. {year}:")
    rules = get_rules("dates", tradition, flags)

    for holiday_key, holiday_data in rules.items():
        try:
            holiday_date = get_holiday(year, holiday_key, tradition, flags)
            holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
            alt_name = holiday_data.get("alt_name")
            if alt_name:
                holiday_name += f" ({alt_name})"
            print(f"{holiday_name}: {holiday_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")

def display_seasons(year, tradition, flags):
    """
    Displays the seasons on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} liturgical seasons for A.D. {year}:")

    rules = get_rules("seasons", tradition, flags)

    for season_key, season_data in rules.items():
        try:
            start_date, end_date = get_season(year, season_key, tradition, flags)
            season_name = season_data.get("name", season_key.replace('_', ' ').title())
            alt_name = season_data.get("alt_name")
            if alt_name:
                season_name += f" ({alt_name})"
            print(f"{season_name}: {start_date.strftime('%A, %B %d, %Y')} - {end_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{season_key.replace('_', ' ').title()}: Error - {e}")

def display_saints(year, tradition, flags):
    """
    Displays the saints on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} saints for A.D. {year}:")

    rules = get_rules("saints", tradition, flags)

    for saint_key, saint_data in rules.items():
        try:
            name, date = get_saint(year, saint_key, tradition, flags)
            alt_name = saint_data.get("alt_name") #never used with saints as of now
            if alt_name:
                name += f" ({alt_name})"
            print(f"{name}: {date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")