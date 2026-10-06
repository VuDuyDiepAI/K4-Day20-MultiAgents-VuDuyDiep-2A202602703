# Chạy lab bằng Ollama local

Cấu hình hiện tại dùng Qwen3 8B, không cần API key. Ollama chạy trên Windows; backend agent chạy trong Linux qua container `lab-workflow-linux`.

```powershell
ollama pull qwen3:8b
ollama create qwen3-lab-fast:8b -f Modelfile.lab
.venv\Scripts\python.exe -m pip install -e .
.\Start-LabModel.ps1
python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').text)"
```

`.env` dùng:

```dotenv
LAB_MODEL=ollama:qwen3-lab-fast:8b
LAB_TEMPERATURE=0.7
OLLAMA_HOST=http://127.0.0.1:11435
```

Để tránh cấu hình Azure được ưu tiên, giữ các biến endpoint/key/deployment Azure trống. Các khóa provider khác không cần xóa; chúng không được dùng khi chọn Ollama.

Container hiện tại đã cài dependency và kiểm tra đủ 29 test. Chạy agent từ PowerShell bằng wrapper để kết nối tới Ollama trên Windows:

```powershell
docker start lab-workflow-linux
.\Run-Lab.ps1 -m pytest -q
.\Run-Lab.ps1 -m lab.runner --condition baseline --tasks learn --recursion-limit 60
```

`Run-Lab.ps1` tự kiểm tra/khởi động adapter và đặt `OLLAMA_HOST=http://host.docker.internal:11435` cho tiến trình trong container. Đây là wrapper cho runtime đã tạo trên máy này; trên máy mới cần tạo runtime Linux theo README trước.

Ollama chạy trên port 11434; adapter `Ollama-NoThink.py` chỉ lắng nghe loopback port 11435 và đặt `think=false` trên request `/api/chat`, theo [API thinking của Ollama](https://docs.ollama.com/capabilities/thinking). Prompt và công cụ của lab được chuyển nguyên vẹn. `Start-LabModel.ps1` chạy adapter ẩn và kiểm tra `/lab-config`; gọi script này trước lệnh Python native sau khi khởi động lại máy. Cần Ollama đang chạy.

Model alias `qwen3-lab-fast:8b` dùng chung trọng số với `qwen3:8b`; cấu hình context và sampling được ghi trong `Modelfile.lab`. Đã kiểm tra câu trả lời `OK`. `ollama ps` ghi nhận context 16384 và phân bổ 80% GPU / 20% CPU trên máy này.

Runner Linux cách ly agent trong một worker và áp dụng deadline mặc định 180 giây/task (`LAB_TASK_TIMEOUT_SECONDS`). Khi hết hạn, dừng cả nhóm tiến trình của worker, giữ trace/token đã nhận và vẫn chấm đầu ra trong sandbox. Giới hạn này chặn cả subagent lặp vô hạn; CLI vẫn dùng recursion-limit=60 cho graph chính. Mọi task của phép so sánh dùng cùng budget 180 giây. Token của request bị cắt giữa chừng chưa trả metadata có thể không được ghi nhận.

Qwen3 8B hỗ trợ gọi công cụ nhưng chất lượng hoàn thành và tuân thủ quy tắc phải đo bằng bài lab. Model local vẫn dùng tài nguyên máy. Các kết quả Gemini lỗi hạ tầng và pilot Qwen3 thinking trong `results-infrastructure/` được giữ riêng, không dùng cho curator hoặc so sánh ba điều kiện. Temperature 0.7 và top_p 0.8 theo khuyến nghị [Qwen3 non-thinking](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html).

Tiếp tục theo `WORKFLOW.md`: chỉ chạy tập học trước khi viết giả thuyết và freeze skills; chưa chạy tập đánh giá trước checkpoint đó.
