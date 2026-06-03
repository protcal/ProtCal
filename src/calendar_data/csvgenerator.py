"""Calendar CSV generation module."""

import csv
from datetime import date, timedelta

# Support both module import and direct execution
try:
    from .utilities import CalendarRules
    from .western.western_functions import WesternCalendar
except ImportError:
    # Fallback for direct script execution
    from utilities import CalendarRules
    from western.western_functions import WesternCalendar


class CalendarGenerator:
    """Generates liturgical calendars in various formats."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarGenerator.
        
        Parameters:
            calendar (WesternCalendar, optional): Calendar instance. If None, creates new instance.
            rules_manager (CalendarRules, optional): Rules manager. If None, creates new instance.
        """
        self.calendar = calendar or WesternCalendar()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def generate_calendar_csv(self, year, tradition, flags, output_file):
        """
        Generate a CSV file containing the liturgical calendar for the given year.
        
        Parameters:
            year (int): The year
            tradition (str): The tradition (e.g., "lutheran", "anglican")
            flags (str, optional): Additional flags for rule selection
            output_file (str): Path to the output CSV file
        """
        # Initialize empty calendar
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        calendar = []
        
        current_date = start_date
        while current_date <= end_date:
            calendar.append({
                "date": current_date,
                "holiday": None,
                "season": None,
                "saint": None
            })
            current_date += timedelta(days=1)
        
        # Populate calendar with data
        self._place_holidays(calendar, year, tradition, flags)
        self._place_seasons(calendar, year, tradition, flags)
        self._place_saints(calendar, year, tradition, flags)
        
        # Write to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Holiday", "Season", "Saint"])
            
            for entry in calendar:
                writer.writerow([
                    entry["date"].strftime('%Y-%m-%d'),
                    entry["holiday"] or "",
                    entry["season"] or "",
                    entry["saint"] or ""
                ])
    
    def _place_holidays(self, calendar, year, tradition, flags):
        """Place holidays in the calendar."""
        rules = self.rules_manager.get_rules('dates', tradition, flags)
        
        for holiday_key, holiday_data in rules.items():
            try:
                holiday_date = self.calendar.get_holiday(year, holiday_key, tradition, flags)
                holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
                alt_name = holiday_data.get("alt_name")
                if alt_name:
                    holiday_name += f" ({alt_name})"
                
                for entry in calendar:
                    if entry["date"] == holiday_date:
                        entry["holiday"] = holiday_name
                        break
            except ValueError as e:
                print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")
    
    def _place_seasons(self, calendar, year, tradition, flags):
        """Place seasons in the calendar."""
        rules = self.rules_manager.get_rules('seasons', tradition, flags)
        
        for season_key, season_data in rules.items():
            try:
                season_ranges = self.calendar.get_season(year, season_key, tradition, flags)
                season_name = season_data.get("name", season_key.replace('_', ' ').title())
                alt_name = season_data.get("alt_name")
                if alt_name:
                    season_name += f" ({alt_name})"
                
                for start_date, end_date in season_ranges:
                    for entry in calendar:
                        if start_date <= entry["date"] <= end_date:
                            entry["season"] = season_name
            except ValueError as e:
                print(f"{season_key.replace('_', ' ').title()}: Error - {e}")
    
    def _place_saints(self, calendar, year, tradition, flags):
        """Place saints in the calendar."""
        rules = self.rules_manager.get_rules('saints', tradition, flags)
        
        for saint_key, saint_data in rules.items():
            try:
                saint_date = self.calendar.get_saint(year, saint_key, tradition, flags)
                saint_name = saint_data.get("name")
                alt_name = saint_data.get("alt_name")
                if alt_name:
                    saint_name += f" ({alt_name})"
                
                for entry in calendar:
                    if entry["date"] == saint_date:
                        entry["saint"] = saint_name
                        break
            except ValueError as e:
                print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")


# Legacy function exports for backwards compatibility
def generate_calendar_csv(year, tradition, flags, output_file):
    """Legacy function - use CalendarGenerator.generate_calendar_csv() instead."""
    generator = CalendarGenerator()
    generator.generate_calendar_csv(year, tradition, flags, output_file)