---
name: fix-failing-tests
description: Use when a test suite has failing tests that must be made to pass without breaking existing behaviour.
---
1. Run the full suite first and capture the summary line; note every failing test name.
2. For each failure, re-run with output narrowed to the failing test (e.g. slice the traceback) so the assertion and actual value are visible.
3. Read the docstring or spec of the function under test before editing; treat documented formats and edge cases as the contract.
4. Reproduce the failure in a one-off snippet with the exact input from the traceback before changing code.
5. Fix the root cause in the source, not the test; re-run the single test, then the whole suite.
6. Check every other caller of the changed function still works; a fix that breaks a caller is not done.
7. Add one regression test per bug fixed in a dedicated regression test file; run it and confirm it passes.
8. Record each fix as a bullet under an "## Unreleased" heading in the changelog, one bullet per fixed function.
9. Ensure every public function (name not starting with "_") has type annotations on all parameters and the return value.
10. Completion check: full suite green, regression file green, changelog has at least one bullet per fix, annotations present.
