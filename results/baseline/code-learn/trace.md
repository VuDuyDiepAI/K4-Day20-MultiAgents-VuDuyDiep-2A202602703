### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: ls
{"path": "/workspace/inventory"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool call: ls
{"path": "/workspace/inventory/export.py"}

### Tool result
Error: Path '/workspace/inventory/export.py': not_a_directory

### Tool call: ls
{"path": "/workspace/inventory/pricing.py"}

### Tool result
Error: Path '/workspace/inventory/pricing.py': not_a_directory

### Tool call: ls
{"path": "/workspace/inventory/report.py"}

### Tool result
Error: Path '/workspace/inventory/report.py': not_a_directory

### Assistant
It seems there was an issue with the file paths. Let me try to read the content of the `export.py`, `pricing.py`, and `report.py` files to understand their contents and identify any issues that might be causing the test suite to fail. I'll start by reading the content of these files.