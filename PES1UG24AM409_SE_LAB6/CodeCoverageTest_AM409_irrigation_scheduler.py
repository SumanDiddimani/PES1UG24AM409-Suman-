import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# --- Code Coverage Tests for should_irrigate ---

def test_wet_soil_no_irrigation():
    """Line coverage: moisture >= 60 returns False."""
    assert should_irrigate(70, 0, "seedling") is False
    assert should_irrigate(60, 5, "flowering") is False


def test_heavy_rain_no_irrigation():
    """Line coverage: rain_mm >= 10 returns False."""
    assert should_irrigate(50, 12, "seedling") is False
    assert should_irrigate(30, 10, "vegetative") is False


def test_seedling_stage_dry_soil():
    """Line coverage: stage == 'seedling' and moisture < 45 returns True."""
    assert should_irrigate(40, 2, "seedling") is True


def test_seedling_stage_adequate_soil():
    """Line coverage: stage == 'seedling' and moisture >= 45 returns False."""
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_stage_needs_irrigation():
    """Line coverage: stage == 'flowering' returns moisture < 55."""
    assert should_irrigate(50, 2, "flowering") is True
    assert should_irrigate(56, 1, "flowering") is False


def test_other_stage_moderate_rain():
    """Line coverage: other stage with rain_mm >= 5 returns False."""
    assert should_irrigate(30, 6, "vegetative") is False


def test_other_stage_dry_soil():
    """Line coverage: other stage returns moisture < 40."""
    assert should_irrigate(35, 2, "vegetative") is True
    assert should_irrigate(42, 2, "vegetative") is False


# --- Code Coverage Tests for water_volume ---

def test_water_volume_invalid_area():
    """Line coverage: area_m2 <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 25)
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-5, "flowering", 20)


def test_water_volume_seedling():
    """Line coverage: seedling stage default temp (litres = 2)."""
    assert water_volume(10, "seedling", 20) == 20


def test_water_volume_flowering():
    """Line coverage: flowering stage default temp (litres = 5)."""
    assert water_volume(10, "flowering", 25) == 50


def test_water_volume_other_stage():
    """Line coverage: other stage default temp (litres = 4)."""
    assert water_volume(10, "vegetative", 25) == 40


def test_water_volume_high_temp():
    """Line coverage: temp_c > 35 applies 1.5x multiplier."""
    assert water_volume(10, "seedling", 38) == 30.0


def test_water_volume_low_temp():
    """Line coverage: temp_c < 10 applies 0.5x multiplier."""
    assert water_volume(10, "flowering", 8) == 25.0


# --- Code Coverage Tests for schedule ---

def test_schedule_all_zones_irrigated():
    """Line coverage: schedule plans irrigation for zones that need water within budget."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),
        ("ZoneB", 5, 40, 2, "flowering", 25),
    ]
    plan = schedule(zones, 100)
    assert plan == ["ZoneA", "ZoneB"]


def test_schedule_skips_unneeded_and_breaks_on_budget():
    """Line coverage: schedule skips zones not needing water, breaks when budget exceeded."""
    zones = [
        ("Zone1", 10, 70, 0, "seedling", 20),
        ("Zone2", 10, 30, 0, "seedling", 20),
        ("Zone3", 10, 30, 0, "flowering", 20),
        ("Zone4", 2, 20, 0, "seedling", 20),
    ]
    plan = schedule(zones, 30)
    assert plan == ["Zone2"]
