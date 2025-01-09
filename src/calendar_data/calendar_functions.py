from datetime import date, timedelta
from utilities import get_rules, calculate_offset, get_closest_sunday

#specific holiday functions for complex holiday calculations

def get_easter(year):
    """
    Performs the computus paschalis formula to get Easter. 
    Returns the date of Easter
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
    Returns the date of the start of advent.
    """
    christmas = date(year, 12, 25)
    fourth_sunday_before_christmas = christmas - timedelta(days=(christmas.weekday() + 22) % 7)
    advent_start = fourth_sunday_before_christmas - timedelta(weeks=3)
    return advent_start

def get_thanksgiving(year, canada = False):
    """
    Finds the day of thanksgiving in Canada and the USA
    Returns the date of Thanksgiving depending on which North American country
    """
    if canada:
        first_day = date(year, 10, 1)
        first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
        return first_monday + timedelta(weeks=1)
    first_day = date(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    return first_thursday + timedelta(weeks=3)

#these getter functions find the data of a specific holiday, season or saint in the JSON files

def get_holiday(year, holiday, tradition, flags):
    """
    Given the name of the holiday, determines the date it is on
    depending on the given year.
    Returns the date of the holiday
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
    Returns a list unlike any other getter due to cross-year holy days
    Depending on if it is cross-year, it will return one element in the list or (normally) two.
    """
    rules = get_rules("seasons", tradition, flags)
    season_data = rules.get(season)

    if not season_data:
        raise ValueError(f"Unrecognized or unsupported season rules for: {season}")

    start_day = get_holiday(year, season_data["start"], tradition, flags)
    end_day = get_holiday(year, season_data["end"], tradition, flags)

    if season_data.get("offset", False): #end of a season is the start of another season
        end_day -= timedelta(days=1)
    
    #handle cross-year holy days. Good luck figuring this out. I did this on lots of caffeine.
    if start_day > end_day:
        if season_data["cross-year"]: #kinda dumb since all start_day > end_day have cross-year, but maybe not always
            prior_year_end_day = end_day.replace(year=year)
            prior_year_start_day = start_day.replace(year=year - 1)
        end_day = end_day.replace(year=year + 1)
        return [
            (prior_year_start_day, prior_year_end_day),
            (start_day, end_day)
        ]

    return [(start_day, end_day)]

def get_saint(year, saint, tradition, flags):
    """
    Gets the name and date for a saint 
    Returns only the date of a saint (for now)
    """
    rules = get_rules("saints", tradition, flags)
    saint_data = rules.get(saint)
    return date(year, saint_data["month"], saint_data["day"])
