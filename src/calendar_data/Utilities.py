import json
import os
from datetime import date, timedelta

class CalendarRules:
    """Manages loading and caching of liturgical rules from JSON files."""
    
    def __init__(self, culture='western'):
        """
        Initialize the CalendarRules manager.
        """

        self.culture = culture
        self._cache = {}
    
    def get_rules(self, rule_type, tradition='lutheran', flags=None):
        """
        Gets the liturgical rules from a JSON file.
        """

        cache_key = (rule_type, tradition, flags)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        file_name = f"{rule_type}_{flags}.json" if flags else f"{rule_type}.json"
        file_path = os.path.join(self.culture, tradition, file_name)
        
        try:
            with open(file_path, 'r') as f:
                rules = json.load(f)
            result = rules.get(rule_type, {})
            self._cache[cache_key] = result
            return result
        except FileNotFoundError:
            raise ValueError(f"Rules file not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in rules file: {file_path}")
    
    def clear_cache(self):
        """Clear the rules cache."""
        self._cache.clear()


class DateCalculator:
    """Utility class for date calculations."""
    
    @staticmethod
    def calculate_offset(base_date, offset_days):
        """
        Calculate a date offset.
        """

        return base_date + timedelta(days=offset_days)
    
    @staticmethod
    def get_closest_sunday(holiday):
        """
        Find the closest Sunday to the given holiday.
        
        If the holiday is already a Sunday, returns the same date.
        """

        days_to_previous_sunday = -holiday.weekday() % 7
        days_to_next_sunday = (6 - holiday.weekday()) % 7
        
        if abs(days_to_previous_sunday) <= abs(days_to_next_sunday):
            return DateCalculator.calculate_offset(holiday, days_to_previous_sunday)
        else:
            return DateCalculator.calculate_offset(holiday, days_to_next_sunday)
