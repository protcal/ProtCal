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

def get_christmas(year): #This is done for consistency
    return date(year, 12, 25)

def get_pentacost(year):
    return calculate_offset(easter, rules['calculation_rules']['pentecost']['offset_days'])

def get_lent_start(year):
    return calculate_offset(easter, rules['calculation_rules']['lent_start']['offset_days'])

def get_lent_end(year):
    return calculate_offset(easter, rules['calculation_rules']['lent_end']['offset_days'])

def get_transfiguration(year):
    return calculate_offset(easter, rules['calculation_rules']['transfiguration']['offset_days'])

def calculate_offset(base_date, offset_days):
    return base_date + timedelta(days=offset_days)

def get_fixed_date(year, month, day):
    return date(year, month, day)

with open('liturgical-rules.json', 'r') as f:
    rules = json.load(f)

#debug
year = 2025
easter = get_easter(year)
christmas = date(year, 12, 25)
pentecost = get_pentacost(year)
lent_start = get_lent_start(year)
lent_end = get_lent_end(year)
#advent_start = calculate_offset(
#advent_end = calculate_offset(

transfiguration = get_transfiguration(year)
christmas = get_christmas(year)

print(f"Easter: {easter}")
print(f"Pentecost: {pentecost}")
print(f"Lent Start: {lent_start}")
print(f"Lent End: {lent_end}")
#print(f"Advent Start: {advent_start}")
#print(f"Advent End: {advent_end}")
print(f"Transfiguration: {transfiguration}")
print(f"Christmas: {christmas}")