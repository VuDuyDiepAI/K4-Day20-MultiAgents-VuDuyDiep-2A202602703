---
name: inspect-data-before-analysis
description: Use when analysing a raw dataset whose fields, encodings or quality are not yet known.
---
1. Locate the input file and confirm it exists and is readable before writing any analysis code.
2. Print the first few records and the total record count; never assume the schema.
3. For each field, print a sample of raw values with repr() to expose whitespace, casing, quoting and separators.
4. Identify per-field normalisation needs: trim whitespace, unify case, strip currency symbols and thousands separators, map accounting parentheses to negatives.
5. Identify missing or sentinel values (e.g. placeholder numbers) and decide explicitly whether to drop or keep them.
6. Identify duplicate records and decide the deduplication key before aggregating.
7. Convert timestamps to a single canonical timezone and format; state the target format in the output.
8. Write the cleaned dataset to the required output path with the exact header, column order and units specified.
9. Completion check: output file exists at the required path, row count matches the deduplicated known-amount records, and a spot-check of parsed values matches the raw input.
