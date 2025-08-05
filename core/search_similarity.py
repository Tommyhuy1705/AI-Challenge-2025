from models import llm_model
from core.utils import getVector, search_vector, call_llm, transcribe_audio
import os
def search_similarity(path: str, top_k: int):
    """
    Purpose: Tìm kiếm những ảnh hoặc nội dung có độ tương đồng cao với ảnh đầu vào.

    Circumtance: Khi người dùng đưa vào một ảnh và muốn biết các ảnh/frame/đoạn hội thoại tương tự.

    Args:
        path (str): Đường dẫn tới ảnh đầu vào cần so sánh.

    Returns:
        list[dict]: Danh sách top N ảnh tương đồng nhất, ví dụ:
            [
                {"path": "img_01.jpg", "similarity": 0.91},
                {"path": "img_03.jpg", "similarity": 0.87},
                ...
            ]

    Pipelines:
        Trích xuất vector đặc trưng từ ảnh đầu vào -> Tìm kiếm ảnh trong cơ sở dữ liệu theo vector gần nhất ->
        Tính toán độ tương đồng -> Trả về danh sách top N ảnh gần nhất.
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
