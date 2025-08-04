def generate_description(path: str) -> str:
    """
    Giả lập quá trình tạo mô tả cho một ảnh.
    Input:
        path (str): ảnh đầu vào (đường dẫn hoặc tên file)
    Output:
        str: mô tả của ảnh
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