import json
from datetime import date, timedelta

def get_rules(type, oneyear = False):
    """
    Gets the liturgical rules from a JSON file 
    Type can either be "days" or "seasons"
    TODO: Make it generic so you can ask for which file to get
    instead of binary
    """
    rules_file = 'western/liturgical-rules-1year.json' if oneyear else 'western/liturgical-rules-3year.json'
    with open(rules_file, 'r') as f:
        rules= json.load(f)
    return rules.get(type, {})

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