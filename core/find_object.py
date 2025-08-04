from core.utils import getKeyword, searchByKeyword 
def find_manager(query: str) -> dict:
    """
    Purpose: tìm vật thể X được nhắc đến trong query.

    Args: query (str): Câu truy vấn của người dùng.

    Returns:
        dict: Kết quả JSON, ví dụ:
            {
              "video1": path1.mp4,
              "video2": path2.mp4,
            }

    Pipelines: Lấy keyword từ query -> chuyển đổi thành vector -> tìm kiếm trong database -> trả về các video paths -> output JSON
    """
    
    target = getKeyword(query)
    results = searchByKeyword(target)
    paths = [r for r in results]

    output = {
        f"video{i+1}": path
        for i, path in enumerate(paths)
    }

    return output