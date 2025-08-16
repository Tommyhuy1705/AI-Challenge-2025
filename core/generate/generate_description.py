from core.supporter.helper import getVector, search_vector, call_llm
import os
def generate_description(path: str) -> str:
    """
    Purpose: Tạo mô tả ngắn gọn cho nội dung của một ảnh tĩnh (image captioning).

    Circumtance: Khi người dùng cung cấp một ảnh và muốn biết ảnh đó thể hiện điều gì.

    Args:
        path (str): Đường dẫn tới ảnh đầu vào.

    Returns:
        str: Một mô tả ngắn gọn của nội dung ảnh.

    Pipelines: 
        Trích xuất vector đặc trưng của ảnh -> Tìm kiếm các thông tin liên quan trong database ->
        Đưa thông tin vào LLM để tạo mô tả tự nhiên.
    """
    
    if not os.path.exists(path):
        return "Ảnh không tồn tại"

    vector = getVector(path)
    if vector is None:
        return "Không thể tạo vector từ ảnh"

    info = search_vector(vector)
    if not info:
        return "Không tìm thấy thông tin liên quan để mô tả"

    # Gọi LLM sinh caption
    prompt = f"Mô tả nội dung ảnh dựa trên các thông tin: {info}"
    description = call_llm(prompt)

    return description