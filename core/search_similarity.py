from models import llm_model
def search_similarity(path: str, top_k: int = 5):
    """
    Giả lập quá trình tìm ảnh tương đồng với 1 ảnh đầu vào.
    Input:
        path (str): ảnh đầu vào (đường dẫn hoặc tên file)
    Output:
        JSON: { "path": ..., "similarity": ... }
    """
    vector = getVector(path)
    if vector is None:
        return {"error": "Không tìm thấy vector tương ứng với ảnh."}

    keyword = getKeywordByVector(vector)
    if keyword is None:
        return {"error": "Không tìm thấy từ khóa tương ứng với vector."}
    
    imgs = searchByKeyword(keyword)

    if imgs is None:
        return {"error": "Không tìm thấy ảnh tương tự."}
    
    similarities = []

    for img in imgs:
        img_vector = getVector(img)

        sim = calSimilarity(vector, img_vector)
        similarities.append({
            "path": img,
            "similarity": sim
        })


        top_similarity = sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:top_k]
    return top_similarity

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

def generate_multimodal_report(path: str):
    """
    Giả lập quá trình tạo báo cáo đa phương thức cho một ảnh.
    Input:
        path (str): ảnh đầu vào (đường dẫn hoặc tên file)
    Output:
        str: báo cáo đa phương thức
    """
    if not os.path.exists(path):
        return " Video is not exist"
    
    keyframes = extract_keyframes(path) # return List[Dict] chứa 'frame_path', 'timestamp'

    descriptions = []
    for frame in keyframes:
        vector = getVector(frame['frame_path'])
        info = search_vector(vector)
        caption = call_llm(f"Mô tả nội dung ảnh tại thời điểm {frame['timestamp']}: {info}")
        descriptions.append({
            "frame_path": frame['frame_path'],
            "timestamp": frame['timestamp'],
            "description": caption
        })

    # Trích đoạn hội thoại từ audio trong video
    transcript = transcribe_audio(path)
    summary = call_llm("Tóm tắt nội dung chính của video dựa trên đoạn transcript sau:\n{transcript}")

    #Tạo báo cáo tổng hợp
    report = {
        "video_path": path,
        "summary": summary,
        "keyframes": descriptions,
    }

    return report