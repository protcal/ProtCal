import csv
from datetime import date, timedelta
from calendar_functions import get_holiday
from utilities import get_rules

def generate_calendar(year, tradition, flags):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    rules = get_rules("days", tradition, flags)

    holidays = {}
    for holiday_key in rules.keys():
        try:
            holidays[holiday_key] = get_holiday(year, holiday_key, tradition, flags)
        except ValueError as e:
            print(f"Error generating date for {holiday_key}: {e}")

    calendar = []
    current_date = start_date
    while current_date <= end_date:
        day_entry = {
            "date": current_date,
            "holiday": None
        }

        for holiday_key, holiday_date in holidays.items():
            if current_date == holiday_date:
                holiday_name = rules[holiday_key].get("name", holiday_key.replace('_', ' ').title())
                day_entry["holiday"] = holiday_name
                break

        calendar.append(day_entry)
        current_date += timedelta(days=1)

    return calendar

def write_calendar_to_csv(calendar, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Holiday"])

        for entry in calendar:
            writer.writerow([
                entry["date"].strftime('%Y-%m-%d'),
                entry["holiday"] or ""
            ])
