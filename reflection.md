# Lab 5 — Reflection

## 1. What is static code analysis, and how is it different from testing by running a program?

Static code analysis examines source code without executing it. Pylint checks code quality and common programming mistakes, Flake8 checks style and formatting rules, and Bandit looks for common security weaknesses. Running tests is still important because tests reveal behaviour for selected inputs, while static analysis can flag risky patterns even when a test has not triggered them. Neither approach replaces the other.

## 2. What kinds of problems did the tools help identify?

The analysis focused on a dangerous `eval()` call, shell-command construction, a hard-coded secret-like value, a predictable random-number generator, MD5 hashing, a mutable default argument, broad exception handling, and style problems. Some correctness and security concerns also required reading the code rather than relying only on tool output. For example, removing an item did not update the separate global total, and the program printed the hard-coded payment key.

## 3. Which fixes were most important, and why?

The most important fixes were removing `eval()`, removing the shell command built from a filename, and deleting the hard-coded payment secret. These reduce the risk of code execution, shell injection, and credential exposure. Using `secrets` for a PIN and SHA-256 for the item digest improves the security posture. Input validation and clearer error handling also make the cart more reliable for unexpected values.

## 4. How would static analysis fit into a future development workflow?

I would run Pylint, Bandit, and Flake8 after making changes and before committing code. I would review high-severity security findings first, fix correctness and reliability problems next, and then address style warnings. I would also keep tests for key cart operations, such as adding and removing products, validating quantities, calculating discounts, and exporting receipts. Running the checks automatically in a CI workflow would help prevent similar problems from returning.
