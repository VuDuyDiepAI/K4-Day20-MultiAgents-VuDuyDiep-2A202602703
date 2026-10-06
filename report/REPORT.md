# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Vu Duy Diep | 2A202602703 | Triển khai và kiểm tra harness, chạy thí nghiệm, phân tích và viết báo cáo với hỗ trợ Codex. Thông tin tên/MSSV lấy từ tên kho bài lab. |

- Mô hình hiện tại: `ollama:qwen3-lab:8b` (Qwen3 8B local); `LAB_TEMPERATURE=0.6`; `recursion_limit=60`, dùng nhất quán cho ba điều kiện. Context 16384, num_predict 4096, top_p 0.95, top_k 20 theo `Modelfile.lab`.
- Deep Agents 0.7.21, langchain-google-genai 4.4.0; Python 3.11.16 trên Linux trong container Docker riêng `lab-workflow-linux`. Phiên bản thư viện đầy đủ: `report/environment-linux.txt`. Cài dependency offline bằng wheel Linux sau lỗi tải mạng. Toàn bộ 29 test đạt trên Linux trước khi chạy task thật.
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
| | | | |

Nhận xét: nhóm lỗi nào chiếm đa số? Skill có thể phòng ngừa nhóm đó không?

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
2. Mỗi cấu hình chính thức chỉ chạy một lần và model có temperature=0.6; chênh lệch điểm có thể do nhiễu. So hai lần skills-auto trên tập học chỉ ước lượng nhiễu trên tập học, không tạo khoảng tin cậy cho tập đánh giá.
3. Chỉ dùng một model và một harness; kết luận không thể tự động chuyển sang provider hoặc kiến trúc khác. Token tính cả subagent nhưng trace/tool_calls chỉ thuộc luồng chính, hạn chế phân tích thao tác nội bộ subagent.
4. Lỗi quota và quá tải API có thể làm task dừng trước khi hoàn tất. Các lần có lỗi hạ tầng được lưu riêng và không dùng làm bằng chứng agent kém hoặc feedback cho curator; ngân sách tổng vẫn cần tính cả chúng.

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
