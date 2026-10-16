# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding-style violations. It improves code quality, security, readability, and maintainability.

## 2. What issues did you identify and fix?

I identified issues such as unsafe use of `eval()`, weak MD5 hashing, insecure random-token generation, shell-command execution, broad exception handling, mutable default arguments, unused variables, and formatting violations. I fixed these issues to improve the program's security and code quality.

## 3. How did Pylint, Bandit, and Flake8 help?

Pylint identified code-quality problems and initially gave the program a score of 5.19/10. Bandit identified five potential security issues, including the use of `eval()` and `os.system()`. Flake8 detected formatting and style violations. After making corrections, Pylint scored 10.00/10, Bandit reported no issues, and Flake8 reported no violations.

## 4. What did you learn from this lab?

I learned that static analysis tools can identify problems that may be overlooked during ordinary programming. Using these tools helped me improve the safety, readability, and maintainability of Python code. I also learned the importance of checking the reports again after making changes to verify that the issues have been resolved.