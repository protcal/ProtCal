"""Western calendar tradition functions"""

from datetime import date, timedelta
from Utilities import DateCalculator, CalendarRules

class WesternCalendar:
    """Handles date calculations for the Western calendar tradition."""
    
    def __init__(self, rules_manager = None):
        """
        Initialize the WesternCalendar
        """
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def get_easter(self, year):
        """
        Calculate Easter Sunday using the computus paschalis formula
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
    
    def get_advent_start(self, year):
        """
        Find the start of Advent (4 Sundays before Christmas)
        """

        christmas = date(year, 12, 25)
        fourth_sunday_before_christmas = christmas - timedelta(days=(christmas.weekday() + 22) % 7)
        advent_start = fourth_sunday_before_christmas - timedelta(weeks=3)
        return advent_start
    
    def get_thanksgiving(self, year, canada = False):
        """
        Calculate Thanksgiving date
        """

        if canada:
            first_day = date(year, 10, 1)
            first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
            return first_monday + timedelta(weeks=1)
        
        first_day = date(year, 11, 1)
        first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
        return first_thursday + timedelta(weeks=3)
    
    def get_holiday(self, year, holiday_key, tradition, flags=None):
        """
        Get the date of a specific holiday based on rules
        """

        rules = self.rules_manager.get_rules('dates', tradition, flags)
        
        if holiday_key not in rules:
            raise ValueError(f"Holiday '{holiday_key}' not found in rules")
        
        holiday_rule = rules[holiday_key]
        
        # Handle complex holidays (Easter, Advent)
        if holiday_rule.get('complex'):
            if holiday_key == 'easter':
                return self.get_easter(year)
            elif holiday_key == 'advent_start':
                return self.get_advent_start(year)
            else:
                raise ValueError(f"Unknown complex holiday type: '{holiday_key}'")
        
        # Handle fixed date holidays (Christmas)
        if 'fixed_date' in holiday_rule:
            fixed = holiday_rule['fixed_date']
            return date(year, fixed['month'], fixed['day'])
        
        # Handle offset-based holidays (depend on another holiday, like Pentecost from Easter)
        if 'offset_days' in holiday_rule:
            depends_on = holiday_rule.get('depends_on')
            if not depends_on:
                raise ValueError(f"Holiday '{holiday_key}' has offset_days but no depends_on")
            
            base_date = self.get_holiday(year, depends_on, tradition, flags)
            offset = holiday_rule['offset_days']
            return DateCalculator.calculate_offset(base_date, offset)
        
        raise ValueError(f"Holiday '{holiday_key}' has no recognized rule structure")
    
    def get_season(self, year, season_key, tradition, flags=None):
        """
        Get the date range(s) for a liturgical season
        """

        rules = self.rules_manager.get_rules('seasons', tradition, flags)
        
        if season_key not in rules:
            raise ValueError(f"Season '{season_key}' not found in rules")
        
        season_rule = rules[season_key]
        start_holiday_key = season_rule.get('start')
        end_holiday_key = season_rule.get('end')
        
        if not start_holiday_key or not end_holiday_key:
            raise ValueError(f"Season '{season_key}' missing start or end holiday keys")
        
        start_date = self.get_holiday(year, start_holiday_key, tradition, flags)
        end_date = self.get_holiday(year, end_holiday_key, tradition, flags)
        
        return [(start_date, end_date)]
    
    def get_saint(self, year, saint_key, tradition, flags=None):
        """
        Get the date of a specific saint's day.
        """

        rules = self.rules_manager.get_rules('saints', tradition, flags)
        
        if saint_key not in rules:
            raise ValueError(f"Saint '{saint_key}' not found in rules")
        
        saint_rule = rules[saint_key]
        
        if saint_rule.get('type') == 'fixed':
            month = saint_rule.get('month')
            day = saint_rule.get('day')
            return date(year, month, day)
        
        else:
            raise ValueError(f"Unknown saint rule type for '{saint_key}'")