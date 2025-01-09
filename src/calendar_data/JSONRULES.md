# JSON Rules

# Naming of JSON files

    All files should be named after whatever they're for and put into a folder of whichever tradition those seasons belong to.
    The possibilities currently are lectionary.json, dates.json, saints.json, and seasons.json.
    Flags are used for denoting differences in the JSON files. For example, seasons.json and seasons_oneyear.json for the standard
    three year seasons or the seasons for the one year calendar.

# Seasons
    "name": Denotes the name of the season
    "description": Describes what the season is, what its for, and just general stuff
    "start": The holiday on which the season begins 
    "end": The holiday on which the season ends
    "offset": Optional. If the ending holiday of the season is considered a part of the season or not
    "cross-year": Optional. If the season starts in the previous year or not
    "liturgical_color": Optional, highly recommended. Colour of the season

## Dates

    Dates can either be one of three: Fixed date, offset date, and complex date.

### All dates:

        "name": Name of the holy day
        "alt_name": Optional. Alternative name for the holy day
        "description": Description of the holy day

### Fixed dates:

        "fixed_date": {
            "month": The month of the holy day
            "day": The day of the holy day
        }

### Offset dates:

        "offset_days": An integer that denotes how many days after the dependency holy day this holy day happens
        "depends_on": The key of the holy day this holy day depends on

### Complex dates:

        "complex": If set to true, this holy day must have a function for calculating the holy day provided in calendar_functions.py,
        and later in development will be in western_functions or eastern_functions respectively, according to whichever culture




