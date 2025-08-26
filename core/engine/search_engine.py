from core.supporter.helper import calculate_similarity
# from core.db_controller.crud import convert_to_vector, query_database

def search(keyword: str) -> dict:
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
    
    _, paths = get_all_frames_by_keyword(keyword)
    
    output = {
        f"video{i+1}": path
        for i, path in enumerate(paths)
    } # sửa lại định dạng output

    return output
