from datetime import date, timedelta

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