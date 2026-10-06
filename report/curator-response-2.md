=== SKILL: clean_data_format ===
---
name: clean_data_format
description: Use when data contains inconsistent formatting or missing values that need to be standardized.
---
1. Identify rows with missing or invalid data (e.g., `-999` in the `amount` column).
2. Remove or mark rows with invalid data as per the data specification.
3. Standardize date formats to `YYYY-MM-DDTHH:MM:SSZ` (UTC).
4. Normalize region names to `North`, `South`, `East`, or `West`.
5. Convert the `amount` column to integer cents, ensuring negative values are handled appropriately.
6. Ensure all rows have the correct header: `order_id,timestamp_utc,region,amount_cents`.
7. Save the cleaned data to `workspace/clean.csv`.
8. Verify that all rows are distinct and meet the specified format.
9. Check that the file `workspace/clean.csv` exists and has the correct content.
10. Confirm that no invalid or missing data remains.
=== END ===

=== SKILL: enforce_type_annotations ===
---
name: enforce_type_annotations
description: Use when functions lack type annotations as per the team's coding conventions.
---
1. Review all public functions in the package (those not starting with `_`).
2. Identify functions that do not have type annotations on parameters or return values.
3. Add appropriate type annotations to each identified function.
4. Ensure that all parameters and return types are correctly annotated.
5. Verify that the annotations match the expected data types.
6. Check that the function signatures are consistent with the docstrings.
7. Confirm that the changes adhere to the Acme Python team conventions.
8. Ensure that no existing files in `tests/` are modified.
9. Validate that all functions now have proper type annotations.
10. Confirm that the changes are ready for review and testing.
=== END ===

=== SKILL: update_changelog_and_tests ===
---
name: update_changelog_and_tests
description: Use when changes need to be documented in the changelog and regression tests added.
---
1. Identify all functions that were modified or fixed.
2. For each function, create a changelog entry in `CHANGELOG.md` under the '## Unreleased' section.
3. Format each changelog entry as: `- fix(<function name>): <short description of the fix>`.
4. Ensure at least three changelog entries are added.
5. Create a new file `tests/test_regressions.py`.
6. Add at least three test functions to `test_regressions.py`, one for each bug fixed.
7. Ensure that each test function is named clearly and covers the fixed bug.
8. Write the tests to validate the behavior of the fixed functions.
9. Verify that the `test_regressions.py` file passes all tests.
10. Confirm that the changelog and test file are correctly formatted and ready for review.
=== END ===