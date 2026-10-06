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
