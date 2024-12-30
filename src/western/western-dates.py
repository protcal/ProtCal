import json
from datetime import date, timedelta

def get_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def calculate_offset(base_date, offset_days):
    return base_date + timedelta(days=offset_days)

def get_fixed_date(year, month, day):
    return date(year, month, day)

def get_advent_start(year):
    christmas = get_fixed_date(year, 12, 25)
    fourth_sunday = christmas - timedelta(days=(christmas.weekday() + 22) % 7)
    return fourth_sunday

def get_holy_week_start(easter):
    return calculate_offset(easter, -7)

def get_last_sunday_after_pentecost(advent_start):
    advent_start = get_advent_start(year)
    offset_days = rules['last_sunday_after_pentecost']['offset_days']
    return calculate_offset(advent_start, offset_days)

def get_thanksgiving(year, canada=False):
    if canada:
        first_day = date(year, 10, 1)
        first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
        return first_monday + timedelta(weeks=1)
    first_day = date(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    return first_thursday + timedelta(weeks=3)

def get_sunday_of(holiday):
    offset_days = (6 - holiday.weekday()) % 7
    return calculate_offset(holiday, offset_days)


with open('liturgical-rules.json', 'r') as f:
    rules = json.load(f)

#debug
year = 2024
easter = get_easter(year)
christmas = get_fixed_date(year, rules['christmas']['fixed_date']['month'], rules['christmas']['fixed_date']['day'])
pentecost = calculate_offset(easter, rules['pentecost']['offset_days'])
epiphany = get_fixed_date(year, rules['epiphany']['fixed_date']['month'], rules['epiphany']['fixed_date']['day'])
epiphany_sunday = get_sunday_of(epiphany)
lent_start = calculate_offset(easter, rules['lent_start']['offset_days'])
lent_end = calculate_offset(easter, rules['lent_end']['offset_days'])
holy_week_start = get_holy_week_start(easter)
advent_start = get_advent_start(year)
advent_end = get_fixed_date(year, rules['advent_end']['fixed_date']['month'], rules['advent_end']['fixed_date']['day'])
transfiguration = calculate_offset(easter, rules['transfiguration']['offset_days'])
trinity_sunday = calculate_offset(easter, rules['trinity_sunday']['offset_days'])
last_sunday_after_pentecost = get_last_sunday_after_pentecost(advent_start)
all_saints = get_fixed_date(year, 11, 1)
all_saints_sunday = get_sunday_of(all_saints)
thanksgiving = get_thanksgiving(year)
thanksgiving_ca = get_thanksgiving(year, True)

print(f"Easter: {easter}")
print(f"Christmas: {christmas}")
print(f"Epiphany: {epiphany}")
print(f"Pentecost: {pentecost}")
print(f"Lent Start: {lent_start}")
print(f"Lent End: {lent_end}")
print(f"Holy Week Start: {holy_week_start}")
print(f"Advent Start: {advent_start}")
print(f"Advent End: {advent_end}")
print(f"Transfiguration: {transfiguration}")
print(f"Trinity Sunday: {trinity_sunday}")
print(f"Last Sunday After Pentecost: {last_sunday_after_pentecost}")
print(f"All Saints: {all_saints}")
print(f"Thanksgiving: {thanksgiving}")
print(f"Thanksgiving, CA: {thanksgiving_ca}")
print(f"All Saints Sunday: {all_saints_sunday}")
print(f"Epiphany Sunday: {epiphany_sunday}")
