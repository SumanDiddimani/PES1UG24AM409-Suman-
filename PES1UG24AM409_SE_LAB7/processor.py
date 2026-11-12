"""
Lab 7: Fuzzing for Input Validation Bugs
Module: processor.py (Irrigation Scheduler Application)
Student SRN: PES1UG24AM409
Student Name: SUMAN DIDDIMANI

This module provides robust input parsing and calculation functions
for the Irrigation Scheduler application, hardened against malformed,
unexpected, boundary, and fuzz inputs uncovered during Hypothesis fuzz testing.
"""

import math


def parse_zone(text):
    """
    Parses a zone string in the format 'name:area' (e.g., 'north:120').
    
    Robustness and Validation Rules:
    - Rejects or safely handles None, non-string, and empty inputs.
    - Requires exactly one colon separating zone name and area.
    - Trims whitespace from both name and area.
    - Converts zone name to title case (e.g., 'north' -> 'North'); defaults to 'Unknown' if name is empty.
    - Converts area to float; validates that area is non-negative and non-NaN/inf.
    - Returns a tuple (zone_name, zone_area) as (str, float).
    """
    if text is None or not isinstance(text, str):
        return ("Unknown", 0.0)

    parts = text.split(':')
    if len(parts) != 2:
        return ("Unknown", 0.0)

    raw_name, raw_area = parts[0].strip(), parts[1].strip()
    zone_name = raw_name.title() if raw_name else "Unknown"

    try:
        area = float(raw_area)
        if math.isnan(area) or math.isinf(area) or area < 0.0:
            area = 0.0
    except (ValueError, TypeError):
        area = 0.0

    return (zone_name, area)


def moisture_average(readings_csv):
    """
    Computes the integer average of moisture readings provided as a CSV string (e.g., '40,35,50').
    
    Robustness and Validation Rules:
    - Rejects or safely handles None, non-string, and empty inputs.
    - Handles extra whitespace, consecutive commas, and trailing/leading commas.
    - Filters out non-numeric tokens.
    - Clamps moisture values to non-negative percentages (>= 0).
    - Avoids ZeroDivisionError when no valid readings are found by returning 0.
    - Returns integer average using floor division (sum(values) // len(values)).
    """
    if readings_csv is None or not isinstance(readings_csv, str):
        return 0

    values = []
    for token in readings_csv.split(','):
        cleaned = token.strip()
        if not cleaned:
            continue
        try:
            val = int(cleaned)
            # Moisture percentage is clamped to non-negative values
            values.append(max(0, val))
        except (ValueError, TypeError):
            continue

    if not values:
        return 0

    return sum(values) // len(values)


def water_needed(text):
    """
    Calculates estimated irrigation water needed given 'plot|rainfall' in m2 and mm (e.g., '120|8').
    Formula: need = plot * 5 - rainfall; result = max(need, 0.0).
    
    Robustness and Validation Rules:
    - Rejects or safely handles None, non-string, and empty inputs.
    - Requires exactly one pipe delimiter '|'.
    - Parses plot area and rainfall as floats; rejects NaN, inf, and negative values safely.
    - Returns float >= 0.0.
    """
    if text is None or not isinstance(text, str):
        return 0.0

    parts = text.split('|')
    if len(parts) != 2:
        return 0.0

    plot_str, rain_str = parts[0].strip(), parts[1].strip()

    try:
        plot = float(plot_str)
        if math.isnan(plot) or math.isinf(plot) or plot < 0.0:
            plot = 0.0
    except (ValueError, TypeError):
        plot = 0.0

    try:
        rain = float(rain_str)
        if math.isnan(rain) or math.isinf(rain) or rain < 0.0:
            rain = 0.0
    except (ValueError, TypeError):
        rain = 0.0

    need = plot * 5.0 - rain
    return max(need, 0.0)


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result)

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result)

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result)


if __name__ == "__main__":
    main()
