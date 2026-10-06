# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Vu Duy Diep | 2A202602703 | Triển khai và kiểm tra harness, chạy thí nghiệm, phân tích và viết báo cáo với hỗ trợ Codex. Thông tin tên/MSSV lấy từ tên kho bài lab. |

- Mô hình chính thức: `ollama:qwen3-lab-fast:8b` (Qwen3 8B local); `LAB_TEMPERATURE=0.7`; `recursion_limit=60`, dùng nhất quán cho ba điều kiện. Context 16384, num_predict 4096, top_p 0.8, top_k 20 theo `Modelfile.lab`; adapter loopback đặt `think=false` cho mọi request chat, không thay đổi prompt/công cụ của lab.
- Budget cuối cùng: 180 giây/task trên Linux, worker cách ly và dừng cả nhóm tiến trình khi hết hạn; trace chính và usage của các request hoàn tất được chuyển về runner trước khi dừng. Thêm guard sau khi phát hiện bound recursion_limit=9999 ở graph con có thể ghi đè giới hạn graph cha. Ba baseline fast và subagents code đã hoàn tất trước guard đều dưới 180 giây nên giữ kết quả; lượt nested data chưa có record được dừng và chạy lại. Đây là thay đổi vận hành được công khai, không phải chọn lại điểm cao hơn.
- Deep Agents 0.7.21, langchain-ollama 1.1.0, Ollama SDK 0.6.3, Ollama server 0.35.1; Python 3.11.16 trên Linux trong container Docker riêng `lab-workflow-linux`. Phiên bản thư viện đầy đủ: `report/environment-linux.txt`. Cài dependency offline bằng wheel Linux sau lỗi tải mạng. Toàn bộ 29 test đạt trên Linux sau khi đổi provider. Qwen3 8B dùng context 16K, phân bổ GPU/CPU 80%/20% khi đo ban đầu; thời gian còn phụ thuộc trạng thái tải/cache của máy.
- Số lần chạy: ba baseline data-learn lỗi hạ tầng (429, 503, 429), lưu riêng trong results-infrastructure, không tính là kết quả hợp lệ; chưa có run chính thức hợp lệ. Tổng token ghi nhận của các lần lỗi: 198.547; thời gian: 438,1 giây. Chi tiết: report/STATUS.md.
- Commit của tag `freeze`: chưa tạo; chờ dữ liệu học hợp lệ và giả thuyết.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline):
- H2 (skills-auto so với baseline):
- H3 (tác vụ học so với tác vụ đánh giá):

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tour quan sát được các công cụ `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. `execute` chạy lệnh shell. Kết quả đầy đủ được lưu trong `report/tour.txt`.
2. `general-purpose` có các công cụ như tác tử chính, phù hợp nghiên cứu câu hỏi phức tạp, tìm tệp và thực hiện nhiệm vụ nhiều bước. Mỗi lần gọi mặc định không có trạng thái; subagent chỉ thấy prompt giao việc và trả một báo cáo cuối, nên phải truyền đầy đủ quy tắc và đường dẫn.
3. System prompt mặc định quan sát được là chuỗi rỗng. Mô tả `task` yêu cầu: “Put full detail in the prompt”. Mô tả `execute` yêu cầu: “Quote paths containing spaces”. Các mô tả tool cũng hướng dẫn hành vi của model.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| data-learn / baseline | north_q1_revenue | A: chưa đáp ứng đặc tả đầu ra | Grader không tìm thấy answer.json; 11 tool call chủ yếu đọc CSV và tìm sentinel, kết thúc bằng danh sách dòng thiếu tiền thay vì tạo đầu ra. |
| data-learn / baseline | north_q1_orders | A | answer.json không tồn tại; chưa có đầu ra để kiểm tra số đơn. |
| data-learn / baseline | top_region | A | answer.json không tồn tại; không thể kết luận thuật toán tổng hợp đúng hay sai. |
| data-learn / baseline | duplicate_rows_removed | B: thiếu kiểm chứng hoàn thành | Trace không có execute hoặc write_file; answer.json không tồn tại. |
| data-learn / baseline | rule_money_in_cents | E: quy ước đầu ra | Thiếu answer.json, nên không đáp ứng quy ước tiền ở dạng cents. |
| data-learn / baseline | rule_meta_block | E | Thiếu answer.json và khối metadata bắt buộc. |
| data-learn / baseline | rule_clean_csv | E | Không tạo clean.csv với schema và chuẩn hóa theo feedback RULE. |
| logs-learn / baseline | valid_structure | A | errors.json không tồn tại. |
| logs-learn / baseline | entry_count | G: dùng công cụ sai và lặp vô ích | Lặp grep literal ERROR\|CRITICAL dù tool nhắc không hỗ trợ regex; chạm GraphRecursionError sau 30 tool call, không tạo errors.json. |
| code-learn / baseline | visible_suite_passes | B | Không gọi execute để chạy suite; grader ghi 2 failed, 4 passed. |
| code-learn / baseline | csv_quoting_follows_docstring | A | Không đọc/sửa nguồn: gọi ls trên tệp Python dẫn tới not_a_directory, rồi kết thúc bằng lời hứa sẽ đọc tệp. |
| code-learn / baseline | rule_type_hints | E | Thiếu annotation của public function theo feedback RULE. |
| code-learn / baseline | rule_regression_tests | E | Không tạo tests/test_regressions.py với ít nhất ba test theo quy ước. |
| code-learn / baseline | rule_changelog | E | Không ghi các mục fix(...) dưới heading Unreleased. |

Ở baseline data-learn, cả 8 check thất bại; 5 check kỹ thuật và 3 check quy ước. Nguyên nhân quan sát trực tiếp là thiếu đầu ra, không phải đã chứng minh tính toán sai. Nhóm hoàn thành đặc tả/kiểm chứng chiếm đa số; skill nhắc lập danh sách deliverable và kiểm tra tồn tại/schema trước khi kết thúc có thể phù hợp. Check missing_amount_orders cũng thất bại vì thiếu answer.json. Không coi mỗi check là một lỗi thuật toán độc lập.

Lượt code-learn trước khi khôi phục LF được lưu riêng, không dùng để sinh skill hoặc so sánh chính thức. Trace ở lượt đó gọi format_name nhưng không định nghĩa hàm, và tuyên bố sửa CSV dù không chạy kiểm chứng; đây là bằng chứng chẩn đoán cho lần thử bị ảnh hưởng môi trường, chưa thay thế kết quả chạy lại.

Baseline chính thức đạt 1/27 check: chỉ tests_not_modified của code-learn đạt. Có 18 check kỹ thuật (1 đạt) và 9 check rule_ (0 đạt); do đó lỗi không chủ yếu là quy ước. Cả hai task dữ liệu/log đều thiếu đầu ra, còn task code không thực hiện sửa nguồn. Curator giữ GraphRecursionError như thất bại của agent dưới ngân sách cố định; các lỗi API/kết nối được bỏ qua. Khi output không tồn tại, nhiều detail chỉ là FileNotFoundError, không tiết lộ quy ước; skill tự sinh sẽ bị giới hạn bởi feedback này.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` đọc đặc tả, khảo sát code/dữ liệu/log và đề xuất kế hoạch dựa trên bằng chứng; `reviewer` chạy kiểm tra độc lập trên đầu ra và báo lỗi cụ thể. Cả hai được yêu cầu không sửa tệp. Tách điều tra và kiểm chứng để tác tử chính giữ trách nhiệm thực hiện, đồng thời tránh hai tác tử sửa cùng tệp. Mode single vẫn có general-purpose mặc định; mode subagents bổ sung hai vai trò này.
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):
- Ảnh hưởng đến token và thời gian:

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do:

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| | | | |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1. Chỉ có ba tác vụ cho mỗi vai trò learn/eval và cùng ba họ do giảng viên thiết kế; kết quả không đại diện cho mọi tác vụ agent thực tế.
2. Mỗi cấu hình chính thức chỉ chạy một lần và model có temperature=0.7; chênh lệch điểm có thể do nhiễu. So hai lần skills-auto trên tập học chỉ ước lượng nhiễu trên tập học, không tạo khoảng tin cậy cho tập đánh giá.
3. Chỉ dùng một model và một harness; kết luận không thể tự động chuyển sang provider hoặc kiến trúc khác. Token tính cả subagent nhưng trace/tool_calls chỉ thuộc luồng chính, hạn chế phân tích thao tác nội bộ subagent.
4. Lỗi quota và quá tải API có thể làm task dừng trước khi hoàn tất. Các lần có lỗi hạ tầng được lưu riêng và không dùng làm bằng chứng agent kém hoặc feedback cho curator; ngân sách tổng vẫn cần tính cả chúng.
5. Context 16K, num_predict 4096 và budget 180 giây có thể hạn chế hoàn thành nhiệm vụ; kết luận chỉ áp dụng trong ngân sách này. Pilot thinking có hai task data/logs kết thúc với final_message trống và thiếu đầu ra, được lưu riêng. Phép so sánh chính thức dùng non-thinking; không so trực tiếp tốc độ local với Gemini vì không có lượt Gemini hoàn tất hợp lệ.
6. Ollama có thể dừng sinh khi phát hiện lặp token. Lượt subagents code-learn chính thức gặp prediction aborted, token repeat limit reached; grading vẫn được giữ như một thất bại của model trong cấu hình cố định. Token callback chỉ có usage của các request đã trả metadata, nên chi phí của lượt lỗi có thể bị đánh giá thấp. Không chạy lại chỉ để chọn điểm cao hơn.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:

Sau khi thay key, một lần chạy gặp 503 do quá tải và lần thử lại gặp quota 20 request/ngày/project/model. [Quota Gemini áp dụng theo project, không theo key](https://ai.google.dev/gemini-api/docs/rate-limits); việc đổi key không bảo đảm có thêm quota. Không dùng điểm 0/8 của các lần này làm kết quả hành vi của agent hoặc làm feedback cho curator.

### Tài liệu tham khảo và cơ sở phương pháp

- README.md, GUIDE.md, RUBRIC.md và guides/pseudocode/01–05 trong kho: định nghĩa điều kiện, metric, protocol freeze và yêu cầu skill tự sinh.
- [SkillsBench, Li và cộng sự, arXiv:2602.12670v4](https://arxiv.org/abs/2602.12670v4): đánh giá cặp giữa không skill và skill biên soạn cho thấy lợi ích phụ thuộc model/harness; skill tập trung có thể tốt hơn bộ lớn. Kết quả này không bảo đảm skill tự sinh của lab có lợi.
- [SkillEvolBench, trang nhóm nghiên cứu](https://skillevolbench.github.io/): tách học trải nghiệm và triển khai sau freeze; khả năng cải thiện tại chỗ không đồng nghĩa chuyển giao ổn định khi ngữ cảnh thay đổi. Đây là căn cứ để tách learn/eval và kiểm tra quá khớp.
