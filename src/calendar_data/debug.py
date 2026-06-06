"""Debug and interactive CLI for the liturgical calendar."""

import os
import sys
sys.path.insert(0, '..') #necessary since this is always run as a script for debugging

from calendar_data.Utilities import CalendarRules, CalendarContext, RuleType
from calendar_data.CalendarWrapper import CalendarWrapper

class CalendarDisplay:
    """Handles display and debugging of calendar information."""
    
    def __init__(self, calendar=None, rules_manager=None):
        """
        Initialize the CalendarDisplay.
        """
        
        self.calendar = calendar or CalendarWrapper()
        self.rules_manager = rules_manager or CalendarRules('western')
    
    def display_holidays(self, context):
        """Display all holidays for a given context."""
        print(f"{context.tradition} liturgical holidays for A.D. {context.year}:")
        rules = self.rules_manager.get_rules(RuleType.DATES, context)

        holiday_list = self.calendar.get_all_holidays(context, rules)
        for holiday_name, holiday_date in holiday_list:
            print(f"{holiday_name}: {holiday_date.strftime('%A, %B %d, %Y')}")
    
    def display_seasons(self, context):
        """Display all seasons for a given context."""
        print(f"{context.tradition} liturgical seasons for A.D. {context.year}:")
        rules = self.rules_manager.get_rules(RuleType.SEASONS, context)
        
        all_seasons = self.calendar.get_all_seasons(context, rules)

        # Sort by start date
        all_seasons.sort(key=lambda x: x[1])
        
        for season_name, start_date, end_date in all_seasons:
            print(f"{season_name}: {start_date.strftime('%A, %B %d, %Y')} - {end_date.strftime('%A, %B %d, %Y')}")
    
    def display_saints(self, context):
        """Display all saints for a given context."""
        print(f"{context.tradition} saints for A.D. {context.year}:")
        rules = self.rules_manager.get_rules(RuleType.SAINTS, context)
        
        all_saints = self.calendar.get_all_saints(context, rules)

        for saint_name, saint_date in all_saints:
            print(f"{saint_name}: {saint_date.strftime('%A, %B %d, %Y')}")


class CalendarInteractive:
    """Handles interactive CLI for calendar generation and display."""
    
    def __init__(self, culture='western'):
        """
        Initialize the interactive calendar interface.
        
        Parameters:
            culture (str): The culture (e.g., "western", "eastern")
        """
        self.culture = culture
        self.rules_manager = CalendarRules(culture)
        self.calendar = CalendarWrapper('western', self.rules_manager)
        self.display = CalendarDisplay(self.calendar, self.rules_manager)
    
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
                
        # Generate and display calendar
        print("\nGenerating the liturgical calendar...\n")
        try:
            context_dates = CalendarContext(year, tradition, dates_file)
            context_seasons = CalendarContext(year, tradition, seasons_file)
            context_saints = CalendarContext(year, tradition, saints_file)
            
            self.display.display_holidays(context_dates)
            print()
            self.display.display_seasons(context_seasons)
            print()
            self.display.display_saints(context_saints)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interactive = CalendarInteractive('western')
    interactive.run()