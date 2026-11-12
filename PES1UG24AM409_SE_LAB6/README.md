# Software Engineering Lab 6: Code and Branch Coverage Analysis

- **Student Name:** Suman Diddimani
- **SRN:** PES1UG24AM409
- **Assigned Application:** `irrigation_scheduler.py`
- **Assigned Repository:** `https://github.com/SETAPESU26/L6_L7_37_irrigation_scheduler`

---

## Deliverables Summary

This directory contains complete test suites for measuring and maximizing statement (line) coverage and decision (branch) coverage for `irrigation_scheduler.py`.

```
PES1UG24AM409_SE_LAB6/
├── irrigation_scheduler.py
├── CodeCoverageTest_AM409_irrigation_scheduler.py
├── BranchCoverageTest_AM409_irrigation_scheduler.py
├── README.md
├── pytest.ini
├── .gitignore
└── screenshots/
    ├── Code_Coverage_Report.png
    └── Branch_Coverage_Report.png
```

---

## Requirements & Setup

Install the required testing libraries:

```bash
pip install coverage pytest
```

---

## 1. Code Coverage (Statement Coverage)

The code coverage test suite (`CodeCoverageTest_AM409_irrigation_scheduler.py`) contains 15 unit tests covering every executable line and functionality across `should_irrigate`, `water_volume`, and `schedule`.

### Running Code Coverage

```bash
coverage run -m pytest CodeCoverageTest_AM409_irrigation_scheduler.py
coverage report -m
```

### Results Achieved
- **Statements Covered:** 38 / 38 (100%)
- **Test Suite Statements:** 43 / 43 (100%)
- **Total Line Coverage:** **100%** (exceeds the 90% threshold requirement)
- **Tests Passed:** 15 / 15

Screenshot reference: `screenshots/Code_Coverage_Report.png`

---

## 2. Branch Coverage (Decision Coverage)

The branch coverage test suite (`BranchCoverageTest_AM409_irrigation_scheduler.py`) contains 34 targeted tests specifically analyzing each condition, true/false evaluation, and boundary conditions:
- **`should_irrigate`**: moisture boundaries (59, 60, 61), rain boundaries (4.9, 5, 9.9, 10, 12, 15), seedling moisture boundaries (44, 45, 46), flowering moisture boundaries (54, 55, 56), and other stage moisture boundaries (39, 40, 41).
- **`water_volume`**: non-positive area handling (`<= 0`), stage branches (`seedling`, `flowering`, other), and temperature threshold multipliers (`> 35`, `35`, `10..35`, `10`, `< 10`).
- **`schedule`**: empty zones loop branch, zone skipped branch (`not should_irrigate`), budget break branch (`need > budget`), exact budget match (`need == budget`), and complete schedule plan.

### Running Branch Coverage

```bash
coverage run --branch -m pytest BranchCoverageTest_AM409_irrigation_scheduler.py
coverage report -m
```

### Results Achieved
- **Statements Covered:** 38 / 38 (100%)
- **Branches Covered:** 28 / 28 (100%)
- **Total Branch Coverage:** **100%** (exceeds the 90% threshold requirement)
- **Tests Passed:** 34 / 34

Screenshot reference: `screenshots/Branch_Coverage_Report.png`
