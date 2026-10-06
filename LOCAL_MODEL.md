# Chạy lab bằng Ollama local

Cấu hình hiện tại dùng Qwen3 8B, không cần API key. Ollama chạy trên Windows; backend agent chạy trong Linux qua container `lab-workflow-linux`.

```powershell
ollama pull qwen3:8b
ollama create qwen3-lab:8b -f Modelfile.lab
.venv\Scripts\python.exe -m pip install -e .
python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').text)"
```

`.env` dùng:

```dotenv
LAB_MODEL=ollama:qwen3-lab:8b
LAB_TEMPERATURE=0.6
OLLAMA_HOST=http://localhost:11434
```

Để tránh cấu hình Azure được ưu tiên, giữ các biến endpoint/key/deployment Azure trống. Các khóa provider khác không cần xóa; chúng không được dùng khi chọn Ollama.

Container hiện tại đã cài dependency và kiểm tra đủ 29 test. Chạy agent từ PowerShell bằng wrapper để kết nối tới Ollama trên Windows:

```powershell
docker start lab-workflow-linux
.\Run-Lab.ps1 -m pytest -q
.\Run-Lab.ps1 -m lab.runner --condition baseline --tasks learn --recursion-limit 60
```

`Run-Lab.ps1` đặt `OLLAMA_HOST=http://host.docker.internal:11434` cho tiến trình trong container. Đây là wrapper cho runtime đã tạo trên máy này; trên máy mới cần tạo runtime Linux theo README trước.

Model alias `qwen3-lab:8b` dùng chung trọng số với `qwen3:8b`; cấu hình context và sampling được ghi trong `Modelfile.lab`. Đã kiểm tra câu trả lời `OK`. `ollama ps` ghi nhận context 16384 và phân bổ 80% GPU / 20% CPU trên máy này.

Qwen3 8B hỗ trợ gọi công cụ nhưng chất lượng hoàn thành và tuân thủ quy tắc phải đo bằng bài lab. Model local vẫn dùng tài nguyên máy và có thể chậm. Các kết quả Gemini lỗi hạ tầng trong `results-infrastructure/` được giữ riêng, không dùng cho curator hoặc so sánh ba điều kiện.

Tiếp tục theo `WORKFLOW.md`: chỉ chạy tập học trước khi viết giả thuyết và freeze skills; chưa chạy tập đánh giá trước checkpoint đó.
