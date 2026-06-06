'''API wrapper for traditions functions'''
from .Utilities import CalendarRules, CalendarContext
from .western.WesternCalendar import WesternCalendar

class CalendarWrapper:
    """Wrapper for calendar functions across traditions."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarWrapper.
        """

        # TODO: Constructor must determine which calendar to construct based on calendar magic string
        # TODO: Should not construct calendar on magic strings
        self.calendar = WesternCalendar()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def get_holiday(self, context, holiday_key):
        """Get the date of a specific holiday."""
        return self.calendar.get_holiday(context, holiday_key)
    
    def get_season(self, context, season_key):
        """Get the date range of a specific season."""

        #TODO: end_date in seasons that cross over to the next year are in the current year, need to add year rollover logic 
        return self.calendar.get_season(context, season_key)
    
    def get_saint(self, context, saint_key):
        """Get the date of a specific saint's day."""
        return self.calendar.get_saint(context, saint_key)
   
    def get_all_holidays(self, context, rules):
        """Gets all the holidays in a list"""

        all_holidays = []
        for holiday_key, holiday_data in rules.items():
            try:
                holiday_date = self.calendar.get_holiday(context, holiday_key)
                holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
                alt_name = holiday_data.get("alt_name")
                if alt_name:
                    holiday_name += f" ({alt_name})"
                all_holidays.append((holiday_name, holiday_date))
            except ValueError as e:
                raise ValueError(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")

        return all_holidays
    
    def get_all_seasons(self, context, rules):

        all_seasons = []
        for season_key, season_data in rules.items():
            try:
                season_ranges = self.calendar.get_season(context, season_key)
                for start_date, end_date in season_ranges:
                    season_name = season_data.get("name", season_key.replace('_', ' ').title())
                    alt_name = season_data.get("alt_name")
                    if alt_name:
                        season_name += f" ({alt_name})"
                    all_seasons.append((season_name, start_date, end_date))
            except ValueError as e:
                print(f"{season_key.replace('_', ' ').title()}: Error - {e}")
        return all_seasons

    def get_all_saints(self, context, rules):

        all_saints = []
        for saint_key, saint_data in rules.items():
            try:
                saint_date = self.calendar.get_saint(context, saint_key)
                saint_name = saint_data.get("name", saint_key.replace('_', ' ').title())
                alt_name = saint_data.get("alt_name")
                if alt_name:
                    saint_name += f" ({alt_name})"
                all_saints.append((saint_name, saint_date))
            except ValueError as e:
                print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")
        return all_saints