# Configuration file for AI features
import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '123')

# Alternative: You can set your API key directly here (NOT RECOMMENDED for production)
# OPENAI_API_KEY = "your-openai-api-key-here"

# Model Configuration
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4" if you have access
OPENAI_MAX_TOKENS = 4000
OPENAI_TEMPERATURE = 0.7

# Processing Limits
MAX_CONTENT_LENGTH = 8000  # Characters to send to AI (to avoid token limits)
DEFAULT_QUESTIONS = 20
MAX_QUESTIONS = 50

# File Processing Settings
SUPPORTED_EXTENSIONS = {
    'ai': ['.pdf', '.docx', '.xlsx', '.xls'],
    'traditional': ['.docx']
}

# AI Prompts Templates
QUIZ_PROMPT_TEMPLATE = """
Dựa trên nội dung tài liệu sau, hãy tạo {num_questions} câu hỏi trắc nghiệm (multiple choice) với độ khó {difficulty}.

Yêu cầu:
- Mỗi câu hỏi có 4 đáp án (A, B, C, D)
- Chỉ có 1 đáp án đúng
- Câu hỏi phải dựa trên nội dung tài liệu
- Câu hỏi phải có tính thực tiễn và hữu ích
- Trả về định dạng JSON chính xác như mẫu bên dưới
- Sử dụng tiếng Việt
- Đảm bảo câu hỏi có độ khó phù hợp: {difficulty_description}

Định dạng JSON mong muốn:
[{{
    {{
      "question": "Câu hỏi ở đây?",
      "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
      "correctAnswer": "Đáp án đúng"
    }}
}}]

Nội dung tài liệu:
{content}

Hãy tạo {num_questions} câu hỏi trắc nghiệm chất lượng cao từ nội dung trên:
"""

QA_PROMPT_TEMPLATE = """
Dựa trên nội dung tài liệu sau, hãy tạo {num_questions} cặp câu hỏi và đáp án.

Yêu cầu:
- Câu hỏi phải rõ ràng, cụ thể và dựa trên nội dung tài liệu
- Đáp án phải chính xác, chi tiết và đầy đủ thông tin
- Câu hỏi nên bao quát các phần quan trọng của tài liệu
- Trả về định dạng JSON chính xác
- Sử dụng tiếng Việt

Định dạng JSON:
[{{
    {{
      "question": "Câu hỏi ở đây?",
      "answer": "Đáp án chi tiết và đầy đủ ở đây"
    }}
}}]

Nội dung tài liệu:
{content}

Hãy tạo {num_questions} cặp câu hỏi - đáp án chất lượng cao:
"""

DIFFICULTY_DESCRIPTIONS = {
    "easy": "Câu hỏi dễ, tập trung vào kiến thức cơ bản, định nghĩa, và thông tin trực tiếp từ tài liệu",
    "medium": "Câu hỏi trung bình, yêu cầu hiểu biết và phân tích thông tin từ tài liệu",
    "hard": "Câu hỏi khó, yêu cầu suy luận, phân tích sâu và kết hợp kiến thức từ nhiều phần của tài liệu"
}

def get_api_key():
    """Get OpenAI API key from environment or config"""
    return OPENAI_API_KEY

def is_ai_configured():
    """Check if AI is properly configured"""
    return bool(get_api_key())

def get_difficulty_description(difficulty):
    """Get description for difficulty level"""
    return DIFFICULTY_DESCRIPTIONS.get(difficulty, DIFFICULTY_DESCRIPTIONS["medium"])
