import json
import os
from datetime import date, timedelta


class CalendarRules:
    """Manages loading and caching of liturgical rules from JSON files."""
    
    def __init__(self, culture='western'):
        """
        Initialize the CalendarRules manager.
        
        Parameters:
            culture (str): The culture directory (e.g., "western", "eastern")
        """
        self.culture = culture
        self._cache = {}
    
    def get_rules(self, rule_type, tradition='lutheran', flags=None):
        """
        Gets the liturgical rules from a JSON file.
        
        Parameters:
            rule_type (str): The type of rules to fetch (dates, seasons, saints, lectionary)
            tradition (str): The tradition directory to look in (e.g., "lutheran", "anglican")
            flags (str, optional): An additional flag for file selection (e.g., "oneyear")
        
        Returns:
            dict: The requested liturgical rules.
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
        
        Parameters:
            base_date (date): The base date
            offset_days (int): Number of days to offset
        
        Returns:
            date: The offset date
        """
        return base_date + timedelta(days=offset_days)
    
    @staticmethod
    def get_closest_sunday(holiday):
        """
        Find the closest Sunday to the given holiday.
        
        If the holiday is already a Sunday, returns the same date.
        
        Parameters:
            holiday (date): The reference date
        
        Returns:
            date: The closest Sunday
        """
        days_to_previous_sunday = -holiday.weekday() % 7
        days_to_next_sunday = (6 - holiday.weekday()) % 7
        
        if abs(days_to_previous_sunday) <= abs(days_to_next_sunday):
            return DateCalculator.calculate_offset(holiday, days_to_previous_sunday)
        else:
            return DateCalculator.calculate_offset(holiday, days_to_next_sunday)


# Legacy function exports for backwards compatibility
def get_rules(type, tradition='lutheran', flags=None, culture='western'):
    """Legacy function - use CalendarRules class instead."""
    manager = CalendarRules(culture)
    return manager.get_rules(type, tradition, flags)


def calculate_offset(base_date, offset_days):
    """Legacy function - use DateCalculator.calculate_offset() instead."""
    return DateCalculator.calculate_offset(base_date, offset_days)


def get_closest_sunday(holiday):
    """Legacy function - use DateCalculator.get_closest_sunday() instead."""
    return DateCalculator.get_closest_sunday(holiday)