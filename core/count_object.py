from core.utils import getKeyword, detectObjectImage, detectObjectVideo, countObjects
def count_manager(query: str, srces: list[str]) -> dict:
    """
    Purpose: đếm vật thể X được nhắc đến trong query từ lựa chọn của các nguồn có sẵn.

    Circumtance: Sau khi tìm kiếm vật thể hoặc ở giao diện ban đầu, user nhập query và chọn ảnh/video trong giao diện để đếm 
    một vật thể nào đó.

    Args: 
        query (str): Câu truy vấn của người dùng.
        srces (list[str]): Đường dẫn đến ảnh hoặc video nguồn.

    Returns:
        dict: Kết quả JSON, ví dụ:
            {
              object_name: target,
              quantity: count
            }

    Pipelines: Lấy keyword từ query -> track vật thể tùy định dạng -> đếm số lượng vật thể trong tracker -> trả về kết quả JSON.
    """
    
    target = getKeyword(query)
    tracker = list()
    
    for src in srces:
        if src.endswith('.jpg', '.jpeg', '.png'):
            tracker = detectObjectImage(src, target)
        elif src.endswith('.mp4', 'avi', '.mov'):
            tracker = detectObjectVideo(src, target)
        else:
            raise ValueError("Không tồn tại định dạng ảnh hoặc video này!")

    count = countObjects(tracker, target)

    return {
        "object_name": target,
        "quantity": count
    }