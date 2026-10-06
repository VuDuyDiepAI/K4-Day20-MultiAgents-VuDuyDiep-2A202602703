### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace/inventory"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool call: ls
{"path": "/workspace/inventory/tests"}

### Tool result
Error: Path '/workspace/inventory/tests': path_not_found

### Assistant
The tests directory does not exist. I will proceed to fix the source code in the `inventory` package to ensure that every function does what its docstring says and that the test suite passes. I will not modify the existing files in `tests/`.

I will start by examining the source code files in the `inventory` package. Let's first look at the files in the `inventory` directory.