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
