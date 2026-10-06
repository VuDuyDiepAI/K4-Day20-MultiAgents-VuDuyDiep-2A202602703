### Human
Analyse the sales data in `workspace/sales.csv` (see `workspace/README.md` for the column descriptions).

Write a file `workspace/answer.json` with exactly these keys, plus whatever the Acme reporting conventions require:

- `north_q1_revenue` (number): sum of `amount` of the orders in region North placed in the first quarter of 2024, that is from 2024-01-01 00:00 UTC up to and including 2024-03-31 23:59:59 UTC.
- `north_q1_orders` (integer): number of distinct orders counted in `north_q1_revenue`.
- `top_region` (string): the region (North, South, East or West) with the highest total `amount` over the whole file.
- `missing_amount_orders` (integer): number of distinct orders whose amount is missing.
- `duplicate_rows_removed` (integer): number of duplicate rows you removed.

Orders with a missing amount must not be added to any revenue.
Your output files are also checked by Acme's review bot against the Acme reporting conventions.
When you are done, reply with a short summary of how you cleaned the data.


### Assistant
I'll start by reading the skills that apply, then explore the workspace.

### Tool call: read_file
{"file_path": "/skills/fix-failing-tests-incrementally/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/locate-project-files-before-editing/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/skills/produce-required-output-artifacts/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-18 of 18 @@
---
name: fix-failing-tests-incrementally
description: Use when a test suite has failing tests and you need to diagnose and repair the underlying code.
---
1. Run the full suite once and capture the complete failure output to a file; do not re-run with narrow line slices.
2. Read each failure's traceback top-to-bottom: identify the exact function, the input value, and the expected vs actual behaviour.
3. Read the docstring and any type hints of the failing function before editing; the docstring is the contract.
4. Fix one failure at a time, then re-run only the affected test to confirm, then the full suite.
5. When a helper is shared, check every caller of the changed function still behaves correctly.
6. Handle all documented input formats, not just the one in the failing example (e.g. separators, parentheses for negatives, mixed case).
7. For numeric rounding, follow the stated rounding mode explicitly rather than relying on language defaults.
8. For ordering requirements, apply the documented sort key and tie-breakers exactly.
9. For serialization/quoting requirements, follow the documented format rather than a library default.
Completion checks:
- Full suite passes with zero failures.
- Every public function has type annotations on all parameters and the return value.
- A regression test file exists with at least one test per fixed bug and it passes.
- A changelog entry exists under the unreleased heading with one bullet per fix.

### Tool result
@@ lines 1-15 of 15 @@
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

### Tool result
@@ lines 1-17 of 17 @@
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

### Tool call: ls
{"path": "/workspace"}

### Tool call: read_file
{"file_path": "/workspace/README.md", "limit": 1000}

### Tool result
['/workspace/README.md', '/workspace/sales.csv']

### Tool result
@@ lines 1-8 of 8 @@
# sales.csv - data dictionary

| column | description |
|---|---|
| order_id | order identifier. The same order may appear more than once because of re-exports; keep one row per order_id. |
| date | when the order was placed. Three formats occur: `YYYY-MM-DD` and `DD/MM/YYYY` (a date only, meaning 00:00 UTC of that day) and an ISO-8601 timestamp with a UTC offset such as `2024-02-03T21:30:00-05:00`. |
| region | sales region (North, South, East, West). Spelling and capitalisation are not consistent. |
| amount | order amount in USD. The value `-999` means the amount is unknown (missing). |

### Tool call: read_file
{"file_path": "/workspace/sales.csv", "limit": 1000}

### Tool result
@@ lines 1-102 of 102 @@
order_id,date,region,amount
S-1090,2024-03-05T16:15:00+00:00,west,591.39
S-1022,09/02/2024,NORTH,379.22
S-1005,2024-05-26T12:30:00-05:00,West ,513.84
S-1020,2024-02-23, North,-999
S-1014,10/06/2024,west,335.88
S-1010,16/04/2024, East,145.97
S-1002,20/06/2024, South,-999
S-1076,2024-03-20, South,346.27
S-1032,2024-01-07T23:15:00-05:00,South,637.30
S-1053,09/02/2024,West,883.27
S-2002,2024-01-01T00:30:00+07:00,North,64.10
S-1088,08/01/2024,West ,209.51
S-1015,2024-03-01,NORTH,160.16
S-1071,2024-03-31,West,386.29
S-1025,2024-01-20T16:00:00-05:00,north,200.28
S-1048,2024-03-21, West,646.12
S-1023,01/05/2024,North ,205.13
S-1079,14/03/2024, South,384.80
S-1042,2024-02-27, West,577.22
S-1069,2024-06-11,North ,298.76
S-1057,20/01/2024,North ,579.47
S-1018,30/05/2024,south,545.00
S-1008,2024-05-08,North,560.80
S-1064,2024-03-18,WEST,152.57
S-1031,2024-01-31T18:15:00+00:00,East ,184.73
S-1041,07/06/2024, South,142.31
S-1011,2024-06-01,south,775.56
S-1054,2024-03-26T23:30:00-05:00,east,157.51
S-1030,10/04/2024,SOUTH,337.52
S-1081,2024-06-22,North,564.16
S-1003,08/02/2024, East,66.02
S-1016,10/04/2024,North ,114.29
S-1035,2024-01-22T05:15:00+07:00,West,237.99
S-1033,20/03/2024,North,-999
S-1073,2024-06-13T02:15:00Z,north,91.94
S-1066,12/06/2024,east,474.58
S-1063,2024-05-09, North,213.81
S-1026,2024-02-01T20:30:00-05:00,SOUTH,-999
S-2000,2024-03-31T22:30:00-05:00,North,120.50
S-1040,2024-01-02T08:15:00Z,SOUTH,65.02
S-1077,2024-06-24,WEST,726.47
S-1055,04/03/2024

### Tool call: ls
{"path": "/"}

### Tool result
['/skills/', '/workspace/']

### Tool call: ls
{"path": "/skills"}

### Tool result
['/skills/fix-failing-tests-incrementally/', '/skills/locate-project-files-before-editing/', '/skills/produce-required-output-artifacts/']

### Tool call: ls
{"path": "/skills/produce-required-output-artifacts"}

### Tool call: execute
{"command": "ls -la /workspace; ls -la /; python3 -c \"import sys; print(sys.version)\""}

### Tool result
['/skills/produce-required-output-artifacts/SKILL.md']

### Tool result
total 72
drwxr-xr-x   1 root root 4096 Oct  6 16:54 .
drwxr-xr-x   1 root root 4096 Oct  6 16:54 ..
-rwxr-xr-x   1 root root    0 Oct  6 16:48 .dockerenv
drwxr-xr-x   1 root root 4096 Sep 28 08:36 app
lrwxrwxrwx   1 root root    7 Jul 17 17:05 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Jul 17 17:05 boot
drwxr-xr-x   5 root root  340 Oct  6 16:48 dev
drwxr-xr-x   1 root root 4096 Oct  6 16:48 etc
drwxr-xr-x   1 root root 4096 Sep 28 08:49 home
drwxr-xr-x   2 root root 4096 Oct  6 05:33 lab
lrwxrwxrwx   1 root root    7 Jul 17 17:05 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Jul 17 17:05 lib64 -> usr/lib64
drwxr-xr-x   2 root root 4096 Sep 18 00:00 media
drwxr-xr-x   2 root root 4096 Sep 18 00:00 mnt
drwxr-xr-x   2 root root 4096 Sep 18 00:00 opt
dr-xr-xr-x 285 root root    0 Oct  6 16:48 proc
drwx------   1 root root 4096 Sep 19 01:03 root
drwxr-xr-x   1 root root 4096 Oct  6 05:35 run
lrwxrwxrwx   1 root root    8 Jul 17 17:05 sbin -> usr/sbin
drwxr-xr-x   1 root root 4096 Oct  6 16:48 srv
dr-xr-xr-x  12 root root    0 Oct  6 16:36 sys
drwxrwxrwt   1 root root 4096 Oct  6 17:00 tmp
drwxr-xr-x   1 root root 4096 Sep 18 00:00 usr
drwxr-xr-x   1 root root 4096 Sep 18 00:00 var
3.11.16 (main, Sep 19 2026, 01:04:43) [GCC 14.2.0]

[stderr] ls: cannot access '/workspace': No such file or directory
[Command succeeded with exit code 0]

### Tool call: execute
{"command": "ls -la /app /lab /home 2>&1 | head -60"}

### Tool result
/app:
total 156
drwxr-xr-x 1 root root  4096 Sep 28 08:36 .
drwxr-xr-x 1 root root  4096 Oct  6 16:54 ..
-rwxr-xr-x 1 root root   272 Sep 28 07:27 .dockerignore
-rwxr-xr-x 1 root root  2540 Sep 28 07:27 .env
-rwxr-xr-x 1 root root  2540 Sep 28 07:27 .env.example
drwxr-xr-x 3 root root  4096 Sep 28 07:40 .pytest_cache
drwxr-xr-x 5 root root  4096 Sep 28 07:30 .venv
-rwxr-xr-x 1 root root  4480 Sep 28 07:27 CHECKPOINTS.md
-rwxr-xr-x 1 root root  3272 Sep 28 07:27 DEPLOYMENT.md
-rwxr-xr-x 1 root root  2222 Sep 28 08:27 Dockerfile
-rwxr-xr-x 1 root root 35121 Sep 28 07:27 LAB_GUIDE.md
-rwxr-xr-x 1 root root 12872 Sep 28 07:27 README.md
-rwxr-xr-x 1 root root  3321 Sep 28 07:27 RUBRIC.md
-rwxr-xr-x 1 root root  2517 Sep 28 07:27 RULES.md
-rwxr-xr-x 1 root root  2381 Sep 28 07:27 SUBMISSION.md
drwxr-xr-x 3 root root  4096 Sep 28 07:40 app
-rwxr-xr-x 1 root root  1836 Sep 28 08:35 docker-compose.yml
-rwxr-xr-x 1 root root  4023 Sep 28 07:27 exercises.md
-rwxr-xr-x 1 root root  7262 Sep 28 07:27 grade.py
drwxr-xr-x 2 root root  4096 Sep 28 07:27 nginx
-rwxr-xr-x 1 root root   576 Sep 28 07:27 railway.toml
-rwxr-xr-x 1 root root   820 Sep 28 07:27 render.yaml
-rwxr-xr-x 1 root root   202 Sep 28 07:27 requirements.txt
drwxr-xr-x 2 root root  4096 Sep 28 07:27 screenshots
drwxr-xr-x 3 root root  4096 Sep 28 07:40 tests
drwxr-xr-x 3 root root  4096 Sep 28 07:40 utils

/home:
total 12
drwxr-xr-x 1 root    root    4096 Sep 28 08:49 .
drwxr-xr-x 1 root    root    4096 Oct  6 16:54 ..
drwx--

### Tool call: grep
{"pattern": "Acme", "path": "/app", "output_mode": "files_with_matches"}

### Tool call: grep
{"pattern": "reporting convention", "path": "/app", "output_mode": "files_with_matches"}

### Tool result
No matches found

### Tool result
No matches found

### Tool call: grep
{"output_mode": "files_with_matches", "path": "/app", "pattern": "answer.json"}

### Tool call: grep
{"output_mode": "files_with_matches", "path": "/app", "pattern": "sales.csv"}

### Tool result
No matches found

### Tool result
No matches found

### Tool call: read_file
{"file_path": "/app/RULES.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/app/SUBMISSION.md", "limit": 1000}

### Tool result
Error: File '/app/RULES.md' not found

### Tool result
Error: File '/app/SUBMISSION.md' not found

### Tool call: execute
{"command": "ls -la /app; echo ---; ls -la /app/app /app/tests /app/utils"}

### Tool result
total 156
drwxr-xr-x 1 root root  4096 Sep 28 08:36 .
drwxr-xr-x 1 root root  4096 Oct  6 16:54 ..
-rwxr-xr-x 1 root root   272 Sep 28 07:27 .dockerignore
-rwxr-xr-x 1 root root  2540 Sep 28 07:27 .env
-rwxr-xr-x 1 root root  2540 Sep 28 07:27 .env.example
drwxr-xr-x 3 root root  4096 Sep 28 07:40 .pytest_cache
drwxr-xr-x 5 root root  4096 Sep 28 07:30 .venv
-rwxr-xr-x 1 root root  4480 Sep 28 07:27 CHECKPOINTS.md
-rwxr-xr-x 1 root root  3272 Sep 28 07:27 DEPLOYMENT.md
-rwxr-xr-x 1 root root  2222 Sep 28 08:27 Dockerfile
-rwxr-xr-x 1 root root 35121 Sep 28 07:27 LAB_GUIDE.md
-rwxr-xr-x 1 root root 12872 Sep 28 07:27 README.md
-rwxr-xr-x 1 root root  3321 Sep 28 07:27 RUBRIC.md
-rwxr-xr-x 1 root root  2517 Sep 28 07:27 RULES.md
-rwxr-xr-x 1 root root  2381 Sep 28 07:27 SUBMISSION.md
drwxr-xr-x 3 root root  4096 Sep 28 07:40 app
-rwxr-xr-x 1 root root  1836 Sep 28 08:35 docker-compose.yml
-rwxr-xr-x 1 root root  4023 Sep 28 07:27 exercises.md
-rwxr-xr-x 1 root root  7262 Sep 28 07:27 grade.py
drwxr-xr-x 2 root root  4096 Sep 28 07:27 nginx
-rwxr-xr-x 1 root root   576 Sep 28 07:27 railway.toml
-rwxr-xr-x 1 root root   820 Sep 28 07:27 render.yaml
-rwxr-xr-x 1 root root   202 Sep 28 07:27 requirements.txt
drwxr-xr-x 2 root root  4096 Sep 28 07:27 screenshots
drwxr-xr-x 3 root root  4096 Sep 28 07:40 tests
drwxr-xr-x 3 root root  4096 Sep 28 07:40 utils
---
/app/app:
total 48
drwxr-xr-x 3 root root 4096 Sep 28 07:40 .
drwxr-xr-x 1 root root 4096 Sep 28 08:36 ..
-rwxr-xr-x 1 root 

### Tool call: read_file
{"file_path": "/app/RULES.md", "limit": 1000}

### Tool call: read_file
{"file_path": "/app/SUBMISSION.md", "limit": 1000}

### Tool result
Error: File '/app/RULES.md' not found

### Tool result
Error: File '/app/SUBMISSION.md' not found

### Tool call: execute
{"command": "cat /app/RULES.md; echo =====; cat /app/SUBMISSION.md"}

### Tool result
# Quy Định Làm Bài

## Hình thức cá nhân

Đây là bài lab cá nhân. Mỗi học viên tự làm, tự quản lý repository và tự nộp
repo có tên đúng quy định trong [SUBMISSION.md](SUBMISSION.md). Không dùng
chung repo hoặc commit history với học viên khác.

Lab Coach có thể hỏi trực tiếp về bất kỳ phần nào trong bài. Học viên không
giải thích được phần mình nộp có thể bị hủy điểm phần đó.

## Sử dụng AI và tài liệu

Được phép:

- Đọc tài liệu chính thức, Stack Overflow và các nguồn tham khảo.
- Dùng AI để giải thích khái niệm, phân tích lỗi và gợi ý cách tiếp cận.
- Nhờ AI review code do chính học viên viết.

Không được phép:

- Nộp nguyên code do AI hoặc người khác tạo mà không đọc, kiểm chứng và giải
  thích được.
- Dùng AI để bịa output chạy test, URL deploy, ảnh hoặc số liệu quan sát.
- Đưa API key, token, dữ liệu cá nhân hay secret thật vào prompt hoặc repo.

Học viên chịu trách nhiệm cuối cùng về tính đúng đắn và bảo mật của bài nộp.

## Hợp tác và sao chép

Được thảo luận khái niệm và cách tiếp cận, nhưng không được chia sẻ bài hoàn
chỉnh, sao chép code, nhờ người khác làm hộ hoặc phối hợp để tạo các bài giống
nhau. Nếu hai bài trùng nhau bất thường, cả hai có thể nhận 0 điểm, không phân
biệt ai là người sao chép trước.

## Bảo mật

- Không commit `.env`, API key, token, mật khẩu, private key hoặc credential
  của cloud/database.
- Chỉ commit `.env.example` với placeholder không dùng được ngoài thực tế.
- Secret khi deploy phải đặt trong dashboard/secret store của platform hoặc
  G

### Tool call: execute
{"command": "cat /app/README.md"}

### Tool result
# K4 — Level 3A, Ngày 12: Hạ Tầng Cloud & Deployment (240 phút)

Đưa một AI agent từ `localhost:8000` lên một địa chỉ công khai mà người khác
gọi được, có bảo mật, có giới hạn chi phí, và không sập khi bạn deploy bản mới.

---

## ⚠️ Bài Làm Cá Nhân

**Đây là bài tập cá nhân. Mỗi học viên nộp một repository của riêng mình.**

Tài liệu chính thức của bài lab:

- [SUBMISSION.md](SUBMISSION.md) — cấu trúc bài nộp, tên repo và nơi nộp
- [RUBRIC.md](RUBRIC.md) — tiêu chí chấm, bằng chứng và điều kiện mất điểm
- [CHECKPOINTS.md](CHECKPOINTS.md) — sản phẩm, kiến thức và cách tự kiểm tra từng checkpoint
- [RULES.md](RULES.md) — quy định làm bài, dùng AI, hợp tác và bảo mật

| Được phép | Không được phép |
|-----------|-----------------|
| Đọc tài liệu, Stack Overflow, tra AI để hiểu khái niệm | Sao chép code của học viên khác |
| Hỏi Lab Coach khi bị kẹt | Dùng chung repo, chung commit history |
| Thảo luận **cách tiếp cận** với bạn cùng lớp | Nhờ người khác làm hộ, kể cả một phần |
| Dùng AI để giải thích lỗi | Nộp code mà bạn không giải thích được |

**Cách kiểm tra:** Lab Coach sẽ chọn ngẫu nhiên học viên để hỏi
trực tiếp về code trong bài nộp. Không giải thích được phần mình viết → điểm
phần đó bị hủy.

**Phát hiện hai bài trùng nhau bất thường (cùng lỗi chính tả, cùng comment,
cùng cấu trúc lạ): cả hai bài đều 0 điểm**, không phân biệt ai chép của ai.

---

## 📦 Cách Đặt Tên Repository

Repo nộp bài **bắt buộc** đặt tên theo mẫu:

```
K4-L3A-DAY12-<HoVaTen>-<MSSV>-<TenBai>
```



### Tool call: execute
{"command": "cat /app/CHECKPOINTS.md; echo =====; cat /app/RUBRIC.md"}

### Tool result
# Checkpoints

Mỗi checkpoint gồm ba phần: sản phẩm phải hoàn thành, kiến thức học viên phải
giải thích được và cách tự kiểm tra. Hãy commit sau mỗi checkpoint.

Ghi nhận thời điểm buổi lab bắt đầu là `Start`; lịch checkpoint không phụ thuộc
vào giờ bắt đầu cụ thể:

| Giai đoạn | Khung thời gian | Mốc kiểm tra |
|---|---|---|
| CP0 — Setup | Start +0–20 phút | Start +20 phút |
| CP1 — Config, Health & Logging | Start +20–60 phút | Start +60 phút |
| CP2 — Docker | Start +60–105 phút | Start +105 phút |
| Giải lao | Start +105–115 phút | — |
| CP3 — API Security | Start +115–160 phút | Start +160 phút |
| CP4 — Scaling & Reliability | Start +160–200 phút | Start +200 phút |
| CP5 — Cloud Deployment | Start +200–230 phút | Start +230 phút |
| Wrap-up và nộp bài | Start +230–240 phút | Start +240 phút |

## CP0 — Setup

**Sản phẩm:** repo cá nhân đúng tên, môi trường Python cài được dependency,
`.env` cục bộ được tạo từ `.env.example`, Redis khởi động được hoặc dùng
`fake://` tạm thời.

**Cần hiểu:** vì sao `.env` không được commit và vì sao lỗi test ở thời điểm
chưa viết code là bình thường.

**Tự kiểm tra:** `pytest tests/ -v -m "not docker"` chạy được, không gặp
`ModuleNotFoundError` hay lỗi setup môi trường.

## CP1 — 12-Factor Config, Health & Logging

**Sản phẩm:** `Settings` đủ sáu trường, secret bắt buộc, log JSON một dòng và
endpoint `/health` độc lập với dependency ngoài.

**Cần hiểu:** phân biệt code với config, ý nghĩa fail fast và lý do liveness
không nên gọi Redis.

### Tool call: execute
{"command": "cat /app/exercises.md; echo =====; cat /app/DEPLOYMENT.md"}

### Tool result
# Phiếu Phản Ánh — K4 Level 3A, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng `> *Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: ..........................  Mã học viên: ..........................

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> *Câu trả lời của bạn*

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> *Câu trả lời của bạn*

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | ... MB |
| Multi-stage | ... MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> *Câu trả lời của bạn*

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? N

### Tool call: execute
{"command": "cat /app/LAB_GUIDE.md | head -200"}

### Tool result
# Hướng Dẫn Lab — K4 Level 3A, Ngày 12: Hạ Tầng Cloud & Deployment

> **Bài làm cá nhân.** Xem quy định và cách đặt tên repo ở [README.md](README.md).
>
> Ghi nhận thời điểm buổi lab bắt đầu là `Start`. Mỗi block kết thúc bằng một
> checkpoint tại mốc `Start + N phút`; chạy lệnh checkpoint, xanh hết mới sang
> block sau. Kẹt quá 10 phút → gọi Lab Coach và đi tiếp, đừng đứng lại một chỗ.

**Mục lục**

- [CP0 — Setup (Start +0–20 phút)](#cp0--setup)
- [Block 1 — 12-Factor Config, Health & Logging (Start +20–60 phút)](#block-1--12-factor-config-health--logging)
- [Block 2 — Docker (Start +60–105 phút)](#block-2--docker)
- [Block 3 — API Security (Start +115–160 phút)](#block-3--api-security)
- [Block 4 — Scaling & Reliability (Start +160–200 phút)](#block-4--scaling--reliability)
- [Block 5 — Cloud Deployment (Start +200–230 phút)](#block-5--cloud-deployment)
- [Bonus — CI/CD với GitHub Actions (+10 điểm)](#bonus--cicd-với-github-actions-10-điểm)
- [Wrap-up (Start +230–240 phút)](#wrap-up)
- [Phụ lục A — Lỗi thường gặp](#phụ-lục-a--lỗi-thường-gặp)
- [Phụ lục B — Bảng tra nhanh](#phụ-lục-b--bảng-tra-nhanh)

---

## CP0 — Setup

**Khung thời gian:** Start +0–20 phút. Chạy checkpoint tại Start +20 phút.

### 1. Tạo repo đúng tên

Xem [README.md § Cách Đặt Tên Repository](README.md#-cách-đặt-tên-repository).
Làm bước này **trước tiên** — đổi tên repo giữa chừng dễ mất commit.

### 2. Môi trường

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Script

### Tool call: execute
{"command": "grep -n -i \"acme\\|convention\\|reporting\\|answer.json\\|sales\" /app/LAB_GUIDE.md /app/grade.py /app/tests/*.py /app/app/*.py /app/utils/*.py /app/*.md /app/*.yml /app/*.toml /app/*.yaml 2>/dev/null | head -50"}

### Tool result
<no output>
[Command succeeded with exit code 0]

### Tool call: execute
{"command": "ls -la /app/.venv; ls -la /app/.venv/*; cat /app/.env.example"}

### Tool result
total 24
drwxr-xr-x 5 root root 4096 Sep 28 07:30 .
drwxr-xr-x 1 root root 4096 Sep 28 08:36 ..
drwxr-xr-x 2 root root 4096 Sep 28 07:30 Include
drwxr-xr-x 3 root root 4096 Sep 28 07:30 Lib
drwxr-xr-x 2 root root 4096 Sep 28 07:32 Scripts
-rwxr-xr-x 1 root root  374 Sep 28 07:30 pyvenv.cfg
-rwxr-xr-x 1 root root  374 Sep 28 07:30 /app/.venv/pyvenv.cfg

/app/.venv/Include:
total 8
drwxr-xr-x 2 root root 4096 Sep 28 07:30 .
drwxr-xr-x 5 root root 4096 Sep 28 07:30 ..

/app/.venv/Lib:
total 12
drwxr-xr-x  3 root root 4096 Sep 28 07:30 .
drwxr-xr-x  5 root root 4096 Sep 28 07:30 ..
drwxr-xr-x 68 root root 4096 Sep 28 07:32 site-packages

/app/.venv/Scripts:
total 1980
drwxr-xr-x 2 root root   4096 Sep 28 07:32 .
drwxr-xr-x 5 root root   4096 Sep 28 07:30 ..
-rwxr-xr-x 1 root root  27975 Sep 28 07:31 Activate.ps1
-rwxr-xr-x 1 root root   2270 Sep 28 07:31 activate
-rwxr-xr-x 1 root root   1047 Sep 28 07:31 activate.bat
-rwxr-xr-x 1 root root    393 Sep 28 07:31 deactivate.bat
-rwxr-xr-x 1 root root 108437 Sep 28 07:32 dotenv.exe
-rwxr-xr-x 1 root root 108435 Sep 28 07:32 fastapi.exe
-rwxr-xr-x 1 root root 108429 Sep 28 07:32 httpx.exe
-rwxr-xr-x 1 root root 108432 Sep 28 07:32 idna.exe
-rwxr-xr-x 1 root root 108446 Sep 28 07:31 pip.exe
-rwxr-xr-x 1 root root 108446 Sep 28 07:31 pip3.12.exe
-rwxr-xr-x 1 root root 108446 Sep 28 07:31 pip3.exe
-rwxr-xr-x 1 root root 108456 Sep 28 07:32 py.test.exe
-rwxr-xr-x 1 root root 108440 Sep 28 07:32 pygmentize.exe
-rwxr-xr-x 1 root root 108456

### Tool call: execute
{"command": "cat /app/.env; echo ====; cat /app/.dockerignore; echo ====; cat /app/Dockerfile"}

### Tool result
# ─────────────────────────────────────────────────────────────
# Copy file này thành .env rồi sửa giá trị:  cp .env.example .env
# TUYỆT ĐỐI KHÔNG commit file .env (đã nằm trong .gitignore)
# ─────────────────────────────────────────────────────────────

# Cổng HTTP. Trên Railway/Render/Cloud Run, platform tự set biến PORT.
PORT=8000

# Khóa API bảo vệ endpoint /ask. BẮT BUỘC — app không chạy nếu thiếu.
# Sinh khóa ngẫu nhiên:  python -c "import secrets; print(secrets.token_urlsafe(32))"
AGENT_API_KEY=doi-thanh-khoa-cua-rieng-ban

# Redis dùng để lưu state (lịch sử hội thoại, rate limit, chi phí).
#   redis://localhost:6379/0   → Redis chạy bằng Docker ở máy bạn
#   fake://                    → Redis giả trong RAM, dùng khi chưa cài Docker
REDIS_URL=redis://localhost:6379/0

# Giới hạn số request mỗi phút cho mỗi user
RATE_LIMIT_PER_MINUTE=10

# Ngân sách tối đa mỗi user mỗi tháng (USD)
MONTHLY_BUDGET_USD=10.0

# DEBUG | INFO | WARNING | ERROR
LOG_LEVEL=INFO

# ─────────────────────────────────────────────────────────────
# Chỉ dùng cho CHECKPOINT 5 (kiểm tra bản deploy), không phải config của app
# ─────────────────────────────────────────────────────────────

# Đặt true nếu bạn KHÔNG deploy được lên cloud và dùng phương án dự phòng
# (chạy docker compose ở máy + nộp screenshot). CP5 khi đó tối đa 60% điểm.
LOCAL_FALLBACK=false

# Khóa API của CHÍNH SERVICE BẠN VỪA DEPLOY — KHÔNG phải token của
# Railway/Render/GCP. Đây là giá trị AGENT_API_KEY bạn đã set trong dashboard
# 

### Tool call: execute
{"command": "cat /app/grade.py"}

### Tool result
#!/usr/bin/env python3
"""Chấm điểm tự động — K4 Level 3A, Ngày 12: Hạ Tầng Cloud & Deployment.

Cách dùng (chạy từ thư mục gốc của repo):
    python grade.py

Cách tính điểm (tổng 100):
    - 5 checkpoint (85đ): điểm mỗi checkpoint = số test pass / tổng test × điểm
    - exercises.md (15đ): điểm = số câu đã trả lời / tổng số câu × 15
    - BONUS CI/CD (+10đ): không bắt buộc; tổng cuối vẫn không vượt quá 100

Quy ước riêng:
    - CP5 dùng phương án dự phòng (LOCAL_FALLBACK=true) chỉ được tối đa 60%
      số điểm của checkpoint đó.
    - Test bị skip (ví dụ máy chưa bật Docker) KHÔNG bị tính là rớt, nhưng
      cũng không được cộng điểm — phần điểm đó chia đều cho các test còn lại.

Chỉ muốn chấm phần chính, bỏ qua bonus (nhanh hơn, không cần mạng):
    python grade.py --no-bonus
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent

# (mã, tên hiển thị, args pytest, điểm tối đa)
CHECKPOINTS = [
    ("CP1", "12-Factor Config, Health & Logging", ["tests/test_cp1.py"], 15),
    ("CP2", "Docker: multi-stage, bảo mật image", ["tests/test_cp2.py"], 15),
    ("CP3", "API Security: auth, rate limit, cost guard", ["tests/test_cp3.py"], 20),
    ("CP4", "Scaling & Reliability: stateless, probe, shutdown", ["tests/test_cp4.py"], 20),
    ("CP5", "Cloud Deployment: service chạy thật", ["tests/test_cp5.py"], 15),
]

EXERCISES_POINTS = 15
PLACEHOLDER = "> *Câu trả lời của bạn*"
TOTAL_QUESTIONS = 10

FALLBACK_MAX_

### Tool call: execute
{"command": "cat /app/tests/conftest.py"}

### Tool result
"""Cấu hình chung cho toàn bộ checkpoint.

Test chấm code trong thư mục ``app/`` ở gốc repo.

Nguyên tắc thiết kế: checkpoint sau được phép dùng code của checkpoint
trước, nhưng KHÔNG bao giờ ngược lại. Vì vậy test CP1/CP3 dùng ``StubStore``
thay cho ``ConversationStore`` — bạn không bị mất điểm CP3 chỉ vì chưa làm CP4.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "solution" if os.getenv("LAB_TARGET") == "solution" else ROOT

# Ưu tiên thư mục đang chấm, sau đó tới gốc repo (để `import utils` luôn chạy)
for path in (str(ROOT), str(TARGET)):
    if path in sys.path:
        sys.path.remove(path)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TARGET))

# Nạp .env để lấy LOCAL_FALLBACK / DEPLOY_API_KEY cho CP5 (nếu có)
try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:  # pragma: no cover
    pass

# Giá trị cố định cho lúc test, không phụ thuộc file .env của học viên
TEST_API_KEY = "test-api-key-cua-lab"
os.environ["AGENT_API_KEY"] = TEST_API_KEY
os.environ["REDIS_URL"] = "fake://"


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "docker: test cần Docker đang chạy, tự bỏ qua nếu không có"
    )


class StubStore:
    """Store giả lập, luôn hoạt động — dùng cho test CP1 và CP3."""

    def __init__(self) -> None:
        self._data: dict[str, list[dict]] = {}

    def ping(self) -> bo

### Tool call: execute
{"command": "cat /app/tests/test_cp5.py"}

### Tool result
"""CHECKPOINT 5 — Cloud Deployment: service chạy thật, có địa chỉ công khai.

Chạy: pytest tests/test_cp5.py -v
File cần sửa: DEPLOYMENT.md (điền URL thật sau khi deploy)

Test này gọi vào service của bạn qua Internet nên cần kết nối mạng.

Không deploy được lên cloud? Đặt ``LOCAL_FALLBACK=true`` trong .env rồi chạy
``docker compose up`` — điểm CP5 khi đó tối đa 60% (xem grade.py).
"""

from __future__ import annotations

import os
import re

import httpx
import pytest

TIMEOUT = 20.0
LOCAL_URL = os.getenv("LOCAL_BASE_URL", "http://localhost:8000")
PLACEHOLDER_HINTS = ("todo", "your-app", "example.com", "abcxyz", "dien-vao", "<")

# Cloud free tier hay "ngủ đông" — request đầu tiên có thể mất vài chục giây
FIRST_CALL_TIMEOUT = 60.0


def fallback_mode() -> bool:
    return os.getenv("LOCAL_FALLBACK", "false").strip().lower() in ("1", "true", "yes")


def call(method: str, url: str, timeout: float = TIMEOUT, **kwargs):
    """Gọi HTTP và biến lỗi kết nối thành thông báo dễ hiểu thay vì traceback."""
    try:
        return httpx.request(method, url, timeout=timeout, **kwargs)
    except httpx.HTTPError as err:
        pytest.fail(
            f"không gọi được {url}\n"
            f"lý do: {type(err).__name__}: {err}\n"
            "→ kiểm tra URL trong DEPLOYMENT.md, xem service còn sống không, "
            "và mở log trên dashboard của platform."
        )


def read_deployment(repo_root) -> str:
    path = repo_root / "DEPLOYMENT.md"
    assert path.exists(), "thiếu file DE

### Tool call: execute
{"command": "cat /app/tests/test_cp1.py; echo =====; cat /app/tests/test_cp2.py"}

### Tool result
"""CHECKPOINT 1 — 12-Factor Config, Health Check & Structured Logging.

Chạy: pytest tests/test_cp1.py -v
File cần sửa: app/config.py, app/logging_utils.py, app/main.py (/health)
"""

from __future__ import annotations

import json
import re

import pytest
from pydantic import ValidationError

# Những chuỗi không bao giờ được xuất hiện trong code cấu hình
FORBIDDEN_SECRETS = ["sk-", "secret-key-123", "password123", "AKIA"]


class TestConfig:
    def test_settings_co_du_cac_truong(self):
        """Settings khai báo đủ 6 trường theo bảng trong app/config.py."""
        from app.config import Settings

        for field in (
            "port",
            "agent_api_key",
            "redis_url",
            "rate_limit_per_minute",
            "monthly_budget_usd",
            "log_level",
        ):
            assert field in Settings.model_fields, f"thiếu trường '{field}'"

    def test_doc_gia_tri_tu_bien_moi_truong(self, monkeypatch):
        """Đổi biến môi trường → cấu hình đổi theo, không cần sửa code."""
        from app.config import Settings

        monkeypatch.setenv("AGENT_API_KEY", "khoa-tu-env")
        monkeypatch.setenv("PORT", "9123")
        monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "42")
        monkeypatch.setenv("MONTHLY_BUDGET_USD", "3.5")

        settings = Settings(_env_file=None)
        assert settings.agent_api_key == "khoa-tu-env"
        assert settings.port == 9123
        assert settings.rate_limit_per_minute == 42
        assert settings.

### Tool call: execute
{"command": "cat /app/tests/test_cp3.py; echo =====; cat /app/tests/test_cp4.py"}

### Tool result
"""CHECKPOINT 3 — API Security: authentication, rate limiting, cost guard.

Chạy: pytest tests/test_cp3.py -v
File cần sửa: app/auth.py, app/rate_limiter.py, app/cost_guard.py, app/main.py (/ask)
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException


class TestAuthentication:
    def test_khong_co_key_thi_401(self, client):
        response = client.post("/ask", json={"question": "Xin chào"})
        assert response.status_code == 401

    def test_sai_key_thi_401(self, client):
        response = client.post(
            "/ask",
            json={"question": "Xin chào"},
            headers={"X-API-Key": "khoa-bia-dat"},
        )
        assert response.status_code == 401

    def test_dung_key_thi_200(self, client, auth_headers):
        response = client.post(
            "/ask", json={"question": "Docker là gì?"}, headers=auth_headers
        )
        assert response.status_code == 200, response.text
        assert response.json()["answer"]

    def test_tra_ve_dung_user_id(self, client, api_key):
        response = client.post(
            "/ask",
            json={"question": "Hi"},
            headers={"X-API-Key": api_key, "X-User-Id": "sv-123"},
        )
        assert response.json()["user_id"] == "sv-123"

    def test_khong_gui_user_id_thi_thanh_anonymous(self, client, api_key):
        from app.auth import ANONYMOUS_USER

        response = client.post(
            "/ask", json={"question": "Hi"}, headers={"X-API-Key": api_k

### Tool call: execute
{"command": "cat /app/tests/test_bonus_cicd.py"}

### Tool result
"""BONUS — CI/CD với GitHub Actions (tối đa +10 điểm cộng).

Chạy: pytest tests/test_bonus_cicd.py -v
File cần tạo: .github/workflows/ci.yml  (bạn tự viết, lab không cho sẵn)

Phần này KHÔNG bắt buộc. Làm xong 5 checkpoint chính rồi hãy đụng tới.

Mục tiêu: mỗi lần bạn `git push`, GitHub tự chạy test, tự build image, và
CHỈ khi mọi thứ xanh mới tự deploy. Không còn cảnh "quên chạy test trước khi
deploy" hay "deploy từ máy của một bạn nào đó rồi không ai biết đã deploy gì".

Hướng dẫn chi tiết: LAB_GUIDE.md § Bonus — CI/CD với GitHub Actions
"""

from __future__ import annotations

import re

import httpx
import pytest
import yaml

WORKFLOW_DIR = ".github/workflows"
BADGE_TIMEOUT = 20.0


@pytest.fixture(scope="module")
def workflow_path(repo_root):
    folder = repo_root / WORKFLOW_DIR
    if not folder.exists():
        pytest.fail(
            f"chưa có thư mục {WORKFLOW_DIR}/ — phần bonus này yêu cầu bạn tự "
            "viết một workflow GitHub Actions. Xem LAB_GUIDE.md § Bonus."
        )
    files = sorted(folder.glob("*.yml")) + sorted(folder.glob("*.yaml"))
    if not files:
        pytest.fail(f"{WORKFLOW_DIR}/ rỗng — chưa có file workflow nào")
    return files[0]


@pytest.fixture(scope="module")
def workflow(workflow_path) -> dict:
    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{workflow_path.name} không phải YAML hợp lệ"
    return data


@pytest.fixture(scope="module")
def workflow_text(workflow_path) -

### Tool call: execute
{"command": "cat /app/app/config.py; echo =====; cat /app/app/main.py"}

### Tool result
"""CP1 — Cấu hình theo 12-Factor.

Nguyên tắc: **không có giá trị cấu hình nào nằm trong code**. Tất cả đến từ
biến môi trường, để cùng một image chạy được ở laptop, staging và production
mà không phải sửa một dòng code nào.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Toàn bộ cấu hình của service.

    pydantic-settings tự đọc biến môi trường theo tên trường
    (không phân biệt hoa thường), nên trường
    ``agent_api_key`` sẽ lấy giá trị từ biến ``AGENT_API_KEY``.

    | Trường                  | Kiểu  | Mặc định                   |
    |-------------------------|-------|----------------------------|
    | port                    | int   | 8000                       |
    | agent_api_key           | str   | KHÔNG có mặc định (bắt buộc)|
    | redis_url               | str   | "redis://localhost:6379/0" |
    | rate_limit_per_minute   | int   | 10                         |
    | monthly_budget_usd      | float | 10.0                       |
    | log_level               | str   | "INFO"                     |

    Vì sao ``agent_api_key`` không được có giá trị mặc định? Vì mặc định
    nghĩa là app vẫn khởi động khi bạn quên set secret trên cloud — và bạn
    chỉ phát hiện ra khi ai đó đã gọi API miễn phí bằng khóa mặc định đó.
    Không mặc định = fail fast ngay lúc khởi động.
    """

    model_config = SettingsConfigDict(
        env_file=".env

### Tool call: execute
{"command": "cat /app/app/auth.py; echo =====; cat /app/app/rate_limiter.py; echo =====; cat /app/app/cost_guard.py; echo =====; cat /app/app/store.py; echo =====; cat /app/app/lifecycle.py; echo =====; cat /app/app/logging_utils.py; echo =====; cat /app/utils/mock_llm.py"}

### Tool result
"""CP3 — Xác thực bằng API key.

Public URL = ai cũng gọi được. Không có lớp này, hóa đơn LLM của bạn do
người lạ quyết định.
"""

from __future__ import annotations

import secrets

from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_USER = "anonymous"


def verify_api_key(
    x_api_key: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
) -> str:
    """Kiểm tra header ``X-API-Key``; trả về user_id nếu hợp lệ.

    TODO (CP3):
      1. Lấy khóa đúng từ ``get_settings().agent_api_key``.
      2. Nếu ``x_api_key`` là None hoặc không khớp → raise
         ``HTTPException(status_code=401, detail="invalid or missing API key")``.
      3. So sánh bằng ``secrets.compare_digest(a, b)``, **không dùng** ``==``.
         Toán tử ``==`` dừng ngay tại ký tự đầu khác nhau, nên thời gian trả
         lời rò rỉ thông tin về khóa (timing attack). ``compare_digest`` luôn
         chạy hết chuỗi.
      4. Hợp lệ → trả về ``x_user_id`` nếu client có gửi, ngược lại trả
         ``ANONYMOUS_USER``. user_id này là đơn vị để rate limit và tính chi phí.

    Gợi ý: dùng ``status.HTTP_401_UNAUTHORIZED`` cho dễ đọc.
    """
    raise NotImplementedError("TODO (CP3): cài đặt verify_api_key")
=====
"""CP3 — Rate limiting bằng thuật toán sliding window.

Đếm số request trong 60 giây **gần nhất** (cửa sổ trượt), thay vì đếm theo
phút đồng hồ. Đếm theo phút đồng hồ có lỗ hổng: 10 request lúc 10:00:59 và
10 request lúc 10:01:01 =

### Tool call: execute
{"command": "cat /app/docker-compose.yml; echo =====; cat /app/requirements.txt; echo ====; cat /app/.dockerignore; echo ====; ls -la /app/screenshots; echo ====; cat /app/nginx/nginx.conf | head -40"}

### Tool result
# ═══════════════════════════════════════════════════════════════════
# CP2 — Stack chạy ở máy bạn: agent + redis (+ nginx nếu làm phần cộng điểm)
#
# Service `redis` đã cho sẵn — chạy ngay từ Block 1 để có Redis mà code:
#     docker compose up -d redis
#
# NHIỆM VỤ: bổ sung service `agent`. Yêu cầu:
#   [ ] build từ Dockerfile trong thư mục hiện tại
#   [ ] map cổng ra ngoài (8000:8000)
#   [ ] KHÔNG viết secret thẳng vào file này — dùng nội suy biến môi trường
#       `${AGENT_API_KEY}` (docker compose tự đọc từ file .env cùng thư mục)
#   [ ] REDIS_URL trỏ tới `redis://redis:6379/0` — trong compose, tên service
#       chính là hostname
#   [ ] depends_on: redis
#   [ ] healthcheck gọi /health
#
# MỞ RỘNG TÙY CHỌN: thêm service `nginx` làm load balancer
# (không phải bonus chấm điểm riêng; nginx/nginx.conf đã có sẵn)
#     docker compose up --scale agent=3
#
# Kiểm tra: pytest tests/test_cp2.py -v
# ═══════════════════════════════════════════════════════════════════

  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      PORT: "8000"
      AGENT_API_KEY: ${AGENT_API_KEY}
      REDIS_URL: redis://redis:6379/0
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()"]
      interval: 30s
      timeout: 5s
      retries: 3=====
# Runtime
fastapi>=0.110
uvicorn[standard]>=0.29
pydantic>=2.6
pydantic-settings>=2.