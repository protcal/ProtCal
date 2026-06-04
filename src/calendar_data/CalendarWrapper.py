'''API wrapper for traditions functions'''
from .Utilities import CalendarRules, CalendarContext
from .western.WesternCalendar import WesternCalendar

class CalendarWrapper:
    """Wrapper for calendar functions across traditions."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarWrapper.
        """

        self.calendar = calendar or WesternCalendar()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def get_holiday(self, context, holiday_key):
        """Get the date of a specific holiday."""
        return self.calendar.get_holiday(context, holiday_key)
    
    def get_season(self, context, season_key):
        """Get the date range of a specific season."""
        return self.calendar.get_season(context, season_key)
    
    def get_saint(self, context, saint_key):
        """Get the date of a specific saint's day."""
        return self.calendar.get_saint(context, saint_key)
   
    def get_all_holidays(self, context, holiday_key):
        """Gets all the holidays in a list"""

        rules = self.rules_manager.get_rules('dates', context.tradition, context.flags)
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
                print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")

        return all_holidays
