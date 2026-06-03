"""Legacy compatibility wrapper.

This module provides backwards compatibility with older code.
For new code, use the class-based API from the specific modules:
- calendar_data.utilities.CalendarRules
- calendar_data.utilities.DateCalculator  
- calendar_data.western.western_functions.WesternCalendar
- calendar_data.csvgenerator.CalendarGenerator
- calendar_data.debug.CalendarDisplay
"""

# Support both module import and direct execution
try:
    from .western.western_functions import (
        get_easter,
        get_advent_start,
        get_thanksgiving,
        get_holiday,
        get_season,
        get_saint,
    )
except ImportError:
    # Fallback for direct script execution
    from western.western_functions import (
        get_easter,
        get_advent_start,
        get_thanksgiving,
        get_holiday,
        get_season,
        get_saint,
    )

__all__ = [
    "get_easter",
    "get_advent_start",
    "get_thanksgiving",
    "get_holiday",
    "get_season",
    "get_saint",
]

