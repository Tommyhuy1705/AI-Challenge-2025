def count_objects(tracker: list[dict], target: str) -> int: #thêm class chứa model 
    return len([obj for obj in tracker if obj['label'] == target])  # Ví dụ: con mèo = 8

def classify_action(clip: list[str]) -> str:
    # Gọi mô hình phân loại hành động
    return "đang chạy"