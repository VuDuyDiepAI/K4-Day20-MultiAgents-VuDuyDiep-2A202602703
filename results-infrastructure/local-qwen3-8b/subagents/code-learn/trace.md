### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: task
{"description": "Fix the source code of the `inventory` package in the folder `workspace/` so that the whole test suite passes and every function does what its docstring says. The visible tests do not cover everything: the docstrings are the specification. Do not modify the existing files in `tests/`. Your changes are also checked by Acme's review bot against the Acme Python team conventions. The task requires analyzing the docstrings, identifying discrepancies between the implementation and the specification, and making the necessary changes to the source code.", "subagent_type": "general-purpose"}

### Tool result
I will analyze the source code of the `inventory` package to ensure that every function behaves according to its docstring. Here's my plan:

1. **Understand the specifications**:
   - Review the docstrings of each function to understand what they are supposed to do.

2. **Compare with the implementation**:
   - Check if the implementation matches the specification in the docstrings.

3. **Fix discrepancies**:
   - Modify the source code to align the implementation with the specifications.

4. **Ensure code quality**:
   - Make sure the changes adhere to Acme's Python team conventions.

Let's start by analyzing the functions in the `inventory` package.

### Step 1: Analyze the `export.py` module

#### Function: `to_csv_row`
**Docstring**:
```python
"""Format one item as a CSV row: name,price,qty (price with 2 decimals).

A name that contains a comma or a double quote is wrapped in double quotes,
and every double quote inside it is doubled (RFC 4180).
"""
```

**Implementation**:
```python
def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'
```

**Analysis**:
- The function correctly formats the price to 2 decimal places.
- It does not handle the wrapping of names containing commas or double q