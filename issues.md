# Lab 5 — Static Analysis Issue Log

**Target file:** `ecommerce_cart_system.py`  
**Tools:** Pylint, Bandit, and Flake8

> Line numbers below refer to the original `ecommerce_cart_system.py` in the teacher-provided GitHub repository. They will change after replacing the file with the cleaned version.

| Issue | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Dynamic `eval()` execution | Security — High | `43` | Evaluating an expression string can execute arbitrary Python code if the value is influenced by untrusted input. | Replaced the expression parameter with a numeric `discount_rate`, validated it, and computed the discounted price directly. |
| Shell command built with input | Security — High | `59` | `os.system()` with a filename concatenated into a command can allow shell injection. | Removed the shell command and used `pathlib.Path.write_text()` to write the receipt directly. |
| Hard-coded payment secret | Security — High | `71, 80` | A secret-like payment gateway key was embedded in the source and printed, risking exposure through source control or logs. | Removed the hard-coded key and the statement that printed it. Real credentials should be supplied through a secure configuration mechanism and never printed. |
| Predictable PIN generator | Security — Medium | `52` | The `random` module is not intended for security-sensitive tokens such as checkout PINs. | Replaced it with `secrets.randbelow()` to generate a four-digit PIN securely. The demo does not display the PIN itself. |
| MD5 digest | Security / Reliability — Medium | `48` | MD5 is outdated for collision-resistant hashing. | Replaced MD5 with SHA-256 and documented that this digest is only an identifier/checksum, not authentication. |
| Mutable default argument | Bug / Maintainability — Medium | `14` | `audit_log=[]` is shared across calls, so entries can unexpectedly persist between calls. | Changed the default to `None` and only appends when the caller supplies a log list. |
| Bare `except` that silently ignores errors | Reliability — Medium | `27–28` | A bare exception catches unrelated problems and `pass` hides failures. | Used `dict.pop(item_id, None)` and returned a clear success/failure result; missing items are logged. |
| No input validation | Reliability — Medium | `14–20, 41–44` | Empty IDs/names, invalid prices, non-positive quantities, or invalid discounts could corrupt cart calculations. | Added validation and raised `ValueError` or `TypeError` for invalid inputs. |
| File opened without a context manager | Maintainability — Low | `56–58` | Manual `open()`/`close()` can leave a file open if an error occurs. | Used `Path.write_text()`, which manages the file operation cleanly. |
| Incorrect comparison to `None` and unused variable | Style / Maintainability — Low | `32–33` | `== None` is non-idiomatic, and `handling_fee` was assigned but never used. | Used an explicit `is not None` check and removed the unused variable. |
| Poor naming and formatting | Style — Low | `14, 20` and unused import at `4` | CamelCase function names, unused imports, and old-style `%` formatting reduce consistency and readability. | Used `snake_case`, removed unused imports, and adopted f-strings and standard formatting. |
| Cart total tracking was fragile | Correctness — Medium | `19, 24–28` | A separate global total was increased on add but not reduced on removal, so totals could become inaccurate. | Removed the stale global counter and calculate the current cart total from the cart contents when requested. |

## Verification checklist

- [ ] Run the original program before modifying it and record any surprising behaviour.
- [ ] Save the original Pylint, Bandit, and Flake8 output as `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt`.
- [ ] Apply the fixes in the cleaned file.
- [ ] Rerun all three tools and check that the issues addressed above no longer appear.
- [ ] The locations are for the original version; do not copy these old line numbers as references to the cleaned file.
