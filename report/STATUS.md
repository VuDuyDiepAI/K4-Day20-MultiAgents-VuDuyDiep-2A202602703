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

## Tiếp tục khi quota/API sẵn sàng

Container lab-workflow-linux giữ runtime Linux; nếu đã dừng, dùng docker start lab-workflow-linux.
Container đọc .env từ repo khi mỗi tiến trình Python khởi động, không cần đưa key vào câu lệnh.
Từ PowerShell tại thư mục gốc, chạy tuần tự và kiểm tra error=null:

```powershell
docker exec lab-workflow-linux python -m lab.runner --condition baseline --tasks data-learn --recursion-limit 60
docker exec lab-workflow-linux python -m lab.runner --condition baseline --tasks code-learn logs-learn --recursion-limit 60
docker exec lab-workflow-linux python -m lab.runner --condition subagents --tasks learn --recursion-limit 60
```

Nếu quota tiếp tục lỗi, không chạy tiếp các lệnh. Một task có nhiều request; 20 request/ngày có thể không đủ cho một task, càng không đủ toàn bộ lab trong một buổi.
Nếu đổi model/provider, ghi cấu hình mới và dùng nhất quán cho toàn bộ ba điều kiện; không trộn số liệu.
Khi sáu kết quả học hợp lệ đã có, phân tích mục 4/5 rồi mới chạy:

```powershell
docker exec lab-workflow-linux python -m lab.curator
docker exec lab-workflow-linux python -m lab.runner --condition skills-auto --tasks learn --recursion-limit 60
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
