import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# =====================================================================
# Branch Coverage Tests for should_irrigate()
# =====================================================================

def test_branch_moisture_above_60():
    """Branch: moisture >= 60 evaluates to True (moisture = 61)."""
    assert should_irrigate(61, 0, "seedling") is False


def test_branch_moisture_exact_60_boundary():
    """Branch: moisture >= 60 evaluates to True at boundary (moisture = 60)."""
    assert should_irrigate(60, 0, "seedling") is False


def test_branch_moisture_below_60_boundary():
    """Branch: moisture >= 60 evaluates to False at boundary (moisture = 59)."""
    # Follows through to subsequent checks; with seedling and moisture 40 -> True
    assert should_irrigate(40, 0, "seedling") is True


def test_branch_rain_above_10():
    """Branch: rain_mm >= 10 evaluates to True (rain = 15)."""
    assert should_irrigate(30, 15, "seedling") is False


def test_branch_rain_exact_10_boundary():
    """Branch: rain_mm >= 10 evaluates to True at boundary (rain = 10)."""
    assert should_irrigate(30, 10, "flowering") is False


def test_branch_rain_below_10_boundary():
    """Branch: rain_mm >= 10 evaluates to False at boundary (rain = 9.9)."""
    # Follows through to flowering branch (< 55) -> True
    assert should_irrigate(50, 9.9, "flowering") is True


def test_branch_seedling_moisture_below_45():
    """Branch: stage == 'seedling' True, moisture < 45 True (moisture = 44)."""
    assert should_irrigate(44, 2, "seedling") is True


def test_branch_seedling_moisture_exact_45_boundary():
    """Branch: stage == 'seedling' True, moisture < 45 False at boundary (moisture = 45)."""
    assert should_irrigate(45, 2, "seedling") is False


def test_branch_seedling_moisture_above_45():
    """Branch: stage == 'seedling' True, moisture < 45 False (moisture = 46)."""
    assert should_irrigate(46, 2, "seedling") is False


def test_branch_flowering_moisture_below_55():
    """Branch: stage == 'flowering' True, moisture < 55 True (moisture = 54)."""
    assert should_irrigate(54, 3, "flowering") is True


def test_branch_flowering_moisture_exact_55_boundary():
    """Branch: stage == 'flowering' True, moisture < 55 False at boundary (moisture = 55)."""
    assert should_irrigate(55, 3, "flowering") is False


def test_branch_flowering_moisture_above_55():
    """Branch: stage == 'flowering' True, moisture < 55 False (moisture = 56)."""
    assert should_irrigate(56, 3, "flowering") is False


def test_branch_other_stage_rain_exact_5_boundary():
    """Branch: other stage, rain_mm >= 5 evaluates to True at boundary (rain = 5)."""
    assert should_irrigate(30, 5, "vegetative") is False


def test_branch_other_stage_rain_above_5():
    """Branch: other stage, rain_mm >= 5 evaluates to True (rain = 6)."""
    assert should_irrigate(20, 6, "fruiting") is False


def test_branch_other_stage_rain_below_5_boundary():
    """Branch: other stage, rain_mm >= 5 evaluates to False at boundary (rain = 4.9)."""
    # Follows through to moisture < 40 check -> True
    assert should_irrigate(35, 4.9, "vegetative") is True


def test_branch_other_stage_moisture_below_40():
    """Branch: other stage, moisture < 40 evaluates to True (moisture = 39)."""
    assert should_irrigate(39, 2, "vegetative") is True


def test_branch_other_stage_moisture_exact_40_boundary():
    """Branch: other stage, moisture < 40 evaluates to False at boundary (moisture = 40)."""
    assert should_irrigate(40, 2, "vegetative") is False


def test_branch_other_stage_moisture_above_40():
    """Branch: other stage, moisture < 40 evaluates to False (moisture = 41)."""
    assert should_irrigate(41, 2, "vegetative") is False


# =====================================================================
# Branch Coverage Tests for water_volume()
# =====================================================================

def test_branch_water_volume_negative_area():
    """Branch: area_m2 <= 0 evaluates to True for negative area."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-5, "seedling", 20)


def test_branch_water_volume_zero_area_boundary():
    """Branch: area_m2 <= 0 evaluates to True at zero boundary."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)


def test_branch_water_volume_positive_area_boundary():
    """Branch: area_m2 <= 0 evaluates to False for positive area."""
    assert water_volume(1, "seedling", 20) == 2


def test_branch_water_volume_stage_seedling():
    """Branch: stage == 'seedling' sets litres = 2."""
    assert water_volume(10, "seedling", 20) == 20


def test_branch_water_volume_stage_flowering():
    """Branch: stage == 'flowering' sets litres = 5."""
    assert water_volume(10, "flowering", 20) == 50


def test_branch_water_volume_stage_other_else():
    """Branch: other stage else sets litres = 4."""
    assert water_volume(10, "mature", 20) == 40


def test_branch_water_volume_temp_above_35():
    """Branch: temp_c > 35 evaluates to True (temp = 36, multiplier 1.5)."""
    # stage other: 4 * 1.5 = 6.0; 10 * 6.0 = 60.0
    assert water_volume(10, "mature", 36) == 60.0


def test_branch_water_volume_temp_exact_35_boundary():
    """Branch: temp_c > 35 False and temp_c < 10 False at boundary (temp = 35)."""
    assert water_volume(10, "mature", 35) == 40


def test_branch_water_volume_temp_between_10_and_35():
    """Branch: temp_c in [10, 35] normal range without multiplier."""
    assert water_volume(10, "mature", 25) == 40


def test_branch_water_volume_temp_exact_10_boundary():
    """Branch: temp_c < 10 evaluates to False at boundary (temp = 10)."""
    assert water_volume(10, "mature", 10) == 40


def test_branch_water_volume_temp_below_10():
    """Branch: temp_c < 10 evaluates to True (temp = 9, multiplier 0.5)."""
    # stage other: 4 * 0.5 = 2.0; 10 * 2.0 = 20.0
    assert water_volume(10, "mature", 9) == 20.0


# =====================================================================
# Branch Coverage Tests for schedule()
# =====================================================================

def test_branch_schedule_empty_zones():
    """Branch: for-loop over empty zones list evaluates to False immediately."""
    assert schedule([], 100) == []


def test_branch_schedule_skip_zone_not_needing_water():
    """Branch: if not should_irrigate evaluates to True (continue branch executed)."""
    zones = [
        ("WetZone", 10, 80, 0, "seedling", 20),   # should_irrigate is False -> continue
        ("DryZone", 10, 30, 0, "seedling", 20),   # should_irrigate is True -> planned
    ]
    assert schedule(zones, 50) == ["DryZone"]


def test_branch_schedule_need_exceeds_budget_break():
    """Branch: if need > budget evaluates to True (break branch executed)."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),   # need = 20 <= 25 -> budget left: 5
        ("ZoneB", 10, 30, 0, "seedling", 20),   # need = 20 > 5 -> break
        ("ZoneC", 1, 30, 0, "seedling", 20),    # skipped due to break
    ]
    assert schedule(zones, 25) == ["ZoneA"]


def test_branch_schedule_need_exact_match_budget():
    """Branch: if need == budget (boundary: need > budget is False)."""
    zones = [
        ("ZoneExact", 10, 30, 0, "seedling", 20),  # need = 20, budget = 20
    ]
    assert schedule(zones, 20) == ["ZoneExact"]


def test_branch_schedule_all_zones_planned():
    """Branch: loop completes normally when all eligible zones fit budget."""
    zones = [
        ("Field1", 10, 30, 0, "seedling", 20),     # need = 20
        ("Field2", 5, 40, 2, "flowering", 20),    # need = 25
        ("Field3", 10, 20, 1, "vegetative", 20),  # need = 40
    ]
    assert schedule(zones, 100) == ["Field1", "Field2", "Field3"]
