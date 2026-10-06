# Trạng thái thực hiện workflow

## Đã hoàn thành

- Triển khai get_subagents: explorer điều tra, reviewer kiểm chứng độc lập.
- Triển khai make_backend/build_agent đúng hằng prompt, không kế thừa API key.
- Triển khai run_task: sandbox tạm, hash skill, timestamp, token, tool/subagent/skill đọc, grading, trace và JSON.
- Triển khai curate_skills: chỉ lấy dữ liệu learn không có lỗi hạ tầng, kiểm tra skill trước khi ghi, không gọi model khi không có check thất bại.
- Dùng AIMessage.text để đọc văn bản từ content block của Gemini, giữ nguyên message trong agent.
- 29 test đạt trên Linux trước thí nghiệm; sau cải tiến giữ trace bằng stream, toàn bộ 29 test tiếp tục đạt (14,13 giây).
- Smoke test Gemini 3.5 Flash trên Linux trả OK. Cấu hình: google_genai:gemini-3.5-flash, temperature=1, recursion-limit=60.
- Tạo REPORT.md, điền cấu hình và câu hỏi tour; lưu tour.txt và environment-linux.txt.

## Lỗi hạ tầng và bằng chứng

### Tiếp tục với key mới

- Lần đầu với key mới: 503 UNAVAILABLE do model quá tải; 181,3 giây, 18.766 token, năm lượt công cụ. Trace xác nhận đọc README, khảo sát file và đọc CSV nhưng chưa tạo answer.json. Lưu tại results-infrastructure/retry-503/baseline/data-learn/.
- Thử lại một lần: 429 RESOURCE_EXHAUSTED, giới hạn 20 request/ngày/project/model; retryDelay 34.536 giây, khoảng 9 giờ 36 phút từ lúc báo lỗi. 93,3 giây, 3.122 token, một lượt công cụ. Lưu tại results-infrastructure/new-key-429/baseline/data-learn/.
- Không có baseline hợp lệ sau hai lần này. Không chạy task khác, curator hoặc eval khi quota đã hết.
- Tổng ba lần baseline lỗi hạ tầng: 198.547 token ghi nhận, 438,1 giây; không đưa vào bảng điểm chính thức.
- [Google xác nhận quota tính theo project, không theo API key](https://ai.google.dev/gemini-api/docs/rate-limits). Đổi key trong cùng project không đặt lại quota. Cần project/provider có đủ quota hoặc chờ đặt lại; kiểm tra hạn mức thực tế ở Google AI Studio.
- Báo cáo đã bổ sung thiết kế subagent, hạn chế và tài liệu phương pháp; giả thuyết và kết quả vẫn chờ dữ liệu thật.

### Lần lỗi trước khi đổi key

Baseline data-learn chạy 163,5 giây, ghi nhận 176.659 token rồi gặp GoogleRateLimitError / 429 RESOURCE_EXHAUSTED.
API báo giới hạn 20 request/ngày/project/model của generate_content_free_tier_requests và retryDelay 66.172 giây, khoảng 18 giờ 23 phút từ lúc báo lỗi.
Không lấy điểm 0/8 này làm kết quả thí nghiệm và không dùng lỗi làm feedback cho curator.
Bằng chứng: results-infrastructure/baseline/data-learn/run.json và trace.md.

Lần lỗi dùng invoke nên mất danh sách message khi API ném ngoại lệ: tool_calls=0 và trace trống không chứng minh agent chưa gọi công cụ.
Sau lần lỗi, runner dùng stream_mode=values để giữ trạng thái cuối khi có lỗi, vẫn cộng token qua callback và giữ định nghĩa metric.

## Chưa thực hiện

- Sáu kết quả học hợp lệ của baseline/subagents; phân loại lỗi và phân tích giao việc.
- Chạy curator thực, đánh giá skill và ba lần thử skills-auto trên tập học.
- Viết giả thuyết có căn cứ từ tập học, commit hypotheses và tag freeze.
- Chín lần eval và ba lần skills-auto learn chính thức sau freeze.
- Bảng so sánh, phân tích và kết luận theo số liệu.

Chưa tạo tag freeze; chưa chạy hoặc phân tích task eval. Không có skill giả hoặc điểm tự tạo.

## Cấu hình Ollama local hiện tại

**Cấu hình chính thức mới:** `ollama:qwen3-lab-fast:8b`, temperature=0.7, context 16384, num_predict 4096, top_p=0.8, top_k=20, think=false. Adapter loopback `Ollama-NoThink.py` dùng API think=false được Ollama hỗ trợ, giữ nguyên prompt/công cụ; native port 11435 và Docker host.docker.internal:11435. Smoke test native/Docker trả OK, 2 token đầu ra. `Run-Lab.ps1` tự khởi động adapter bằng `Start-LabModel.ps1`.

Runner hiện dùng worker Linux cách ly, budget 180 giây/task, truyền main messages và usage callback về parent trong quá trình chạy; khi hết hạn dừng nhóm tiến trình rồi grade. Đã kiểm tra một nested thread cố ý treo: deadline dừng worker, giữ partial trace và hoàn tất grading. Toàn bộ 29 test đạt sau thay đổi. Graph con của langchain/deepagents có bound recursion_limit=9999; lượt subagents data chưa kết thúc được dừng, ghi tại results-infrastructure/nested-budget-abort, chạy lại có guard. Ba baseline fast và subagents code đã hoàn tất trước guard đều dưới 180 giây. Curator giữ các lỗi budget/graph/model repetition như failure hành vi; bỏ lỗi API/kết nối hạ tầng.

Các baseline Qwen3 thinking data/logs trước đây được chuyển tới results-infrastructure/local-thinking-pilot; không dùng cho curator hay so sánh chính thức. Lượt subagents code thinking chưa kết thúc đã dừng, không có run.json và không có số liệu cuối. Một lượt code được xếp hàng sai đã dừng sớm; không có run.json, không tính vào số lượt hoàn tất. Giữ các số liệu pilot phía dưới như lịch sử cấu hình cũ. Chưa chạy eval hoặc tạo freeze. Đang chạy lại baseline và subagents learn với cấu hình fast nhất quán.

Đã chuyển `.env` sang `ollama:qwen3-lab:8b`, temperature=0.6. Ollama 0.35.1 chạy trên Windows; model Qwen3 8B tải thành công và alias được tạo từ `Modelfile.lab` (context 16384, num_predict 4096). Docker gọi model qua `http://host.docker.internal:11434`; `Run-Lab.ps1` đặt biến này cho từng lệnh. Smoke test trả về `OK`; đủ 29 test đạt sau khi cài langchain-ollama 1.1.0 và ollama SDK 0.6.3. GPU/CPU ghi nhận 80%/20% với bộ nhớ model 7.8 GB. Chi tiết tái lập: `LOCAL_MODEL.md`.

Baseline `data-learn` local đã hoàn tất: 0/8, error=null, 867.6 giây, 43110 token, 4 tool call. Agent sửa dữ liệu nguồn nhưng không tạo answer.json hoặc clean.csv; final_message trống. Đây là lỗi hoàn thành nhiệm vụ, không phải quota API.

Lượt `code-learn` đầu tiên: 0/10, 286.4 giây, 22096 token, 5 tool call. Đã phát hiện check tests_not_modified thất bại do checkout Windows dùng CRLF: SHA-256 thực tế efb5e7650d4f03356e8353d209fbcfe81505ce2fd648bd558d5ada6e8b92ff19, trong khi byte LF gốc từ Git khớp hash grader 79e05f4cc2e62a4f606d210b0b08a2cc21777245bc2f6ad244a126e9a2aee00d. Lưu riêng tại results-infrastructure/windows-crlf/baseline/code-learn, không dùng cho curator. Đã khôi phục đúng byte gốc của các test được grader fingerprint và thêm .gitattributes để giữ LF cho tasks. Không sửa nội dung mã/test PROVIDED. Phải chạy lại baseline code-learn trước curator.

Docker từng dừng giữa chuỗi task; đã khởi động lại. Tiếp tục logs-learn baseline và ba task subagents learn, rồi chạy lại code-learn baseline. Các thống kê Gemini ở trên là lịch sử hạ tầng, không phải kết quả của cấu hình local. Model thinking mất nhiều thời gian mỗi lượt; không khởi chạy trùng task khi tiến trình hiện tại còn chạy.

## Tiếp tục với runtime hiện tại

Container lab-workflow-linux giữ runtime Linux; nếu đã dừng, dùng docker start lab-workflow-linux.
Container đọc .env từ repo khi mỗi tiến trình Python khởi động, không cần đưa key vào câu lệnh.
Từ PowerShell tại thư mục gốc, chạy tuần tự và kiểm tra error=null:

```powershell
.\Run-Lab.ps1 -m lab.runner --condition baseline --tasks data-learn --recursion-limit 60
.\Run-Lab.ps1 -m lab.runner --condition baseline --tasks code-learn logs-learn --recursion-limit 60
.\Run-Lab.ps1 -m lab.runner --condition subagents --tasks learn --recursion-limit 60
```

Nếu quota tiếp tục lỗi, không chạy tiếp các lệnh. Một task có nhiều request; 20 request/ngày có thể không đủ cho một task, càng không đủ toàn bộ lab trong một buổi.
Nếu đổi model/provider, ghi cấu hình mới và dùng nhất quán cho toàn bộ ba điều kiện; không trộn số liệu.
Khi sáu kết quả học hợp lệ đã có, phân tích mục 4/5 rồi mới chạy:

```powershell
.\Run-Lab.ps1 -m lab.curator
.\Run-Lab.ps1 -m lab.runner --condition skills-auto --tasks learn --recursion-limit 60
```

Đọc và đánh giá skill, sao lưu results/skills-auto thành results/skills-auto-dev; viết H1–H3 và freeze theo WORKFLOW.md trước bất kỳ lệnh eval nào.

## Môi trường và cách tái lập

Image Python 3.12 trong Dockerfile gốc không tải được layer do lỗi mạng.
Đã dùng image Python 3.11.16 có sẵn day12-agent:prod trong container riêng, cài dependency lab bằng wheel Linux được pip kiểm tra hash. Không chạy entrypoint ứng dụng cũ.
Git được cài trong container để verify_freeze chạy trên cùng hệ Linux và hash đường dẫn nhất quán.
.lab-wheels/, .venv-wsl/, .uv-cache/ được git bỏ qua.
WSL Ubuntu đã được cài python3.14-venv và tạo .venv-wsl; cài dependency trong WSL đã được dừng vì Docker sẵn sàng. Không coi .venv-wsl là runtime hoàn chỉnh, chưa dùng WSL chạy task API và không trộn với kết quả Docker.
Tái lập runtime mới khi mạng ổn định bằng Dockerfile gốc và cài git trong container, hoặc WSL theo WORKFLOW.md.
Phiên bản runtime thực tế: environment-linux.txt.
