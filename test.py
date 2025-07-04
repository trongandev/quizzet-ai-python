import docx
import re
import json

def is_correct_answer(run):
    """Kiểm tra run có phải đáp án đúng không (bold, highlight, hoặc màu chữ khác)"""
    return (run.bold is True or 
            run.font.highlight_color is not None or
            (run.font.color and run.font.color.rgb is not None))

def parse_quiz_from_docx(docx_path):
    """Parse file DOCX thành format quiz JSON"""
    doc = docx.Document(docx_path)
    quiz_data = []
    current_question = None
    
    # Patterns để nhận diện câu hỏi và đáp án
    question_patterns = [
        r'^(Câu\s*\d+[:\.]?)\s*(.*)',  # Câu 1., Câu 2:
        r'^(\d+[:\.])\s*(.*)',          # 1., 2:
        r'^(.*)\?$'                     # Kết thúc bằng ?
    ]
    
    answer_pattern = r'^([a-dA-D][\.\)])\s*(.*)'  # a., B), c.
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Tách paragraph thành nhiều dòng nếu có xuống dòng
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Kiểm tra xem có phải câu hỏi không
            is_question = any(re.match(pattern, line, re.IGNORECASE) for pattern in question_patterns)
            
            if is_question:
                # Lưu câu hỏi trước đó nếu có
                if current_question:
                    quiz_data.append(current_question)
                
                # Tạo câu hỏi mới
                current_question = {
                    "question": line,
                    "answers": [],
                    "correct": -1  # -1 nghĩa là chưa có đáp án đúng
                }
            
            # Kiểm tra xem có phải đáp án không
            elif current_question:
                match = re.match(answer_pattern, line, re.DOTALL)
                if match:
                    answer_text = match.group(2).strip()
                    current_question["answers"].append(line)
                    
                    # Kiểm tra format của đáp án để xem có phải đáp án đúng không
                    for run in para.runs:
                        if answer_text in run.text and is_correct_answer(run):
                            # Lưu index của đáp án đúng (bắt đầu từ 0)
                            current_question["correct"] = len(current_question["answers"]) - 1
                            break
    
    # Thêm câu hỏi cuối cùng
    if current_question:
        quiz_data.append(current_question)
    
    # Sắp xếp câu hỏi: câu hỏi có đáp án và correct lên trước, câu hỏi thiếu thông tin xuống cuối
    valid_questions = []
    invalid_questions = []
    
    for question in quiz_data:
        # Kiểm tra câu hỏi có đầy đủ thông tin không (có answers và correct >= 0)
        if question["answers"] and question["correct"] >= 0:
            valid_questions.append(question)
        else:
            invalid_questions.append(question)
    
    # Format và làm sạch các câu hỏi hợp lệ
    formatted_valid_questions = format_valid_questions(valid_questions)
    
    # Kết hợp lại: câu hỏi hợp lệ đã format trước, câu hỏi thiếu thông tin sau
    sorted_quiz_data = formatted_valid_questions + invalid_questions
    
    return sorted_quiz_data

def clean_question_text(question_text):
    """Xóa các từ thừa trong câu hỏi như 'Câu n:', 'câu n:', 'số:'"""
    # Loại bỏ các pattern thường gặp ở đầu câu hỏi
    patterns_to_remove = [
        r'^Câu\s*\d+[:\.]?\s*',   # Câu 1:, Câu 2., Câu 3
        r'^câu\s*\d+[:\.]?\s*',   # câu 1:, câu 2., câu 3  
        r'^\d+[:\.]?\s*',         # 1:, 2., 3
    ]
    
    cleaned_text = question_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE).strip()
    
    return cleaned_text

def clean_answer_text(answer_text):
    """Xóa các ký tự thừa trong đáp án như A., B., a), b), 1., 2."""
    # Loại bỏ các pattern thường gặp ở đầu đáp án
    patterns_to_remove = [
        r'^[a-dA-D][\.\)]\s*',    # A., B., a), b)
        r'^[1-4][\.\)]\s*',       # 1., 2., 1), 2)
    ]
    
    cleaned_text = answer_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text).strip()
    
    return cleaned_text

def format_valid_questions(questions):
    """Format và làm sạch các câu hỏi hợp lệ"""
    formatted_questions = []
    
    for question in questions:
        formatted_question = {
            "question": clean_question_text(question["question"]),
            "answers": [clean_answer_text(answer) for answer in question["answers"]],
            "correct": question["correct"]
        }
        formatted_questions.append(formatted_question)
    
    return formatted_questions

# Sử dụng
if __name__ == "__main__":
    file_path = 'Ôn tập Vật liệu cơ khí (1).docx'
    try:
        quiz_output = parse_quiz_from_docx(file_path)
        
        # In ra JSON
        json_output = json.dumps(quiz_output, indent=2, ensure_ascii=False)
        print(json_output)
        
        # Lưu file
        with open('quiz_output.json', 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"\nĐã lưu vào 'quiz_output.json'")
        
    except FileNotFoundError:
        print(f"Không tìm thấy file '{file_path}'")
    except Exception as e:
        print(f"Lỗi: {e}")