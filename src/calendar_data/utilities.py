import json
import os
from datetime import date, timedelta

def get_rules(type, tradition = 'lutheran', flags=None, culture = 'western'):
    """
    Gets the liturgical rules from a JSON file.
    Parameters:
        type (str): The type of rules to fetch (dates.json or seasons.json or saints.json?)
        tradition (str): The tradition directory to look in (e.g., "lutheran", "anglican")
        flags (str, optional): An additional flag for file selection (e.g., "oneyear" for dates_oneyear.json)
    Returns:
        dict: The requested liturgical rules.
    """
    file_name = f"{type}_{flags}.json" if flags else f"{type}.json"
    file_path = os.path.join(culture, tradition, file_name)
    
    try:
        with open(file_path, 'r') as f:
            rules = json.load(f)
        return rules.get(type, {})
    except FileNotFoundError:
        raise ValueError(f"Rules file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in rules file: {file_path}")


def calculate_offset(base_date, offset_days):
    """
    Helper function that calculates date offets.
    """
    return base_date + timedelta(days=offset_days)

def get_fixed_date(year, month, day):
    """
    Helper function to return the fixed date of a given holiday.
    """
    return date(year, month, day)

def get_closest_sunday(holiday):
    """
    Finds the closest Sunday to the given holiday. If the holiday is already a Sunday,
    it returns the same date.
    """
    days_to_previous_sunday = -holiday.weekday() % 7
    days_to_next_sunday = (6 - holiday.weekday()) % 7

    if abs(days_to_previous_sunday) <= abs(days_to_next_sunday):
        return calculate_offset(holiday, days_to_previous_sunday)
    else:
        return calculate_offset(holiday, days_to_next_sunday)