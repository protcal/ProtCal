from calendar_functions import *
from utilities import * 
from csvgenerator import *

#debug functions

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

    all_seasons = [] #the reason a list is used here unlike any other display function is to print it sorted

    for season_key, season_data in rules.items():
        try:
            season_ranges = get_season(year, season_key, tradition, flags)
            for start_date, end_date in season_ranges:
                season_name = season_data.get("name", season_key.replace('_', ' ').title())
                alt_name = season_data.get("alt_name")
                if alt_name:
                    season_name += f" ({alt_name})"
                all_seasons.append((start_date, end_date, season_name))
        except ValueError as e:
            print(f"{season_key.replace('_', ' ').title()}: Error - {e}")

    #sort
    all_seasons.sort(key=lambda x: x[0])

    for start_date, end_date, season_name in all_seasons:
        print(f"{season_name}: {start_date.strftime('%A, %B %d, %Y')} - {end_date.strftime('%A, %B %d, %Y')}")


def display_saints(year, tradition, flags):
    """
    Displays the saints on a command prompt when run. This is
    useful for debugging purposes.
    """
    print(f"{tradition} saints for A.D. {year}:")

    rules = get_rules("saints", tradition, flags)

    for saint_key, saint_data in rules.items():
        try:
            saint_date = get_saint(year, saint_key, tradition, flags)
            saint_name = rules.get("name", saint_key.replace('_', ' ').title())
            alt_name = saint_data.get("alt_name") #never used with saints as of now
            if alt_name:
                name += f" ({alt_name})"
            print(f"{saint_name}: {saint_date.strftime('%A, %B %d, %Y')}")
        except ValueError as e:
            print(f"{saint_key.replace('_', ' ').title()}: Error - {e}")

def prompt_for_flags(type, tradition, culture="western"):
    """
    Prompts the user for a file based on the available options in the specified tradition folder.
    Returns the file with chosen flags
    """
    base_path = os.path.join(culture, tradition)
    files = [f for f in os.listdir(base_path) if f.startswith(type) and f.endswith(".json")]

    if not files:
        raise ValueError(f"No {type} files found in {base_path}")

    print(f"Available {type} options:")
    options = {}
    for file in files:
        flags = file[len(type):-5].strip("_") or "none"
        options[flags] = file
        print(f" - {file} (flags: {flags})")

    selected_flag = input(f"Enter the desired {type} file (or leave blank for default): ").strip()
    return selected_flag if selected_flag else None

if __name__ == "__main__":
    while True:
        try:
            year = int(input("Enter the year for which you want to display the church calendar: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a valid year.")

    print("\nChoose a calendar tradition and file for dates and seasons.")
    culture = "western" #In the future, we will have to prompt for either western or eastern
    available_traditions = [d for d in os.listdir(culture) if os.path.isdir(os.path.join(culture, d))]
    print(f"Available traditions: {', '.join(available_traditions)}")
    
    while True:
        tradition = input("Enter a tradition: ").strip().lower()
        if tradition in available_traditions:
            break
        print("Invalid tradition. Please select from the available options.")

    dates_file = prompt_for_flags("dates", tradition, culture)
    seasons_file = prompt_for_flags("seasons", tradition, culture)

    # Step 3: Saints file
    print("\nStep 3: Choose a file for the saints.")
    saints_file = prompt_for_flags("saints", tradition, culture)

    # Step 4: Lectionary file
    print("\nStep 4: Choose a file for the lectionary.")
    lectionary = prompt_for_flags("lectionary", tradition, culture)

    # Step 5: CSV output
    csv_output = input("\nWould you like to output a CSV file? (yes/no): ").strip().lower() == "yes"

    # Generate calendar
    print("\nGenerating the liturgical calendar...")
    try:
        display_holidays(year, tradition, dates_file)
        print()
        display_seasons(year, tradition, seasons_file)
        print()
        display_saints(year, tradition, saints_file)

        if csv_output:
            output_file = f"liturgical_calendar_{year}.csv"
            generate_calendar_csv(year, tradition, None, output_file)
            print(f"\nLiturgical calendar for {year} has been written to {output_file}.")
    except ValueError as e:
        print(f"Error: {e}")