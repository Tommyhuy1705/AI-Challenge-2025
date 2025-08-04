<<<<<<< HEAD
=======
from core.utils import getKeyword, searchByKeyword 
>>>>>>> 4382bf569872f670e3ff38e9f07cbb3f7a8b66c9
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

<<<<<<< HEAD
    return output

=======
    return output
>>>>>>> 4382bf569872f670e3ff38e9f07cbb3f7a8b66c9
