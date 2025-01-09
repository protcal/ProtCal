from calendar_functions import *
from utilities import * 
from csvgenerator import *

#debug functions

#TODO: Add flags to the input of each of these functions so it shows in the cmd title (low priority - who cares?)
#TODO: Make these us the get_all_seasons(), get_all_saints(), and get_all_holidays()

def display_holidays(year, tradition, flags):
    """
    Displays the holidays on a command prompt when run. This is
    useful for debugging purposes.
    This does not work for cross-holidays in the opposite direction (Ex. Christmastide before Epiphany of given year)
    """
    print(f"{tradition} liturgical holidays for A.D. {year}:")
    rules = get_rules("dates", tradition, flags)

    for holiday_key, holiday_data in rules.items():
        try:
            holiday_date = get_holiday(year, holiday_key, tradition, flags)
            holiday_name = holiday_data.get("name", holiday_key.replace('_', ' ').title())
            alt_name = holiday_data.get("alt_name")
            if alt_name:
                holiday_name += f" ({alt_name})"
            print(f"{holiday_name}: {holiday_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{holiday_key.replace('_', ' ').title()}: Error - {e}")

def display_seasons(year, tradition, flags):
    """
    Displays the seasons on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} liturgical seasons for A.D. {year}:")

    rules = get_rules("seasons", tradition, flags)

    for season_key, season_data in rules.items():
        try:
            start_date, end_date = get_season(year, season_key, tradition, flags)
            season_name = season_data.get("name", season_key.replace('_', ' ').title())
            alt_name = season_data.get("alt_name")
            if alt_name:
                season_name += f" ({alt_name})"
            print(f"{season_name}: {start_date.strftime('%A, %B %d, %Y')} - {end_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{season_key.replace('_', ' ').title()}: Error - {e}")

def display_saints(year, tradition, flags):
    """
    Displays the saints on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} saints for A.D. {year}:")

    rules = get_rules("saints", tradition, flags)

    for saint_key, saint_data in rules.items():
        try:
            name, date = get_saint(year, saint_key, tradition, flags)
            alt_name = saint_data.get("alt_name") #never used with saints as of now
            if alt_name:
                name += f" ({alt_name})"
            print(f"{name}: {date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")

#debug main

if __name__ == "__main__":
    year = int(input("Enter the year for which you want to display the church calendar: "))    
    tradition = input("Put in the tradition you wish to use (default = lutheran): ").strip().lower()
    if not tradition:
        tradition = "lutheran"    
    flags = input("Insert any calendar flags here (ex: oneyear calendar): ").strip().lower()
    if not flags:
        flags = None
    #csv = input("Would you like to output a CSV file? (yes/no): ").strip().lower() == "yes"
    print()
    display_holidays(year, tradition, flags)
    print()
    display_seasons(year, tradition, flags)
    print()
    display_saints(year, tradition, flags)
    
    #if csv:
    #    output_file = f"liturgical_calendar_{year}.csv"
    #    calendar = generate_calendar_csv(year, tradition, flags, output_file)
    #    print(f"\nLiturgical calendar for {year} has been written to {output_file}.")