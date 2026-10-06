### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

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
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/skills/', '/workspace/']

### Tool call: ls
{"path": "/workspace/bookings"}

### Tool call: ls
{"path": "/workspace/tests"}

### Tool call: read_file
{"file_path": "/workspace/README.md"}

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: read_file
{"file_path": "/workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "/workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Assistant
Now let me run the test suite to capture the failures.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40"}

### Tool result
/lab/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings/timeutil.py:18: ValueError
________________________ test_billable_blocks_rounds_up ________________________

>   ???
E   assert 1 == 2
E    +  where 1 = billable_blocks(20)

/lab/tasks/code-eval/workspace/tests/test_bookings.py:10: AssertionError
=========================== short test summary info ============================
FAILED tests/test_bookings.py::test_total_minutes_mixed_formats - ValueError:...
FAILED tests/test_bookings.py::test_billable_blocks_rounds_up - assert 1

### Assistant
Three bugs identified. Let me fix them one at a time.

**Bug 1: `parse_duration`** — only handles `"1h30m"`. Docstring requires `"2h"`, `"45m"`, `"1:30"`, `"45"`, and whitespace tolerance.

### Tool call: write_file
{"file_path": "/workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n_HOURS_MINUTES_RE = re.compile(r\"(\\d+)h(\\d+)m\")\n_HOURS_RE = re.compile(r\"(\\d+)h\")\n_MINUTES_RE = re.compile(r\"(\\d+)m\")\n_CLOCK_RE = re.compile(r\"(\\d+):(\\d+)\")\n_BARE_MINUTES_RE = re.compile(r\"(\\d+)\")\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    stripped = text.strip()\n\n    m = _HOURS_MINUTES_RE.fullmatch(stripped)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n\n    m = _HOURS_RE.fullmatch(stripped)\n    if m:\n        return int(m.group(1)) * 60\n\n    m = _MINUTES_RE.fullmatch(stripped)\n    if m:\n        return int(m.group(1))\n\n    m = _CLOCK_RE.fullmatch(stripped)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n\n    m = _BARE_MINUTES_RE.fullmatch(stripped)\n    if m:\n        return int(m.group(1))\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
.F.                                                                      [100%]
=================================== FAILURES ===================================
________________________ test_billable_blocks_rounds_up ________________________

>   ???
E   assert 1 == 2
E    +  where 1 = billable_blocks(20)

/lab/tasks/code-eval/workspace/tests/test_bookings.py:10: AssertionError
=========================== short test summary info ============================
FAILED tests/test_bookings.py::test_billable_blocks_rounds_up - assert 1 == 2
1 failed, 2 passed in 0.02s

[Command succeeded with exit code 0]

### Assistant
**Bug 2: `billable_blocks`** — uses banker's rounding instead of always rounding up, and doesn't validate negatives.

### Tool call: write_file
{"content": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return math.ceil(minutes / block)\n", "file_path": "/workspace/bookings/billing.py"}

### Tool result
Updated file /workspace/bookings/billing.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
All visible tests pass. Now the third bug — `add_slot` uses a mutable default argument, which the docstring explicitly forbids (separate calls must not share state). The visible test only covers a single call.

### Tool call: write_file
{"content": "\"\"\"Schedule helpers.\"\"\"\nfrom typing import Iterable, List, Optional\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: str, slots: Optional[List[str]] = None) -> List[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return list(slots or []) + [slot]\n", "file_path": "/workspace/bookings/schedule.py"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Assistant
Now let me verify the docstring contracts thoroughly, including edge cases the visible tests don't cover.

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\n\n# parse_duration: all documented formats + whitespace\ncases = {'1h30m':90,'2h':120,'45m':45,'1:30':90,'45':45,' 1h30m ':90,' 2h ':120,' 45 ':45,' 1:30 ':90}\nfor k,v in cases.items():\n    got = parse_duration(k)\n    assert got == v, (k, got, v)\n    assert isinstance(got, int), (k, type(got))\nprint('parse_duration ok')\n\n# bad input still raises\nfor bad in ['', 'abc', '1h30', 'h30m', '1.5h', '-5m']:\n    try:\n        parse_duration(bad); print('NO RAISE', repr(bad))\n    except ValueError: pass\nprint('parse_duration errors ok')\n\n# billable_blocks: round up, exact multiples, zero, negative\nassert billable_blocks(16) == 2\nassert billable_blocks(15) == 1\nassert billable_blocks(0) == 0\nassert billable_blocks(1) == 1\nassert billable_blocks(30) == 2\nassert billable_blocks(31) == 3\nassert billable_blocks(20, block=10) == 2\nassert billable_blocks(21, block=10) == 3\ntry:\n    billable_blocks(-1); print('NO RAISE negative')\nexcept ValueError: pass\nprint('billable_blocks ok')\n\n# add_slot: no shared state\nassert add_slot('a') == ['a']\nassert add_slot('b') == ['b']\nassert add_slot('a') == ['a']\nassert add_slot('c', ['a','b']) == ['a','b','c']\nbase = ['a']\nout = add_slot('b', base)\nassert out == ['a','b'] and base == ['a'], (

### Tool result
parse_duration ok
parse_duration errors ok
billable_blocks ok
add_slot ok
total_minutes ok
slot_end ok
ALL CONTRACT CHECKS PASSED

[Command succeeded with exit code 0]

### Assistant
All contracts hold. Now let me check the Acme Python team conventions — the skill mentions type annotations on all parameters and return values, a regression test file, and a changelog entry.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5; echo \"---\"; python -c \"\nimport inspect\nfrom bookings import timeutil, billing, schedule, calendar_export\nfor mod in (timeutil, billing, schedule, calendar_export):\n    for name, fn in vars(mod).items():\n        if inspect.isfunction(fn) and fn.__module__ == mod.__name__:\n            sig = inspect.signature(fn)\n            missing = [p for p in sig.parameters.values() if p.annotation is inspect.Parameter.empty]\n            print(f'{mod.__name__}.{name}: ret={sig.return_annotation!r} missing={[p.name for p in missing]}')\n\""}

### Tool result
...                                                                      [100%]
3 passed in 0.01s
---
bookings.timeutil.parse_duration: ret=<class 'int'> missing=[]
bookings.billing.billable_blocks: ret=<class 'int'> missing=[]
bookings.schedule.total_minutes: ret=<class 'int'> missing=[]
bookings.schedule.add_slot: ret=typing.List[str] missing=[]
bookings.calendar_export.slot_end: ret=<class 'inspect._empty'> missing=['start_minute', 'duration_text']

[Command succeeded with exit code 0]

### Assistant
`slot_end` is missing annotations. Let me add them.

### Tool call: write_file
{"content": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n", "file_path": "/workspace/bookings/calendar_export.py"}

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Assistant
Now the regression test file (one test per fixed bug) and the changelog entry.

### Tool call: write_file
{"content": "\"\"\"Regression tests for bugs fixed in the bookings package.\n\nOne test per fixed bug. These complement tests/test_bookings.py.\n\"\"\"\nimport pytest\n\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n\n# --- Bug 1: parse_duration only accepted the \"1h30m\" form -------------------\n\n\n@pytest.mark.parametrize(\n    (\"text\", \"expected\"),\n    [\n        (\"1h30m\", 90),\n        (\"2h\", 120),\n        (\"45m\", 45),\n        (\"1:30\", 90),\n        (\"45\", 45),\n        (\" 1h30m \", 90),\n        (\" 2h \", 120),\n        (\" 45m \", 45),\n        (\" 1:30 \", 90),\n        (\" 45 \", 45),\n    ],\n)\ndef test_parse_duration_supported_formats(text, expected):\n    result = parse_duration(text)\n    assert result == expected\n    assert isinstance(result, int)\n\n\n@pytest.mark.parametrize(\"text\", [\"\", \"abc\", \"1h30\", \"h30m\", \"1.5h\", \"-5m\"])\ndef test_parse_duration_rejects_bad_input(text):\n    with pytest.raises(ValueError):\n        parse_duration(text)\n\n\ndef test_total_minutes_accepts_all_formats():\n    assert total_minutes([\"1h30m\", \"2h\"]) == 210\n    assert total_minutes([\"45\", \"1:30\"]) == 135\n    assert total_minutes([]) == 0\n\n\ndef test_slot_end_uses_parsed_duration():\n    assert slot_end(600, \"1h30m\") == 690\n    assert slot_end(0, \"45\") == 45\n\n\n# --- Bug 2: bi

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: edit_file
{"file_path": "/workspace/CHANGELOG.md", "old_string": "## Unreleased\n\n## 1.4.2", "new_string": "## Unreleased\n- Fix `parse_duration` to accept all documented formats (`\"2h\"`, `\"45m\"`, `\"1:30\"`, bare minutes) and to ignore surrounding whitespace.\n- Fix `billable_blocks` to always round up (a partial block is billed as a full block) and to raise `ValueError` for negative minutes.\n- Fix `add_slot` to return a new list instead of sharing state through a mutable default argument.\n\n## 1.4.2"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -10"}

### Tool result
.................................                                        [100%]
33 passed in 0.03s

[Command succeeded with exit code 0]

### Assistant
All 33 tests pass. Let me do a final verification of the complete state.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -3; echo \"=== annotations ===\"; python -c \"\nimport inspect\nfrom bookings import timeutil, billing, schedule, calendar_export\nok = True\nfor mod in (timeutil, billing, schedule, calendar_export):\n    for name, fn in vars(mod).items():\n        if inspect.isfunction(fn) and fn.__module__ == mod.__name__:\n            sig = inspect.signature(fn)\n            missing = [p.name for p in sig.parameters.values() if p.annotation is inspect.Parameter.empty]\n            if missing or sig.return_annotation is inspect.Signature.empty:\n                ok = False; print('MISSING', mod.__name__, name, missing)\nprint('all annotated' if ok else 'INCOMPLETE')\n\"; echo \"=== git status ===\"; git status --short 2>/dev/null || echo \"(no git)\""}

### Tool result
.................................                                        [100%]
33 passed in 0.05s
=== annotations ===
all annotated
=== git status ===
(no git)

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "/workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-9 of 9 @@
# Changelog

## Unreleased
- Fix `parse_duration` to accept all documented formats (`"2h"`, `"45m"`, `"1:30"`, bare minutes) and to ignore surrounding whitespace.
- Fix `billable_blocks` to always round up (a partial block is billed as a full block) and to raise `ValueError` for negative minutes.
- Fix `add_slot` to return a new list instead of sharing state through a mutable default argument.

## 1.4.2
- initial import

### Assistant
All done. The full suite passes (33 tests) and every function matches its docstring.

## Summary

I found three bugs in `workspace/bookings/`, all of which were only partially covered by the visible tests, so I fixed them against the docstrings (the spec) rather than just the failing assertions.

**`bookings/timeutil.py` — `parse_duration`**
The regex only matched the `"1h30m"` form, so `"2h"` raised `ValueError`. The docstring documents five formats plus whitespace tolerance. I rewrote it to handle `"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, and bare minutes (`"45"`), stripping surrounding whitespace, and to still raise `ValueError` for genuinely bad input. Added type annotations.

**`bookings/billing.py` — `billable_blocks`**
Used `round()`, which is banker's rounding — `20/15 = 1.33` rounded to `1` instead of `2`. The docstring says a partial block is always billed as a full block, so I switched to `math.ceil`. Also added the documented `ValueError` for negative `minutes`, which was missing entirely. Added type annotations.

**`bookings/schedule.py` — `add_slot`**
Used a mutable default argument (`slots=[]`) and mutated it, so separate calls shared state — the exact behaviour the docstring forbids. The visible test only made a single call, so it passed. I changed the default to `None` and return a new list, leaving the caller's list untouched. Added type annotations to both functions here.

**Supporting changes**
- `bookings/calendar_export.py`: added the missing parameter/retur