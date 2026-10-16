# Static Code Analysis — Issues Identified and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Use of `eval()` | Security — Medium | 40 | The `eval()` function evaluates a string as a Python expression, which may execute unsafe code. | Replaced `eval()` with a restricted billing calculation that supports the formula used by the program. |
| Use of MD5 hashing | Security — High | 45 | MD5 is unsuitable for security-sensitive hashing because of known weaknesses. | Replaced MD5 with SHA-256 using `hashlib.sha256()`. |
| Shell command execution | Security — High | 56 | `os.system()` executes a shell command and can introduce command-injection risks. | Removed shell execution and used a normal Python print statement. |
| Insecure random token generation | Security — Low | 49 | `random.randint()` is not designed for security-sensitive token generation. | Replaced it with `secrets.randbelow()` to generate the four-digit token. |
| Silent exception handling | Bug / Security — Low | 24–25 | A bare `except` followed by `pass` silently ignores errors, making problems difficult to detect. | Removed the broad exception handler and checked whether the patient record exists before updating it. |
| Mutable default argument | Code Quality | 13 | The default list `intake_log=[]` can be shared between function calls. | Changed the default to `None` and initialized a new list when needed. |
| Incorrect comparison with `None` | Code Quality | 30 | Comparing a value to `None` using `==` is discouraged by Python style guidelines. | Replaced the comparison with `is not None`. |
| Unused imports and variables | Code Quality | 4, 29, 39 | The unused `math` import and variables make the code less clear and maintainable. | Removed unused imports and variables. |
| Missing documentation and naming conventions | Code Quality | 1, 13, 21, 28, 38, 44, 48, 52, 59, 67 | Missing docstrings and the name `admitPatient` reduce readability and violate Python conventions. | Added docstrings and renamed the function to `admit_patient`. |
| Formatting violations | Style | 7–16, 80 | Long lines and a missing final newline violate Flake8 style checks. | Reformatted the code and ensured the file ends with a newline. |
| Unspecified file encoding and resource handling | Code Quality | 53–54 | Opening a file without an explicit encoding and closing it manually can reduce portability and reliability. | Used a context manager and UTF-8 encoding. |
| Hard-coded access key | Security | 70–71 | The original program printed a hard-coded nurse access key, potentially exposing sensitive information. | Removed the hard-coded key and its print statement from the demonstration. |

## Verification Results

- **Pylint:** Improved from 5.19/10 to 10.00/10.
- **Bandit:** Improved from five reported findings to zero reported issues.
- **Flake8:** Improved from eleven reported violations to zero reported violations.

The corrected program executed successfully and retained the demonstrated patient admission, discharge, billing, ledger export, and ward-summary operations.