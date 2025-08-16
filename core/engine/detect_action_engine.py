from core.supporter.helper import getKeyword, extractKeyframes, detectObjectImage, extractClipAroundBbox, classifyAction
def action_detect(query: str, srces: list[str]) -> dict:
    """
    Purpose: tìm hành động của vật thể X.

    Circumtance: user nhập query liên quan, hệ thống tự động chọn tất cả ảnh/video trong giao diện, truyền vào
    hàm để tìm hành động của vật thể đó.

    Args: 
        query (str): Câu truy vấn của người dùng.
        srces (list[str]): Đường dẫn đến ảnh hoặc video nguồn.

    Returns:
        dict: Kết quả JSON, ví dụ:
            {
                "frame": số-thứ-tự-của-frame,
                "bbox": [x1, y1, x2, y2],
                "label": tên-vật-thể,
                "action": tên-hành-động
            }

    Pipelines: Lấy keyword từ query -> Lấy keyframes từ video -> Phát hiện vật thể -> Trích clip quanh vật thể (~10s) -> Dự đoán hành động.
    """
    
    object_label = getKeyword(query) # trả về vật thể cần tìm 
    action_label = getKeyword(query) # trả về hành động cần tìm
    all_results = {}

    for src in srces:
        keyframes = extractKeyframes(src) # trả về toàn là keyframes (định dạng ảnh)
        results = []

        for i, frame in enumerate(keyframes):
            # Phát hiện vật thể
            bboxes = detectObjectImage(frame, object_label)

            for bbox in bboxes:
                # Trích clip nhỏ quanh bbox
                clip = extractClipAroundBbox(keyframes, i, bbox)

                # Dự đoán hành động của đối tượng đó
                action = classifyAction(clip)

                if action == action_label:
                    results.append({
                        "frame": i,
                        "bbox": bbox,
                        "label": object_label,
                        "action": action
                    })

        all_results[src] = results

    return all_results