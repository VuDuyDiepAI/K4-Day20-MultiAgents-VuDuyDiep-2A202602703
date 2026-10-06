# Trạng thái thực hiện

Lab đã hoàn thành với cấu hình chính thức `deepseek:deepseek-chat`, `LAB_TEMPERATURE=0`, `recursion_limit=60`.

## Quy trình đã thực hiện
1. Cài đặt `subagents.py`, `agent.py`, `runner.py`, `curator.py`; 29 test offline đạt.
2. Chạy `baseline` và `subagents` trên tác vụ học trong container cách ly `lab-isolated`.
3. Chạy `python -m lab.curator` (3 skill hợp lệ) và `skills-auto` trên tác vụ học (sao lưu ở `results/skills-auto-dev/`).
4. Commit `hypotheses` (`60e030f`), tag `freeze` (`f6b8af7`).
5. Chạy `baseline`/`subagents` trên tác vụ đánh giá và `skills-auto` trên cả 6 tác vụ.
6. `lab.compare` -> `report/table.md`; `scripts/check_breakdown.py`; `scripts/verify_freeze.py` (OK, xem lưu ý đường dẫn Windows trong REPORT.md mục 7).

## Bằng chứng bị loại (không dùng cho bảng chính)
Lưu trong `results-infrastructure/`: Qwen3 8B local (`local-qwen3-8b/`, kèm tệp cài đặt Ollama ở `setup/`), các lần chạy bị rò rỉ khỏi sandbox (`leak-run*/`), lỗi quota/quá tải Gemini (`retry-503/`, `new-key-429/`), CRLF Windows (`windows-crlf/`), và các thử nghiệm ngân sách/hủy (`nested-budget-abort/`, `cancellation-pilot/`).

## Tái lập
Cách ly: container không mount repo, shell của tác tử chạy bằng user không đặc quyền (`setpriv` trong `make_backend`), `tasks/`, `src/`, `.env`, `results/` đặt quyền 700 cho root. Chi tiết và phân tích: `report/REPORT.md`.
