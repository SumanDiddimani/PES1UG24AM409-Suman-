from hypothesis import given, strategies as st
import pytest
from processor import parse_zone, moisture_average, water_needed


# ==========================================
# 1. No-Crash / Robustness Fuzz Tests
# ==========================================

@given(st.text() | st.none())
def test_parse_zone_no_crash(s):
    """Fuzz test: parse_zone should never crash on arbitrary text or None."""
    try:
        res = parse_zone(s)
        assert isinstance(res, tuple)
        assert len(res) == 2
        assert isinstance(res[0], str)
        assert isinstance(res[1], (int, float))
        assert res[1] >= 0
    except Exception as e:
        pytest.fail(f"parse_zone crashed with: {type(e).__name__}: {e}")


@given(st.text() | st.none())
def test_moisture_average_no_crash(s):
    """Fuzz test: moisture_average should never crash on arbitrary text or None."""
    try:
        res = moisture_average(s)
        assert isinstance(res, int)
        assert res >= 0
    except Exception as e:
        pytest.fail(f"moisture_average crashed with: {type(e).__name__}: {e}")


@given(st.text() | st.none())
def test_water_needed_no_crash(s):
    """Fuzz test: water_needed should never crash on arbitrary text or None."""
    try:
        res = water_needed(s)
        assert isinstance(res, (int, float))
        assert res >= 0
    except Exception as e:
        pytest.fail(f"water_needed crashed with: {type(e).__name__}: {e}")


# ==========================================
# 2. Property-Based Tests for Valid Inputs
# ==========================================

@given(
    name=st.text(alphabet=st.characters(categories=('Lu', 'Ll')), min_size=1, max_size=30),
    area=st.floats(min_value=0.1, max_value=10000.0, allow_nan=False, allow_infinity=False)
)
def test_parse_zone_valid_properties(name, area):
    """Property: Valid zone input 'name:area' preserves title-cased name and float area."""
    formatted_input = f"{name}:{area}"
    zone_name, zone_area = parse_zone(formatted_input)
    assert zone_name == name.strip().title()
    assert zone_area == pytest.approx(float(area), rel=1e-4)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=50))
def test_moisture_average_valid_properties(readings):
    """Property: Valid integer CSV readings produce average bounded by min and max."""
    csv_str = ",".join(str(r) for r in readings)
    avg = moisture_average(csv_str)
    expected_avg = sum(readings) // len(readings)
    assert avg == expected_avg
    assert min(readings) <= avg <= max(readings)


@given(
    plot=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False),
    rain=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False)
)
def test_water_needed_valid_properties(plot, rain):
    """Property: water_needed is always non-negative and follows max(plot*5 - rain, 0)."""
    text_input = f"{plot}|{rain}"
    result = water_needed(text_input)
    assert result >= 0.0
    expected = max(plot * 5.0 - rain, 0.0)
    assert result == pytest.approx(expected, rel=1e-4)


# ==========================================
# 3. Targeted Edge Case & Input Validation Tests
# ==========================================

@given(st.sampled_from([
    "", "   ", "north", "north:120:extra", "north:-50", ":120", "north:",
    "north:abc", None, "north:nan", "north:inf"
]))
def test_parse_zone_edge_cases(s):
    """Ensure malformed zone strings or invalid areas do not crash."""
    res = parse_zone(s)
    assert isinstance(res, tuple)
    assert len(res) == 2
    assert isinstance(res[0], str)
    assert isinstance(res[1], (int, float))
    assert res[1] >= 0


@given(st.sampled_from([
    "", "   ", "40,,50", "40,abc,50", ",,", ",40,", "-10,50", None,
    "100", "0,0,0"
]))
def test_moisture_average_edge_cases(s):
    """Ensure empty CSV, missing tokens, or non-numeric tokens do not crash."""
    res = moisture_average(s)
    assert isinstance(res, int)
    assert res >= 0


@given(st.sampled_from([
    "", "   ", "120", "120|8|2", "120|", "|8", "abc|8", "120|xyz",
    "-50|8", "120|-10", None, "nan|8", "120|inf"
]))
def test_water_needed_edge_cases(s):
    """Ensure malformed pipes, non-numeric values, or negative values do not crash."""
    res = water_needed(s)
    assert isinstance(res, (int, float))
    assert res >= 0.0
