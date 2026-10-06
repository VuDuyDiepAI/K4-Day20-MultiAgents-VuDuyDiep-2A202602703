=== SKILL: clean-data-format ===
---
name: clean-data-format
description: Use when data contains inconsistent or invalid formatting that needs normalization.
---
1. Identify all rows with invalid or inconsistent data in the dataset.
2. Normalize region names to match the canonical spelling: North, South, East, West.
3. Convert date strings to a standardized format: YYYY-MM-DDTHH:MM:SSZ (UTC).
4. Replace any occurrence of `-999` in the amount column with `NULL` or remove the row.
5. Ensure the amount column is stored as an integer in cents.
6. Remove any rows that have missing or invalid data in critical fields.
7. Validate that all entries in the amount column are non-negative and represent valid monetary values.
8. Ensure the final output has the header order_id, timestamp_utc, region, and amount_cents.
9. Write the cleaned data to a new CSV file named `workspace/clean.csv`.
10. Verify that the file contains only distinct orders with known amounts.
11. Confirm that the file meets the specified schema and formatting requirements.
12. Ensure that the file is saved in the correct directory and has the correct file name.
13. Check that all entries have the correct time zone and date format.
14. Ensure that the amount is stored as an integer in cents and not as a float.
15. Confirm that all entries have valid region names.
16. Verify that the file is properly formatted and ready for use.
17. Ensure that the file is saved without any extra characters or formatting issues.
18. Check that the file is properly structured and contains no extra or missing columns.
19. Confirm that the file is ready for further processing or analysis.
20. Final check to ensure the file meets all the specified rules and requirements.
=== END ===

=== SKILL: fix-code-structure ===
---
name: fix-code-structure
description: Use when code lacks proper type annotations or does not follow team conventions.
---
1. Review all public functions in the package to ensure they have type annotations on all parameters and return values.
2. Identify any functions that do not have proper type annotations.
3. Add type annotations to all missing parameters and return values.
4. Ensure that the function names are descriptive and follow the team's naming conventions.
5. Check that all functions are properly documented with docstrings that describe their purpose and expected inputs/outputs.
6. Verify that the functions follow the team's coding standards and conventions.
7. Ensure that the code is well-organized and follows a consistent structure.
8. Check that all functions are properly imported and referenced.
9. Ensure that the code is free of syntax errors and follows PEP8 guidelines.
10. Review the code for any potential issues that could cause the test suite to fail.
11. Make sure that all functions are properly tested and that the test suite covers all edge cases.
12. Ensure that the code is maintainable and easy to understand.
13. Verify that all functions are properly exported and accessible.
14. Check that the code is properly formatted and that all indentation is consistent.
15. Ensure that all functions are properly documented and that their docstrings are accurate.
16. Confirm that the code is ready for review and that it meets the team's quality standards.
17. Final check to ensure that the code is clean, well-documented, and follows all team conventions.
=== END ===

=== SKILL: update-documents ===
---
name: update-documents
description: Use when documentation or changelog needs to be updated with fixes and changes.
---
1. Review the list of fixes made to the codebase.
2. For each fix, identify the function name and a short description of the change.
3. Update the CHANGELOG.md file by adding a new bullet point under the '## Unreleased' section.
4. Ensure that each bullet point follows the format: `- fix(<function name>): <short description>`.
5. Add at least three bullet points to the changelog.
6. Verify that the changelog is formatted correctly and follows the team's documentation standards.
7. Ensure that the changelog is saved in the correct directory and has the correct file name.
8. Check that the changelog is up-to-date and includes all recent changes.
9. Confirm that the changelog is properly structured and that all entries are clear and concise.
10. Ensure that the changelog is free of any formatting issues or errors.
11. Review the changelog to ensure that all entries are properly formatted and follow the team's guidelines.
12. Final check to ensure that the changelog is ready for review and meets the team's documentation standards.
=== END ===