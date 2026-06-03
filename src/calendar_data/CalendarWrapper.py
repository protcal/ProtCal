'''API wrapper for traditions functions'''
from .Utilities import CalendarRules
from .western.WesternCalendar import WesternCalendar

class CalendarWrapper:
    """Wrapper for calendar functions across traditions."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarWrapper.
        """

        self.calendar = calendar or WesternCalendar()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def get_holiday(self, year, holiday_key, tradition='western', flags=None):
        """Get the date of a specific holiday."""
        return self.calendar.get_holiday(year, holiday_key, tradition, flags)
    
    def get_season(self, year, season_key, tradition='western', flags=None):
        """Get the date range of a specific season."""
        return self.calendar.get_season(year, season_key, tradition, flags)
    
    def get_saint(self, year, saint_key, tradition, flags=None):
        """Get the date of a specific saint's day."""
        return self.calendar.get_saint(year, saint_key, tradition, flags)
