# DOCX to JSON Converter API với AI Support 🤖

API Flask để chuyển đổi file Word (.docx) thành JSON với hỗ trợ AI tạo quiz từ bất kỳ tài liệu nào (PDF, DOCX, Excel).

## ✨ Tính năng

### **Xử lý truyền thống:**

-   Quiz format: 1 câu hỏi với 4 đáp án (từ file DOCX có format)
-   Q&A format: 1 câu hỏi với 1 đáp án (từ file DOCX có format)

### **🤖 AI-Powered Features:**

-   **Tạo quiz từ bất kỳ tài liệu nào**: PDF, DOCX, Excel
-   **Không cần format cụ thể**: AI đọc và hiểu nội dung
-   **Tùy chọn độ khó**: Easy, Medium, Hard
-   **Số lượng câu hỏi linh hoạt**: 1-50 câu
-   **Hỗ trợ tiếng Việt**: AI tạo câu hỏi bằng tiếng Việt

### **Xử lý đồng thời:**

-   ThreadPoolExecutor với 10 workers
-   Sync và Async processing
-   Queue system và load balancing
-   Automatic cleanup

## 🚀 Cài đặt

### 1. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

### 2. Cấu hình OpenAI API:

```bash
# Windows
set OPENAI_API_KEY=your-openai-api-key

# Linux/Mac
export OPENAI_API_KEY=your-openai-api-key
```

Hoặc chỉnh sửa file `config.py`:

```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

### 3. Chạy setup (optional):

```bash
python setup.py
```

## 🏃 Chạy Server

```bash
python app_ai.py
```

Server: `http://localhost:5000`

## 📚 API Endpoints

### **Traditional Endpoints (Formatted DOCX only)**

#### Quiz Format

```http
POST /api/quiz
Content-Type: multipart/form-data
Body: file=formatted_quiz.docx
```

#### Q&A Format

```http
POST /api/qa
Content-Type: multipart/form-data
Body: file=formatted_qa.docx
```

### **🤖 AI-Powered Endpoints (Any document)**

#### AI Quiz Generation

```http
POST /api/ai-quiz?async=true
Content-Type: multipart/form-data
Body:
  file=document.pdf
  num_questions=20
  difficulty=medium
```

#### AI Q&A Generation

```http
POST /api/ai-qa?async=true
Content-Type: multipart/form-data
Body:
  file=document.xlsx
  num_questions=15
```

### **Monitoring Endpoints**

```http
GET /api/health                 # Health check
GET /api/server-status          # Server load + AI status
GET /api/status/{task_id}       # Task status check
GET /                           # API documentation
```

## 💡 Cách sử dụng

### **AI Quiz Generation (Python)**

```python
import requests

# Tạo quiz từ PDF
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {
        'num_questions': 20,
        'difficulty': 'medium'  # easy, medium, hard
    }
    response = requests.post(
        'http://localhost:5000/api/ai-quiz?async=true',
        files=files,
        data=data
    )

if response.status_code == 202:
    task_data = response.json()
    task_id = task_data['task_id']

    # Check status
    while True:
        status = requests.get(f'http://localhost:5000/api/status/{task_id}')
        result = status.json()

        if result['status'] == 'completed':
            questions = result['result']['questions']
            print(f"Generated {len(questions)} questions!")
            break

        time.sleep(2)
```

### **JavaScript/Frontend Example**

```javascript
// Upload file và tạo quiz
const formData = new FormData();
formData.append("file", fileInput.files[0]);
formData.append("num_questions", "15");
formData.append("difficulty", "medium");

fetch("http://localhost:5000/api/ai-quiz?async=true", {
    method: "POST",
    body: formData,
})
    .then((response) => response.json())
    .then((data) => {
        if (data.task_id) {
            // Poll for results
            checkTaskStatus(data.task_id);
        }
    });

function checkTaskStatus(taskId) {
    fetch(`http://localhost:5000/api/status/${taskId}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "completed") {
                displayQuestions(data.result.questions);
            } else if (data.status === "processing") {
                setTimeout(() => checkTaskStatus(taskId), 2000);
            }
        });
}
```

## 📋 Response Formats

### **AI Quiz Response**

```json
{
    "questions": [
        {
            "question": "Python được tạo ra bởi ai?",
            "options": ["Guido van Rossum", "Dennis Ritchie", "Bjarne Stroustrup", "James Gosling"],
            "correctAnswer": "Guido van Rossum"
        }
    ]
}
```

### **AI Q&A Response**

```json
{
    "questions": [
        {
            "question": "Python là gì?",
            "answer": "Python là một ngôn ngữ lập trình bậc cao, được thiết kế với triết lý làm cho code dễ đọc và dễ viết. Python hỗ trợ nhiều paradigm lập trình và có thư viện phong phú."
        }
    ]
}
```

### **Async Task Response**

```json
{
    "task_id": "uuid-here",
    "status": "pending",
    "message": "Document submitted for AI processing",
    "check_status_url": "/api/status/uuid-here",
    "parameters": {
        "num_questions": 20,
        "difficulty": "medium"
    }
}
```

## 🗂️ Supported File Types

| Format | Extension       | AI Support | Traditional |
| ------ | --------------- | ---------- | ----------- |
| PDF    | `.pdf`          | ✅         | ❌          |
| Word   | `.docx`         | ✅         | ✅          |
| Excel  | `.xlsx`, `.xls` | ✅         | ❌          |

## ⚙️ Configuration

### **Model Settings (config.py)**

```python
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
OPENAI_MAX_TOKENS = 4000
OPENAI_TEMPERATURE = 0.7
MAX_QUESTIONS = 50
```

### **Difficulty Levels**

-   **Easy**: Câu hỏi cơ bản, định nghĩa, thông tin trực tiếp
-   **Medium**: Phân tích, hiểu biết sâu hơn
-   **Hard**: Suy luận, kết hợp kiến thức phức tạp

## 🧪 Testing

### **Quick Test**

```bash
python test_ai.py
```

### **Load Testing**

```bash
python load_test.py
```

### **Setup Check**

```bash
python setup.py
```

## 🔧 Troubleshooting

### **Common Issues**

1. **"OpenAI API key not configured"**

    ```bash
    set OPENAI_API_KEY=your-key-here
    ```

2. **"Could not extract text from document"**

    - Check file không bị corrupt
    - Thử file khác để test

3. **"Server is busy"**

    - Đợi một chút và thử lại
    - Check server status: `/api/server-status`

4. **AI tạo câu hỏi không chất lượng**
    - Thử tăng/giảm `difficulty`
    - Đảm bảo tài liệu có nội dung phong phú
    - Thử `gpt-4` nếu có access

### **Performance Tips**

-   Sử dụng async mode cho files lớn
-   Giới hạn số câu hỏi (1-50)
-   Files PDF scan cần OCR trước
-   Excel files phức tạp có thể cần preprocessing

## 📊 Monitoring

### **Server Status**

```bash
curl http://localhost:5000/api/server-status
```

Response:

```json
{
    "active_tasks": 2,
    "max_workers": 10,
    "server_load": "2/10",
    "queue_status": "healthy",
    "ai_features": {
        "openai_configured": true,
        "supported_formats": ["PDF", "DOCX", "XLSX", "XLS"]
    }
}
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Test thoroughly
4. Submit pull request

## 📄 License

MIT License - see LICENSE file

## 🔗 Links

-   [OpenAI API Documentation](https://platform.openai.com/docs)
-   [Flask Documentation](https://flask.palletsprojects.com/)
-   [python-docx Documentation](https://python-docx.readthedocs.io/)

---

**🎯 Ready to turn any document into interactive quizzes with AI!**
