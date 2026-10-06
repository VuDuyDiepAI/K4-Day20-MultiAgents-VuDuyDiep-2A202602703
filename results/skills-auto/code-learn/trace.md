### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by reading the skill files that apply to this task.

### Tool call: read_file
{"file_path": "/skills/fix-failing-tests-incrementally/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/locate-project-files-before-editing/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/produce-required-output-artifacts/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-18 of 18 @@
---
name: fix-failing-tests-incrementally
description: Use when a test suite has failing tests and you need to diagnose and repair the underlying code.
---
1. Run the full suite once and capture the complete failure output to a file; do not re-run with narrow line slices.
2. Read each failure's traceback top-to-bottom: identify the exact function, the input value, and the expected vs actual behaviour.
3. Read the docstring and any type hints of the failing function before editing; the docstring is the contract.
4. Fix one failure at a time, then re-run only the affected test to confirm, then the full suite.
5. When a helper is shared, check every caller of the changed function still behaves correctly.
6. Handle all documented input formats, not just the one in the failing example (e.g. separators, parentheses for negatives, mixed case).
7. For numeric rounding, follow the stated rounding mode explicitly rather than relying on language defaults.
8. For ordering requirements, apply the documented sort key and tie-breakers exactly.
9. For serialization/quoting requirements, follow the documented format rather than a library default.
Completion checks:
- Full suite passes with zero failures.
- Every public function has type annotations on all parameters and the return value.
- A regression test file exists with at least one test per fixed bug and it passes.
- A changelog entry exists under the unreleased heading with one bullet per fix.

### Tool result
@@ lines 1-15 of 15 @@
---
name: locate-project-files-before-editing
description: Use when you need to find source, config, or test files in an unfamiliar project layout.
---
1. Do not assume a conventional directory layout; verify it first.
2. List the working directory and its immediate subdirectories before searching deeper.
3. If an installed package points to an editable source location, resolve that path and inspect it.
4. Check whether the package is importable from the current interpreter; if not, adjust the path or interpreter rather than guessing.
5. Search for the relevant files by name pattern and content, not by assumed path.
6. Once located, read the file before editing and confirm it is the one under test.
7. Avoid repeating identical discovery commands; if a command returns nothing new, change approach.
Completion checks:
- The actual source and test file paths are known and confirmed to exist.
- The interpreter used can import the project under test.
- No edits were made to files whose role was unverified.

### Tool result
@@ lines 1-17 of 17 @@
---
name: produce-required-output-artifacts
description: Use when a task requires writing result files to specific paths in a workspace.
---
1. Before analysis, list the exact output paths and formats the task requires.
2. Confirm the workspace directory exists and is writable; create it if missing.
3. Perform the analysis, then write each required artifact to its exact path.
4. Match the required schema exactly: header order, field names, and value types.
5. Normalize values to the required representation (e.g. canonical spellings, integer minor units, UTC timestamps in the specified format).
6. Deduplicate and filter rows according to the stated inclusion rules.
7. Include any required metadata block alongside the primary output.
8. After writing, re-open each artifact and verify it parses and matches the schema.
Completion checks:
- Every required output file exists at its specified path.
- Each file parses and its header/fields match the required schema.
- Value formats (units, casing, timezone, precision) match the specification.
- Row counts and deduplication match the stated rules.

### Assistant
Now let me explore the workspace.

### Tool call: ls
{"path": "/workspace"}

### Tool call: ls
{"path": "/"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool result
['/skills/', '/workspace/']

### Tool call: ls
{"path": "/workspace/inventory"}

### Tool call: ls
{"path": "/workspace/tests"}

### Tool call: read_file
{"file_path": "/workspace/README.md"}

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool call: read_file
{"file_path": "/workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "/workspace/tests/test_report.py"}

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Assistant
Now let me run the test suite to capture the failures.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -60"}

### Tool result
.FF...                                                                   [100%]
=================================== FAILURES ===================================
_____________________ test_total_value_thousands_separator _____________________

>   ???

/lab/tasks/code-learn/workspace/tests/test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
inventory/report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory/pricing.py:15: InvalidOperation
________________________ test_discount_rounding_half_up ________________________

>   ???
E   AssertionError: assert Decimal('9.04') == Decimal('9.05')
E    +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E    +    where Decimal('10.05') = Decimal('10.05')
E    +  and   Decimal('9.05') = Decimal('9.05')

/lab/t

### Assistant
Two failures. Let me analyze each against the docstrings.

**Failure 1 — `parse_price`**: doesn't handle thousands separators `,` or accounting parentheses `(12.00)`.

**Failure 2 — `apply_discount`**: `Decimal.quantize` defaults to `ROUND_HALF_EVEN`, but the docstring requires `ROUND_HALF_UP`. `10.05 * 90 / 100 = 9.045` → half-even gives `9.04`, half-up gives `9.05`.

Also, `low_stock` docstring says "strictly below `threshold`" but the code uses `<=`, and "sorted alphabetically, ignoring case" but the code doesn't sort. And `to_csv_row` docstring requires RFC 4180 quoting, which isn't implemented. Let me fix all of these.

### Tool call: edit_file
{"file_path": "/workspace/inventory/pricing.py", "old_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)\n\n\ndef apply_discount(price, percent):\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"))", "new_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\n_CENTS = Decimal(\"0.01\")\n\n\ndef parse_price(text: str) -> Decimal:\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    negative = cleaned.startswith(\"(\"

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Assistant
Now `report.py` — fix `low_stock` (strictly below, case-insensitive sort) and add annotations:

### Tool call: edit_file
{"file_path": "/workspace/inventory/report.py", "new_string": "\"\"\"Inventory reports.\"\"\"\nfrom decimal import Decimal\nfrom typing import Any, Iterable\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items: Iterable[dict[str, Any]]) -> Decimal:\n    \"\"\"Total value of `items` after per-item discounts.\n\n    Each item is a dict: {\"name\": str, \"price\": str, \"qty\": int, \"discount\": percent (optional)}.\n    \"\"\"\n    total = Decimal(\"0\")\n    for item in items:\n        price = parse_price(item[\"price\"])\n        price = apply_discount(price, item.get(\"discount\", 0))\n        total += price * item[\"qty\"]\n    return total\n\n\ndef low_stock(items: Iterable[dict[str, Any]], threshold: int = 5) -> list[str]:\n    \"\"\"Names of the items whose quantity is strictly below `threshold`.\n\n    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.lower)", "old_string": "\"\"\"Inventory reports.\"\"\"\nfrom decimal import Decimal\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items):\n    \"\"\"Total value of `items` after per-item discounts.\n\n    Each item is a dict: {\"name\": str, \"price\": str, \"qty\": int, \"discount\": percent (optional)}.\n    \"\"\"\n    total = Decimal(\"0\")\n    for item in items:\n        price = parse_price(item[\"price\"])\n        price = apply_discount(pr

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Assistant
Now `export.py` — implement RFC 4180 quoting and add annotations:

### Tool call: edit_file
{"file_path": "/workspace/inventory/export.py", "new_string": "\"\"\"Export helpers.\"\"\"\nfrom typing import Any\n\nfrom .pricing import parse_price\n\n\ndef to_csv_row(item: dict[str, Any]) -> str:\n    \"\"\"Format one item as a CSV row: name,price,qty (price with 2 decimals).\n\n    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    price = parse_price(item[\"price\"])\n    name = item[\"name\"]\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f\"{name},{price:.2f},{item['qty']}\"", "old_string": "\"\"\"Export helpers.\"\"\"\nfrom .pricing import parse_price\n\n\ndef to_csv_row(item):\n    \"\"\"Format one item as a CSV row: name,price,qty (price with 2 decimals).\n\n    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
......                                                                   [100%]
6 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
All 6 pass. Now let me verify the docstring behaviors that the visible tests don't cover, and check the Acme conventions. Let me look for any convention docs.

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom decimal import Decimal\nfrom inventory.pricing import parse_price, apply_discount\nfrom inventory.report import low_stock, total_value\nfrom inventory.export import to_csv_row\n\n# parse_price formats\nprint(parse_price('\\$1,299.50'))\nprint(parse_price('  12 '))\nprint(parse_price('1299.5'))\nprint(parse_price('(12.00)'))\nprint(parse_price('(\\$1,299.50)'))\n# rounding half up\nprint(apply_discount(Decimal('10.05'), 10))\nprint(apply_discount(Decimal('0.005'), 0))\nprint(apply_discount(Decimal('1.005'), 0))\n# low_stock strictly below + case-insensitive sort\nprint(low_stock([{'name':'Zebra','qty':1},{'name':'apple','qty':4},{'name':'Mango','qty':5}]))\nprint(low_stock([{'name':'a','qty':5}]))\n# csv quoting\nprint(to_csv_row({'name':'a,b','price':'2.5','qty':4}))\nprint(to_csv_row({'name':'a\\\"b','price':'2.5','qty':4}))\nprint(to_csv_row({'name':'plain','price':'\\$1,299.50','qty':2}))\n\""}

### Tool result
1299.50
12
1299.5
-12.00
-1299.50
9.05
0.01
1.01
['apple', 'Zebra']
[]
"a,b",2.50,4
"a""b",2.50,4
plain,1299.50,2

[Command succeeded with exit code 0]

### Assistant
All docstring behaviors work. Now let me check the Acme Python team conventions — the review bot checks against them. Let me search for any convention files.

### Tool call: execute
{"command": "cd workspace && ls -la && ls -la .. 2>/dev/null; find / -iname \"*convention*\" -o -iname \"*CONTRIBUTING*\" -o -iname \"*.acme*\" 2>/dev/null | grep -v proc | head -20"}

### Tool result
total 28
drwxr-xr-x 5 appuser appuser 4096 Oct  6 17:06 .
drwx------ 4 appuser appuser 4096 Oct  6 17:06 ..
drwxr-xr-x 3 appuser appuser 4096 Oct  6 17:06 .pytest_cache
-rwxr-xr-x 1 appuser appuser   60 Oct  6 02:57 CHANGELOG.md
-rwxr-xr-x 1 appuser appuser  124 Oct  6 02:57 README.md
drwxr-xr-x 3 appuser appuser 4096 Oct  6 03:52 inventory
drwxr-xr-x 3 appuser appuser 4096 Oct  6 03:52 tests
total 16
drwx------ 4 appuser appuser 4096 Oct  6 17:06 .
drwxrwxrwt 1 root    root    4096 Oct  6 17:07 ..
drwxr-xr-x 5 appuser appuser 4096 Oct  6 17:06 skills
drwxr-xr-x 5 appuser appuser 4096 Oct  6 17:06 workspace
/usr/share/perl/5.40.1/Test2/Manual/Contributing.pm

[Command succeeded with exit code 0]

### Assistant
No convention file present. The skill's completion checks define the conventions to follow: type annotations on all params/return values, a regression test file, and a changelog entry. Let me verify annotations are complete and add the regression tests + changelog.

### Tool call: read_file
{"file_path": "/workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "/workspace/inventory/export.py"}

### Tool result
@@ lines 1-31 of 31 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal

_CENTS = Decimal("0.01")


def parse_price(text: str) -> Decimal:
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    if negative:
        cleaned = cleaned[1:-1].strip()
    value = Decimal(cleaned)
    return -value if negative else value


def apply_discount(price: Decimal, percent: float) -> Decimal:
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(_CENTS, rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-27 of 27 @@
"""Inventory reports."""
from decimal import Decimal
from typing import Any, Iterable

from .pricing import apply_discount, parse_price


def total_value(items: Iterable[dict[str, Any]]) -> Decimal:
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items: Iterable[dict[str, Any]], threshold: int = 5) -> list[str]:
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    names = [item["name"] for item in items if item["qty"] < threshold]
    return sorted(names, key=str.lower)

### Tool result
@@ lines 1-17 of 17 @@
"""Export helpers."""
from typing import Any

from .pricing import parse_price


def to_csv_row(item: dict[str, Any]) -> str:
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = item["name"]
    if "," in name or '"' in name:
        name = '"' + name.replace('"', '""') + '"'
    return f"{name},{price:.2f},{item['qty']}"

### Assistant
All public functions have full annotations. Now let me add the regression test file and changelog entry.

### Tool call: write_file
{"file_path": "/workspace/tests/test_regressions.py", "content": "\"\"\"Regression tests for bugs fixed in the inventory package.\"\"\"\nfrom decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock\n\n\ndef test_parse_price_thousands_separator():\n    assert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\n\n\ndef test_parse_price_accounting_parentheses():\n    assert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\n\n\ndef test_parse_price_parentheses_with_currency_and_separator():\n    assert parse_price(\"($1,299.50)\") == Decimal(\"-1299.50\")\n\n\ndef test_parse_price_whitespace_and_plain():\n    assert parse_price(\"  12 \") == Decimal(\"12\")\n    assert parse_price(\"1299.5\") == Decimal(\"1299.5\")\n\n\ndef test_apply_discount_rounds_half_up():\n    assert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\n    assert apply_discount(Decimal(\"1.005\"), 0) == Decimal(\"1.01\")\n\n\ndef test_low_stock_is_strictly_below_threshold():\n    assert low_stock([{\"name\": \"pen\", \"qty\": 5}]) == []\n    assert low_stock([{\"name\": \"pen\", \"qty\": 4}]) == [\"pen\"]\n\n\ndef test_low_stock_sorted_case_insensitively():\n    items = [{\"name\": \"Zebra\", \"qty\": 1}, {\"name\": \"apple\", \"qty\": 2}]\n    assert low_stock(items) == [\"apple\", \"Zebra\"]\n\n\ndef test_to_csv_row_quotes_comma():\n    assert to_csv_row({\"name\": \"a,b\", \"price\": \"2.5\

### Tool call: edit_file
{"file_path": "/workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `parse_price` to handle thousands separators and accounting-style parentheses for negatives.\n- Fix `apply_discount` to round half up instead of the default half-even.\n- Fix `low_stock` to use a strict \"below threshold\" comparison and sort names case-insensitively.\n- Fix `to_csv_row` to apply RFC 4180 quoting to names containing commas or double quotes.\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
................                                                         [100%]
16 passed in 0.02s

[Command succeeded with exit code 0]

### Assistant
All 16 tests pass. Let me do a final verification of the complete state.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -3 && echo \"--- CHANGELOG ---\" && cat CHANGELOG.md && echo \"--- files ---\" && ls tests inventory"}

### Tool result
................                                                         [100%]
16 passed in 0.02s
--- CHANGELOG ---
# Changelog

## Unreleased
- Fix `parse_price` to handle thousands separators and accounting-style parentheses for negatives.
- Fix `apply_discount` to round half up instead of the default half-even.
- Fix `low_stock` to use a strict "below threshold" comparison and sort names case-insensitively.
- Fix `to_csv_row` to apply RFC 4180 quoting to names containing commas or double quotes.

## 0.3.1
- initial import
--- files ---
inventory:
__init__.py
__pycache__
export.py
pricing.py
report.py

tests:
__pycache__
test_regressions.py
test_report.py

[Command succeeded with exit code 0]

### Assistant
All done. The full suite passes (16 tests, 0 failures).

## Summary

I fixed four bugs in the `inventory` package, each a mismatch between the code and its docstring (the spec):

**`inventory/pricing.py`**
- `parse_price`: it only stripped `$` and whitespace, so `"$1,299.50"` raised `InvalidOperation` and accounting-style negatives like `"(12.00)"` were unsupported. It now also removes thousands separators and treats surrounding parentheses as a negative sign.
- `apply_discount`: `Decimal.quantize` defaults to `ROUND_HALF_EVEN`, contradicting the documented "round half up" rule (`10.05` at 10% gave `9.04` instead of `9.05`). It now passes `rounding=ROUND_HALF_UP` explicitly.

**`inventory/report.py`**
- `low_stock`: used `<=` though the docstring says "strictly below", and never sorted despite the documented case-insensitive alphabetical order. Now uses `<` and `sorted(..., key=str.lower)`.

**`inventory/export.py`**
- `to_csv_row`: the docstring requires RFC 4180 quoting, but names were emitted raw. Names containing a comma or double quote are now wrapped in quotes with inner quotes doubled.

**Conventions / artifacts**
- Added type annotations to every public function parameter and return value.
- Added `tests/test_regressions.py` with one test per fixed bug (10 tests).
- Added an `## Unreleased` changelog entry with one bullet per fix.

I did not modify the existing `tests/test_report.py`.