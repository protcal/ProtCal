import csv
from datetime import date, timedelta
from utilities import get_rules
from calendar_functions import get_holiday, get_season, get_saint

def generate_calendar_csv(year, tradition, flags, output_file):
    """
    Generates a CSV file containing the liturgical calendar for the given year.
    """
    #init empty calendar
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    calendar = []

    current_date = start_date
    while current_date <= end_date:
        calendar.append({"date": current_date, "holiday": None, "season": None, "saint": None})
        current_date += timedelta(days=1)

    place_holidays(calendar, year, tradition, flags)
    place_seasons(calendar, year, tradition, flags)
    place_saints(calendar, year, tradition, flags)

    #write
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

def place_holidays(calendar, year, tradition, flags):
    """
    Adds holidays to the calendar
    """
    rules = get_rules("dates", tradition, flags)

    for holiday_key, holiday_data in rules.items():
        try:
            holiday_date = get_holiday(year, holiday_key, tradition, flags)
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

def place_seasons(calendar, year, tradition, flags):
    """
    Adds seasons to the calendar
    """
    rules = get_rules("seasons", tradition, flags)

    for season_key, season_data in rules.items():
        try:
            season_ranges = get_season(year, season_key, tradition, flags)
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

def place_saints(calendar, year, tradition, flags):
    """
    Adds saints to the calendar
    """
    rules = get_rules("saints", tradition, flags)

    for saint_key, saint_data in rules.items():
        try:
            saint_date = get_saint(year, saint_key, tradition, flags)
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