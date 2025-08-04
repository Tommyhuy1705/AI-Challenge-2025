from models import llm_model
from core.utils import getVector, search_vector, call_llm, transcribe_audio, extract_keyframes
import os
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
