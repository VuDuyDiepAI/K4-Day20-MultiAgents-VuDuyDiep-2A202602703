"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Delegate investigation of unfamiliar code, data or logs before implementing a solution.",
            "system_prompt": "Read the task specifications and relevant files. Identify root causes, data quality risks and output requirements. Do not modify files. Return findings with file paths and evidence, and a concise implementation plan.",
        },
        {
            "name": "reviewer",
            "description": "Delegate independent verification of changed code or generated data outputs before reporting completion.",
            "system_prompt": "Verify the supplied task requirements against actual files. Run relevant tests and independently check data transformations and output formats. Do not modify files. Report concrete failures and evidence; never claim a check passed without performing it.",
        },
    ]
