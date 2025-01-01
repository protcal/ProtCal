from westerndates import *
from csvgenerator import *

if __name__ == "__main__":
    year = int(input("Enter the year for which you want to display church holidays: "))
    oneyear = input("Use one-year lectionary rules? (yes/no): ").strip().lower() == "yes"
    csv = input("Would you like to output a CSV file? (yes/no): ").strip().lower() == "yes"
    print()
    display_holidays(year, True)
    if(csv):
        calendar = generate_calendar(year, oneyear)
        output_file = f"liturgical_calendar_{year}.csv"

        write_calendar_to_csv(calendar, output_file)
        print(f"\nLiturgical calendar for {year} has been written to {output_file}.")