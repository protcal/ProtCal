import json
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


class RuleType(str, Enum):
    """Explicit catalog of configured rule files.
    These are the values found in each culture and tradition."""

    DATES = 'dates'
    SEASONS = 'seasons'
    SAINTS = 'saints'
    LECTIONARY = 'lectionary'


@dataclass(frozen=True)
class RuleFileSpec:
    """Describe a concrete rules file to load for a tradition and variant.
    These are the """

    rule_type: RuleType
    tradition: str
    culture: str # TODO: Removed default western
    flags: Optional[str] = None

    @property
    def file_name(self) -> str:
        return f"{self.rule_type.value}_{self.flags}.json" if self.flags else f"{self.rule_type.value}.json"

    @property
    def file_path(self) -> Path:
        return Path(__file__).resolve().parent / self.culture / self.tradition / self.file_name


class CalendarContext:
    """Data transfer object for calendar query parameters."""
    
    def __init__(self, year, tradition='lutheran', flags=None):
        """
        Initialize the CalendarContext.
        
        Parameters:
            year (int): The year for calendar calculations
            tradition (str): The tradition (e.g., 'lutheran', 'roman')
            flags (str, optional): Flags to specify which rules file to use
        """
        self.year = year
        self.tradition = tradition
        self.flags = flags
    
    def __repr__(self):
        return f"CalendarContext(year={self.year}, tradition='{self.tradition}', flags={self.flags})"


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
        Load liturgical rules from a JSON file using an explicit rule-type descriptor.
        """

        normalized_rule_type = self.normalize_rule_type(rule_type)
        spec = RuleFileSpec(rule_type=normalized_rule_type, tradition=tradition, culture=self.culture, flags=flags)
        #TODO: Move above into constructor and instantiate all CalendarRule classes with this already done, so less crap to write

        cache_key = (spec.rule_type, tradition, flags)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            with spec.file_path.open('r', encoding='utf-8') as f:
                rules = json.load(f)
            result = rules.get(normalized_rule_type.value, {})
            self._cache[cache_key] = result
            return result
        except FileNotFoundError:
            raise ValueError(f"Rules file not found: {spec.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in rules file: {spec.file_path}")
        except Exception as e:
            raise ValueError(f"Error loading rules file {spec.file_path}: {e}")

    def normalize_rule_type(self, rule_type):
        """Convert plain strings to explicit RuleType values."""

        if isinstance(rule_type, RuleType):
            return rule_type

        try:
            return RuleType(rule_type)
        except ValueError as exc:
            valid = ', '.join(item.value for item in RuleType)
            raise ValueError(f"Unknown rule type '{rule_type}'. Expected one of: {valid}") from exc
        except Exception as e:
                raise ValueError(f"Error normalizing rule type {rule_type}: {e}")
        
    
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
