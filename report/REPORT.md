# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Vu Duy Diep | 2A202602703 | Cài đặt và kiểm tra harness, chạy thí nghiệm, phân tích và viết báo cáo (làm cá nhân, có dùng Claude Code hỗ trợ). |

- Mô hình chính thức: `deepseek:deepseek-chat` (API DeepSeek), `LAB_TEMPERATURE=0`, `recursion_limit=60`, dùng nhất quán cho cả ba điều kiện và cả hai vai trò. Mô hình local Qwen3 8B và Gemini đã thử trước đó bị loại khỏi kết quả chính thức (xem mục 9 và phụ lục).
- Môi trường: Deep Agents 0.7.21, Python 3.11 trên Linux trong container Docker `lab-isolated` (không mount thư mục repo; xem phụ lục về cách cách ly). Phiên bản thư viện: `report/environment-linux.txt`.
- Số lần chạy chính thức: mỗi (điều kiện, tác vụ) chạy một lần. `baseline` và `subagents`: 3 tác vụ học + 3 tác vụ đánh giá; `skills-auto`: 3 tác vụ học trước freeze (sao lưu ở `results/skills-auto-dev/`) và 6 tác vụ (3 học + 3 đánh giá) sau freeze.
- Tag `freeze`: commit `f6b8af7`; commit `hypotheses`: `60e030f`. `scripts/verify_freeze.py` báo `OK` (xem mục 7 về một lưu ý đường dẫn Windows).

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): `subagents` sẽ đạt điểm trung bình cao hơn `baseline` trên tác vụ đánh giá. Căn cứ từ tập học (DeepSeek, cách ly): baseline 1/27 check (code 1/10, data 0/8, logs 0/9; cả ba chạm GraphRecursionError ở giới hạn 60) so với subagents 21/27 (code 7/10, data 8/8, logs 6/9). Tôi dự đoán lợi thế giữ lại nhưng nhỏ hơn, vì chênh lệch học lớn có thể một phần do nhiễu (một lần chạy, temperature 0). Chi phí token dự kiến thấp hơn hoặc ngang baseline do baseline lặp công cụ đến khi hết giới hạn.
- H2 (skills-auto so với baseline): `skills-auto` sẽ cao hơn `baseline` nhưng thấp hơn `subagents` trên tác vụ đánh giá. Căn cứ: ba skill sinh ra (fix-failing-tests-incrementally, locate-project-files-before-editing, produce-required-output-artifacts) mang tính quy trình chung; trên tập học skills-auto đạt 9/27 (code 9/10, data 0/8, logs 0/9), tức chỉ cải thiện ở code, còn data/logs vẫn chạm giới hạn đệ quy. Phần lớn check quy ước (rule_) trong tập đánh giá là quy ước mới nên skill không thể biết trước; tôi chỉ kỳ vọng cải thiện ở nhóm check kỹ thuật của code-eval.
- H3 (tác vụ học so với tác vụ đánh giá): điểm trên tác vụ đánh giá sẽ thấp hơn tác vụ học ở mọi điều kiện, đặc biệt `skills-auto`, vì tác vụ đánh giá thêm một quy ước mới và dùng dữ liệu khác; khoảng cách học-đánh giá của skills-auto sẽ lớn hơn của subagents, vì skill chỉ mã hóa kinh nghiệm của tập học.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tour quan sát được các công cụ `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. `execute` chạy lệnh shell. Kết quả đầy đủ được lưu trong `report/tour.txt`.
2. `general-purpose` có các công cụ như tác tử chính, phù hợp nghiên cứu câu hỏi phức tạp, tìm tệp và thực hiện nhiệm vụ nhiều bước. Mỗi lần gọi mặc định không có trạng thái; subagent chỉ thấy prompt giao việc và trả một báo cáo cuối, nên phải truyền đầy đủ quy tắc và đường dẫn.
3. System prompt mặc định quan sát được là chuỗi rỗng. Mô tả `task` yêu cầu: “Put full detail in the prompt”. Mô tả `execute` yêu cầu: “Quote paths containing spaces”. Các mô tả tool cũng hướng dẫn hành vi của model.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Dữ liệu: `results/baseline/*-learn` (DeepSeek, cách ly). Baseline học đạt 1/27 check. Cả ba tác vụ kết thúc bằng `GraphRecursionError` (giới hạn 60) sau 32 đến 37 lượt công cụ.

| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng |
|---|---|---|---|
| code-learn | parse_price_all_formats | C: không sửa nguyên nhân gốc | `wrong for: ['$1,299.50', '(12.00)', '$1,000,000.00']`; trace lặp lệnh `pytest ... \| sed -n 'N,Mp'` cắt dòng thay vì sửa mã, rồi chạm giới hạn. |
| code-learn | other_caller_fixed | C | `to_csv_row returned '<InvalidOperation>'`: hàm gọi `parse_price` chưa được sửa. |
| code-learn | discount_rounds_half_up | A: bỏ qua đặc tả | `wrong for: [('10.05', 10, '9.05'), ('0.05', 50, '0.03') ...]` (docstring yêu cầu làm tròn half-up). |
| code-learn | low_stock_follows_docstring, csv_quoting_follows_docstring | A | `low_stock returned ['b', 'A', 'c']`; `to_csv_row returned 'Desk, large "oak",10.00,2'` (sai so với docstring). |
| code-learn | visible_suite_passes | B: không kiểm chứng | `2 failed, 4 passed`; tác tử không đưa bộ test về xanh trước khi dừng. |
| code-learn | rule_type_hints, rule_regression_tests, rule_changelog | E: quy ước tổ chức | `RULE: every public function ... has type annotations`; `RULE: add tests/test_regressions.py ...`; `RULE: record each fix in CHANGELOG.md under '## Unreleased'`. |
| data-learn | 8/8 check | F/B: không tạo đầu ra | Mọi check kỹ thuật báo `FileNotFoundError ... answer.json`; 32 lượt công cụ, không có `write_file` tạo `answer.json` hay `clean.csv` trước khi chạm giới hạn. |
| logs-learn | 9/9 check | B | `errors.json` không tồn tại sau 32 lượt công cụ (chạm giới hạn), nên cả check kỹ thuật lẫn `rule_*` đều thất bại. |

Nhóm lỗi chiếm đa số là không hoàn thành (B/F): tác tử khám phá và lặp lệnh đến hết ngân sách lượt thay vì viết đầu ra; kèm nhóm E ở code-learn. Bằng chứng phủ định: `check_breakdown.py` cho baseline học là 1/18 check kỹ thuật và 0/9 check quy ước, nên lỗi **không** chủ yếu là quy ước mà là không hoàn thành nhiệm vụ. Ở data/logs không có đầu ra để chấm nên không thể kết luận nhóm D (dữ liệu bẩn) có xảy ra hay không. Một skill nhắc "ghi đầu ra sớm và kiểm tra sau khi ghi" và "chạy bộ test đầy đủ một lần, không cắt dòng" có thể phòng ngừa nhóm này.

Lưu ý cách ly: các lần chạy đầu tiên (lưu ở `results-infrastructure/leak-run*/`) cho thấy tác tử đọc được thư mục `tasks/` trong container (gồm `check.py` và dữ liệu đánh giá). Các lần đó bị loại, không dùng cho phân loại hay curator; xem phụ lục.

## 5. Điều kiện `subagents` (Phần 2.3)

- Subagent đã định nghĩa: `explorer` (đọc đặc tả, khảo sát code/dữ liệu/log, đề xuất kế hoạch) và `reviewer` (kiểm chứng độc lập đầu ra, báo lỗi cụ thể); cả hai không sửa tệp, nhằm tách điều tra/kiểm chứng khỏi thực hiện để tránh hai tác tử sửa cùng tệp.
- `subagent_calls` trên tập học: code-learn=1, data-learn=0, logs-learn=1; trên tập đánh giá: code-eval=1, data-eval=0, logs-eval=0. Lệnh `task` quan sát được trong trace chọn `general-purpose`, không chọn `explorer`/`reviewer`. Việc 0 lần gọi ở data là hợp lệ: tác tử chính tự làm toàn bộ.
- Điểm: subagents học 21/27 (code 7/10, data 8/8, logs 6/9) so với baseline 1/27. Tuy vậy data-learn đạt 8/8 với `subagent_calls=0`, nên khác biệt đến từ tác tử chính hoặc ngẫu nhiên, không từ việc giao việc. Chưa thể quy công cho đa tác tử.
- Token trung bình mỗi lần chạy: baseline 559.743, subagents 477.482 (thấp hơn khoảng 15%). Trace chỉ có luồng chính; hoạt động bên trong subagent không hiện ra.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy trên phản hồi (`detail`) và vết của `baseline` tác vụ học cách ly (không dùng tác vụ đánh giá), ghi 3 skill hợp lệ. Các lần curator trước (trên dữ liệu bị rò rỉ và trên Qwen3) bị loại và lưu ở `results-infrastructure/`. Không sửa tay skill; không xóa skill nào của lần chạy cuối.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai | Độ dài, description, skills_read (dev) |
|---|---|---|---|
| fix-failing-tests-incrementally | Tổng quát cho gói Python có test lỗi; không nêu tên hàm hay đáp án, nhưng có ví dụ dạng giá trị (dấu ngoặc cho số âm, làm tròn, quoting) rút từ tác vụ học. | Phần lớn đúng. Hướng dẫn "chạy bộ test một lần, không cắt dòng" nhắm đúng hành vi lặp `sed -n`. Hạn chế: chỉ nhắc type hints, regression test, changelog, không biết các quy ước mới. | 18 dòng; description nêu đúng tình huống; được đọc ở code-learn. |
| locate-project-files-before-editing | Tổng quát. | Đúng nhưng chủ yếu là kiểm tra thận trọng chung; không giải quyết việc hết ngân sách lượt. | 15 dòng; được đọc ở cả 3 tác vụ học. |
| produce-required-output-artifacts | Tổng quát cho mọi tác vụ ghi đầu ra. | Đúng hướng (liệt kê đầu ra, kiểm tra sau khi ghi) nhưng 8 bước dài, không ép ghi sớm nên không ngăn việc hết lượt trước khi ghi. | 17 dòng; được đọc ở data/logs học. |

- Phần 3.4 (dev, trước freeze): mọi lần chạy đều đọc skill (`skills_read` ≥ 3), tức skill được dùng. Điểm: code-learn 9/10, data-learn 0/8, logs-learn 0/9, so với baseline 1/10, 0/8, 0/9. Skill chỉ cải thiện code-learn (còn thiếu `rule_changelog`); ở data/logs tác tử vẫn chạm giới hạn đệ quy và không tạo đầu ra, nên skill đã đọc nhưng không đủ.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 1/10 | 7/10 | 9/10 |
| data-learn | 0/8 | 8/8 | 0/8 |
| logs-learn | 0/9 | 6/9 | 0/9 |
| code-eval | 7/11 | 8/11 | 9/11 |
| data-eval | 0/9 | 0/9 | 0/9 |
| logs-eval | 0/10 | 6/10 | 0/10 |
| **Mean score - learning tasks** | 0.03 | 0.79 | 0.30 |
| **Mean score - evaluation tasks** | 0.21 | 0.44 | 0.27 |
| **Mean tokens per run** | 559,743 | 477,482 | 426,599 |
| **Runs that read a skill** | 2/6 | 1/6 | 6/6 |

Phân tách check (`python scripts/check_breakdown.py`):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval      7/18         0/12         489,248      1/3
baseline      learn     1/18         0/9          630,237      1/3
subagents     eval     13/18         1/12         591,571      1/3
subagents     learn    18/18         3/9          363,393      0/3
skills-auto   eval      7/18         2/12         432,371      3/3
skills-auto   learn     7/18         2/9          420,827      3/3
```

Các lần chạy có `error`: 13 trong 18 lần chạy chính thức dừng bằng `GraphRecursionError` (giới hạn 60), gồm toàn bộ lần chạy của baseline (trừ code-eval) và skills-auto ở data/logs, và 4 lần của `subagents`. Chúng được giữ làm kết quả hành vi (không phải lỗi hạ tầng) và chấm trên đầu ra tại thời điểm dừng. Không lần chạy nào có `skills_modified = true`.

`verify_freeze.py` báo `OK` sau khi chuẩn hóa dấu phân cách đường dẫn khi băm: trên Windows script gốc băm đường dẫn tương đối bằng `\`, khác băm trong container (`/`), dù ba tệp SKILL.md giống hệt từng byte (đã so sha256). Đó là sai khác của công cụ, không phải thay đổi skill.

## 8. Phân tích

1. **Học và đánh giá.** So với baseline (học 0,03; đánh giá 0,21), `subagents` cải thiện cả học (0,79) và đánh giá (0,44); `skills-auto` cải thiện học (0,30) và đánh giá (0,27) ít hơn. Với skills-auto, lợi ích tập trung ở code (code-learn 1→9/10, code-eval 7→9/11) và biến mất ở data/logs (0 điểm ở cả học và đánh giá). Khoảng cách học–đánh giá của `subagents` (0,79→0,44) lớn hơn của `skills-auto` (0,30→0,27), nhưng điều này phản ánh chủ yếu data-learn 8/8 của subagents (không liên quan skill) hơn là quá khớp skill.
2. **Kỹ thuật so với quy ước.** Check quy ước ở tập đánh giá: baseline 0/12, subagents 1/12, skills-auto 2/12; skills-auto chỉ đạt các check quy ước của code-eval (code-eval chỉ mất `rule_changelog` và `rule_version_bump`). Quy ước **mới** của code-eval (`rule_version_bump`) thất bại ở cả ba điều kiện vì skill (chỉ được học từ phản hồi tập học) không biết quy ước này.
3. **Ví dụ.** Skill giúp: ở code-learn, `rule_type_hints` và `rule_regression_tests` đạt ở skills-auto (baseline thất bại cả hai) vì skill `fix-failing-tests-incrementally` liệt kê chúng ở "Completion checks". Skill không giúp: data-learn và logs-learn (skills đã được đọc nhưng không được làm theo; tác tử vẫn dùng 32 đến 37 lượt khám phá mà không tạo `answer.json`/`errors.json`); skill `produce-required-output-artifacts` thiếu quy tắc "ghi bản nháp đầu ra sớm".
4. **Chi phí.** Token trung bình: baseline 559.743; subagents 477.482; skills-auto 426.599. Điểm đánh giá trung bình trên mỗi 1 triệu token: baseline 0,43; subagents 0,74; skills-auto 0,62. Subagents hiệu quả nhất, nhưng vì `subagent_calls` thường là 0 hoặc 1 nên lợi thế chủ yếu do tác tử chính hoàn thành tác vụ, không rõ do giao việc. Đa tác tử không bị phạt chi phí trong thí nghiệm này.
5. **Rò rỉ và quá khớp.** Phát hiện rò rỉ ở các lần chạy đầu (tác tử đọc `tasks/*/check.py` và dữ liệu `*-eval` qua shell không giới hạn). Biện pháp: chạy lại toàn bộ trong container không mount repo, shell tác tử chạy bằng user không đặc quyền (`setpriv`), `tasks/`, `src/`, `.env`, `results/` đặt quyền 700 cho root, xóa skill cũ khỏi container; kiểm tra `ls /srv/lab/tasks` trả `Permission denied`. Trace cuối chỉ còn nhắc `tasks/` ở chỗ bị từ chối. Skill cuối không chứa tên tác vụ đánh giá hay đáp án.
6. **Nhiễu.** Cùng bộ skill, điểm tác vụ học trước freeze (dev) và sau freeze giống hệt (code 9/10, data 0/8, logs 0/9) nhưng token khác nhiều: data 590.412 → 852.096 (+44%), logs 446.119 → 276.326 (−38%), code 132.435 → 134.061. Điểm ổn định phần lớn nhờ trần đệ quy, nhưng token dao động mạnh; vì vậy chênh lệch token dưới khoảng 40% giữa các điều kiện không đáng tin, và chênh lệch điểm từ một lần chạy chưa có khoảng tin cậy.

## 9. Hạn chế và tính hợp lệ

1. Chỉ 3 tác vụ mỗi vai trò, cùng ba họ do giảng viên thiết kế; mỗi tác vụ có 8 đến 11 check nên một check đổi 0,09 đến 0,12 điểm. Kết quả không đại diện cho mọi tác vụ.
2. Mỗi cấu hình chạy một lần; không có khoảng tin cậy. Đo nhiễu chỉ có cho skills-auto trên tập học, cho thấy điểm ổn định nhưng token dao động đến 44%.
3. Một mô hình, một harness (DeepSeek, `recursion_limit=60`). Giới hạn đệ quy quyết định kết quả: 13/18 lần chạy dừng vì chạm giới hạn, nên điểm 0 ở data/logs phản ánh hết ngân sách lượt chứ không chắc là "không biết làm". Tăng giới hạn có thể đổi thứ hạng các điều kiện.
4. Cách ly chưa hoàn hảo: tác tử vẫn thấy cây thư mục container (không đọc được `tasks/`, `src/`); `verify_freeze.py` cần chuẩn hóa đường dẫn trên Windows (mục 7).
5. Các lần chạy bị rò rỉ, Qwen3 và Gemini bị loại; số lần chạy và chi phí thực tế cao hơn số được báo cáo (xem phụ lục).
6. Token chỉ gồm các request đã trả metadata nên có thể thấp hơn thực tế; trace chỉ chứa luồng chính, không thấy hoạt động bên trong subagent.

## 10. Kết luận

Trong thí nghiệm này, `subagents` đạt điểm đánh giá trung bình cao nhất (0,44), tiếp theo `skills-auto` (0,27) và `baseline` (0,21); lợi thế của subagents chủ yếu đến từ tác tử chính hoàn thành tác vụ (`subagent_calls` thường là 0 hoặc 1). Skill tự sinh chỉ giúp ở họ `code` (code-eval 7/11 → 9/11) và không giúp data/logs, nơi tác tử hết ngân sách lượt trước khi ghi đầu ra; quy ước mới của tập đánh giá (`rule_version_bump`) không được skill phủ. Phát hiện quan trọng là một lỗi cách ly cho phép tác tử đọc bộ chấm, buộc phải chạy lại. Kết luận chỉ áp dụng cho một lần chạy, một mô hình và `recursion_limit=60`. Đề xuất tiếp theo: thêm vào skill quy tắc "ghi bản nháp đầu ra sớm", ghi nhận giới hạn đệ quy, và lặp lại ít nhất 3 lần để đo nhiễu.

## Phụ lục

- Lệnh đã chạy (trong container `lab-isolated`, `python -m lab.<...>`, `--recursion-limit 60`): `runner --condition baseline --tasks learn`; `runner --condition subagents --tasks learn`; `curator`; `runner --condition skills-auto --tasks learn`; (commit `hypotheses`, tag `freeze`); `runner --condition baseline --tasks eval`; `runner --condition subagents --tasks eval`; `runner --condition skills-auto --tasks all`; `compare > report/table.md`; `scripts/check_breakdown.py`; `scripts/verify_freeze.py`.
- Thử thách mở rộng: không thực hiện.
- Bằng chứng bị loại (`results-infrastructure/`): `local-qwen3-8b/` (Qwen3 8B local, điểm gần 0), `leak-run/` và `leak-run2/` (tác tử đọc được `tasks/` hoặc skill cũ; sau đó cách ly bằng container riêng và user không đặc quyền), `retry-503/`, `new-key-429/` (quota Gemini free), `windows-crlf/` (hash test lệch do CRLF), `nested-budget-abort/`, `cancellation-pilot/`.

### Tài liệu tham khảo và cơ sở phương pháp

- README.md, GUIDE.md, RUBRIC.md và guides/pseudocode/01–05 trong kho: định nghĩa điều kiện, metric, protocol freeze và yêu cầu skill tự sinh.
- [SkillsBench, Li và cộng sự, arXiv:2602.12670v4](https://arxiv.org/abs/2602.12670v4): lợi ích của skill phụ thuộc mô hình/harness.
- [SkillEvolBench](https://skillevolbench.github.io/): tách học trải nghiệm và triển khai sau freeze; cải thiện tại chỗ không đồng nghĩa chuyển giao ổn định.
