import os
from core.boostrap import ModelRegistry
from core.db_controller.crud import get_all_frames_by_vector
from core.db_controller.connect import connect_db

def search(keyword: list[str], limit: int = 5) -> dict:
    """
    Purpose: tìm vật thể X được nhắc đến trong query.

    Args: query (str): Câu truy vấn của người dùng.

    Returns:
        dict: Kết quả JSON, ví dụ:
            {
              "video1": path1.mp4,
              "video2": path2.mp4,
            }

    Pipelines: Lấy keyword từ query -> lấy video dựa theo keyword trong database -> trả về các video paths -> output JSON
    """
    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    keyw_vectors = [clip_model.encode_text(k) for k in keyword]

    #Connect
    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)
    
    results = []
    temp_results = None
    init_limit = limit * 20

    # Search: Có filter từng phần => Không dùng code bên dưới nữa
    for i, (k, vec) in enumerate(zip(keyword, keyw_vectors)):
        frames = get_all_frames_by_vector(client, vector=vec, limit=init_limit)

        frame_list = []
        for obj in frames.objects:
            props = obj.properties
            frame_list.append({
                "keyframeId": props.get("keyframeId"),
                "keyframePath": props.get("keyframePath")
            })

        if temp_results is None:
            temp_results = frame_list
        else:
            # Lấy giao với kết quả trước => Nếu không có code này thì kết quả sẽ là của từ khóa cuối cùng
            prev_ids = {f["keyframeId"] for f in results}
            temp_results = [f for f in frame_list if f["keyframeId"] in prev_ids]

        # Giảm dần kết quả (ví dụ giữ lại 80%)
        step_limit = max(limit, int(len(temp_results) * 0.8))
        temp_results = temp_results[:step_limit]

        results.append({
            f"key{i}": k,
            "frames": temp_results
        })

        # Nếu số lượng đã ≤ final_limit thì dừng sớm
        if len(temp_results) <= limit:
            break

    return results
