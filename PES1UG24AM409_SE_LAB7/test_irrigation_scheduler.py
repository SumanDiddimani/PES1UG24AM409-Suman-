"""
Hypothesis fuzz testing suite for irrigation_scheduler.py
Imports from test_processor.py to maintain complete test coverage under both filenames.
"""

from test_processor import (
    test_parse_zone_no_crash,
    test_moisture_average_no_crash,
    test_water_needed_no_crash,
    test_parse_zone_valid_properties,
    test_moisture_average_valid_properties,
    test_water_needed_valid_properties,
    test_parse_zone_edge_cases,
    test_moisture_average_edge_cases,
    test_water_needed_edge_cases,
)
