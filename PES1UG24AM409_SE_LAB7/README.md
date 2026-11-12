# Software Engineering Lab 7: Fuzzing for Input Validation Bugs

**Student Name:** SUMAN DIDDIMANI  
**SRN:** PES1UG24AM409  
**Course:** Software Engineering Laboratory (UE24CS242B) &mdash; Section G  
**Assigned System:** Irrigation Scheduler (`SETAPESU26/L6_L7_37_irrigation_scheduler`)

---

## 1. Overview

This laboratory experiment explores **dynamic fuzz testing** using the **Hypothesis** property-based testing framework in Python. Fuzz testing algorithmically injects pseudo-random, malformed, boundary, and unexpected inputs to identify software vulnerabilities, unhandled exceptions, and input validation defects.

The application under test (`processor.py` / `irrigation_scheduler.py`) provides core computational routines for an automated agricultural irrigation scheduler:
1. `parse_zone(text)`: Parses zone identifiers and land area in $m^2$ from `name:area` format.
2. `moisture_average(readings_csv)`: Computes the integer average of soil moisture readings from comma-separated values.
3. `water_needed(text)`: Calculates required irrigation water in liters based on plot size and rainfall from `plot|rainfall` format.

---

## 2. Directory Structure

```text
PES1UG24AM409_SE_LAB7/
├── processor.py                     # Hardened application code
├── test_processor.py                # Hypothesis property-based fuzz testing suite
├── irrigation_scheduler.py          # Mirror of application code
├── test_irrigation_scheduler.py     # Mirror of test suite
├── Lab7_FuzzTesting_PES1UG24AM409.pdf # Comprehensive lab report with screenshots
├── README.md                        # Documentation and instructions
├── .gitignore                       # Ignores cache and temporary files
└── screenshots/
    ├── 01_Original_Application.png  # Execution of original application
    ├── 02_Fuzz_Test_Failures.png    # Initial failing Hypothesis fuzz tests
    ├── 03_Fixed_Application.png     # Execution of fixed application
    └── 04_Final_Fuzz_Test_Results.png # Successful passing Hypothesis tests
```

---

## 3. Environment & Dependencies

- **Python:** 3.8+ (Tested on Python 3.11.9)
- **Pytest:** `>= 7.0` (Tested on Pytest 9.2.0)
- **Hypothesis:** `>= 6.0` (Tested on Hypothesis 6.170.15)

To install dependencies:
```bash
pip install hypothesis
pip install pytest
```

---

## 4. Execution Commands

### A. Run the Application
```bash
python processor.py
```
Sample interactive inputs:
- `Enter zone:area in m2 (e.g. north:120):` `north:120`
- `Enter moisture readings as CSV (e.g. 40,35,50):` `40,35,50`
- `Enter area|rainfall (e.g. 120|8):` `120|8`

### B. Execute Hypothesis Fuzz Tests
```bash
pytest test_processor.py
```
Or if pytest is not directly on PATH:
```bash
python -m pytest test_processor.py
```

---

## 5. Summary of Bugs Discovered & Fixes

| Function | Discovered Failing Inputs | Unhandled Bug / Crash | Defensive Resolution |
| :--- | :--- | :--- | :--- |
| `parse_zone` | `""`, `None`, `":"`, `"north:-50"` | `ValueError: not enough values to unpack`, `AttributeError: 'NoneType' has no split`, invalid float | Validates string type & non-empty; checks delimiter count; strips whitespace; defaults empty name to `'Unknown'`; clamps area to non-negative non-NaN float. |
| `moisture_average` | `""`, `None`, `"40,,50"`, `"abc"` | `ValueError: invalid literal for int()`, `AttributeError`, `ZeroDivisionError` | Validates string type; iterates over tokens skipping empty/whitespace values; filters non-numeric tokens; clamps moisture to non-negative; returns `0` if empty. |
| `water_needed` | `""`, `None`, `"120|"`, `"nan|8"` | `ValueError: not enough values to unpack`, `AttributeError`, float conversion / NaN comparison | Validates string type; verifies single pipe delimiter; parses floats with NaN/inf checks; ensures result $\ge 0.0$. |

---

## 6. Deliverables Verification

- [x] `processor.py` executes cleanly without unexpected crashes.
- [x] `test_processor.py` executes 9 test suites passing 100% of Hypothesis test cases.
- [x] Genuine terminal screenshots preserved in `screenshots/`.
- [x] Professional report `Lab7_FuzzTesting_PES1UG24AM409.pdf` created.
