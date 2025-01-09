from calendar_functions import *
from csvgenerator import *

if __name__ == "__main__":
    year = int(input("Enter the year for which you want to display the church calendar: "))    
    tradition = input("Put in the tradition you wish to use (default = lutheran): ").strip().lower()
    if not tradition:
        tradition = "lutheran"    
    flags = input("Insert any calendar flags here (ex: oneyear calendar): ").strip().lower()
    if not flags:
        flags = None
    csv = input("Would you like to output a CSV file? (yes/no): ").strip().lower() == "no"
    print()
    display_holidays(year, tradition, flags)
    print()
    display_seasons(year, tradition, flags)
    print()
    display_saints(year, tradition, flags)
    
    if csv:
        calendar = generate_calendar(year, tradition, flags)
        output_file = f"liturgical_calendar_{year}.csv"
        write_calendar_to_csv(calendar, output_file)
        print(f"\nLiturgical calendar for {year} has been written to {output_file}.")