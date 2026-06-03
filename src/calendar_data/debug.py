"""Debug and interactive CLI for the liturgical calendar."""

import os
import sys

from .utilities import CalendarRules
from .western.western_functions import western_functiond

class CalendarDisplay:
    """Handles display and debugging of calendar information."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarDisplay.
        
        Parameters:
            calendar (WesternCalendar, optional): Calendar instance.
            rules_manager (CalendarRules, optional): Rules manager instance.
        """
        self.calendar = calendar or western_functiond()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def display_holidays(self, year, tradition, flags):
        """Display all holidays for a given year and tradition."""
        print(f"{tradition} liturgical holidays for A.D. {year}:")
        rules = self.rules_manager.get_rules('dates', tradition, flags)
        
        for holiday_key, holiday_data in rules.items():
            try:
                holiday_date = self.calendar.get_holiday(year, holiday_key, tradition, flags)
                holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
                alt_name = holiday_data.get("alt_name")
                if alt_name:
                    holiday_name += f" ({alt_name})"
                print(f"{holiday_name}: {holiday_date.strftime('%A, %B %d, %Y')}")
            except ValueError as e:
                print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")
    
    def display_seasons(self, year, tradition, flags):
        """Display all seasons for a given year and tradition."""
        print(f"{tradition} liturgical seasons for A.D. {year}:")
        rules = self.rules_manager.get_rules('seasons', tradition, flags)
        
        all_seasons = []
        
        for season_key, season_data in rules.items():
            try:
                season_ranges = self.calendar.get_season(year, season_key, tradition, flags)
                for start_date, end_date in season_ranges:
                    season_name = season_data.get("name", season_key.replace('_', ' ').title())
                    alt_name = season_data.get("alt_name")
                    if alt_name:
                        season_name += f" ({alt_name})"
                    all_seasons.append((start_date, end_date, season_name))
            except ValueError as e:
                print(f"{season_key.replace('_', ' ').title()}: Error - {e}")
        
        # Sort by start date
        all_seasons.sort(key=lambda x: x[0])
        
        for start_date, end_date, season_name in all_seasons:
            print(f"{season_name}: {start_date.strftime('%A, %B %d, %Y')} - {end_date.strftime('%A, %B %d, %Y')}")
    
    def display_saints(self, year, tradition, flags):
        """Display all saints for a given year and tradition."""
        print(f"{tradition} saints for A.D. {year}:")
        rules = self.rules_manager.get_rules('saints', tradition, flags)
        
        for saint_key, saint_data in rules.items():
            try:
                saint_date = self.calendar.get_saint(year, saint_key, tradition, flags)
                saint_name = saint_data.get("name", saint_key.replace('_', ' ').title())
                alt_name = saint_data.get("alt_name")
                if alt_name:
                    saint_name += f" ({alt_name})"
                print(f"{saint_name}: {saint_date.strftime('%A, %B %d, %Y')}")
            except ValueError as e:
                print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")


class CalendarInteractive:
    """Handles interactive CLI for calendar generation and display."""
    
    def __init__(self, culture='western'):
        """
        Initialize the interactive calendar interface.
        
        Parameters:
            culture (str): The culture (e.g., "western", "eastern")
        """
        self.culture = culture
        self.calendar = western_functiond()
        self.rules_manager = CalendarRules(culture)
        self.display = CalendarDisplay(self.calendar, self.rules_manager)
        self.generator = CalendarGenerator(self.calendar, self.rules_manager)
    
    def prompt_for_year(self):
        """Prompt user for a year and return it."""
        while True:
            try:
                year = int(input("Enter the year for which you want to display the church calendar: ").strip())
                return year
            except ValueError:
                print("Invalid year. Please enter a valid year.")
    
    def prompt_for_tradition(self):
        """Prompt user for a tradition and return it."""
        available_traditions = [
            d for d in os.listdir(self.culture)
            if os.path.isdir(os.path.join(self.culture, d))
        ]
        print(f"Available traditions: {', '.join(available_traditions)}")
        
        while True:
            tradition = input("Enter a tradition: ").strip().lower()
            if tradition in available_traditions:
                return tradition
            print("Invalid tradition. Please select from the available options.")
    
    def prompt_for_flags(self, rule_type, tradition):
        """Prompt user for file flags and return them."""
        base_path = os.path.join(self.culture, tradition)
        files = [
            f for f in os.listdir(base_path)
            if f.startswith(rule_type) and f.endswith(".json")
        ]
        
        if not files:
            raise ValueError(f"No {rule_type} files found in {base_path}")
        
        print(f"\nAvailable {rule_type} options:")
        options = {}
        for file in files:
            flags = file[len(rule_type):-5].strip("_") or "none"
            options[flags] = file
            print(f" - {file} (flags: {flags})")
        
        selected_flag = input(f"Enter the desired {rule_type} file (or leave blank for default): ").strip()
        return selected_flag if selected_flag else None
    
    def run(self):
        """Run the interactive calendar interface."""
        print("=== Liturgical Calendar Generator ===\n")
        
        year = self.prompt_for_year()
        
        print("\nChoose a calendar tradition and file for dates and seasons.")
        tradition = self.prompt_for_tradition()
        
        dates_file = self.prompt_for_flags("dates", tradition)
        seasons_file = self.prompt_for_flags("seasons", tradition)
        saints_file = self.prompt_for_flags("saints", tradition)
        lectionary = self.prompt_for_flags("lectionary", tradition)
        
        csv_output = input("\nWould you like to output a CSV file? (yes/no): ").strip().lower() == "yes"
        
        # Generate and display calendar
        print("\nGenerating the liturgical calendar...\n")
        try:
            self.display.display_holidays(year, tradition, dates_file)
            print()
            self.display.display_seasons(year, tradition, seasons_file)
            print()
            self.display.display_saints(year, tradition, saints_file)
            
            if csv_output:
                output_file = f"liturgical_calendar_{year}.csv"
                self.generator.generate_calendar_csv(year, tradition, dates_file, output_file)
                print(f"\nLiturgical calendar for {year} has been written to {output_file}.")
        except ValueError as e:
            print(f"Error: {e}")


# Legacy function exports for backwards compatibility
def display_holidays(year, tradition, flags):
    """Legacy function - use CalendarDisplay.display_holidays() instead."""
    display = CalendarDisplay()
    display.display_holidays(year, tradition, flags)


def display_seasons(year, tradition, flags):
    """Legacy function - use CalendarDisplay.display_seasons() instead."""
    display = CalendarDisplay()
    display.display_seasons(year, tradition, flags)


def display_saints(year, tradition, flags):
    """Legacy function - use CalendarDisplay.display_saints() instead."""
    display = CalendarDisplay()
    display.display_saints(year, tradition, flags)


def prompt_for_flags(rule_type, tradition, culture="western"):
    """Legacy function - use CalendarInteractive.prompt_for_flags() instead."""
    interactive = CalendarInteractive(culture)
    return interactive.prompt_for_flags(rule_type, tradition)


if __name__ == "__main__":
    interactive = CalendarInteractive('western')
    interactive.run()