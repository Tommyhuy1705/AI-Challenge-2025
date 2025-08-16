# def extract_keyframes(path: str) -> list[str]:
#     return ["frame1.jpg", "frame2.jpg", "frame3.jpg"]  => curd

# def detect_object_image(path: str, target: str) -> list[dict]: => dùng model=> đếm
#     return [{"bbox": [10, 20, 30, 40], "label": target}]  # Ví dụ phát hiện vật thể

# video -> tiền xử lí -> đọc từng frmae dêtct (detect_object_imag) -> kết quả
# def detect_object_video(path: str, target: str) -> list[dict]:
#     return [{"bbox": [10, 20, 30, 40], "label": target}]  

def transcribe_audio(path: str, start: float, end: float) -> str:
    return "Một con chó chạy trong công viên. Sau đó, gặp một đứa bé đang chơi."

# def extract_clip_around_bbox(keyframes: list[str], frame_index: int, bbox: dict) -> list[str]: => task mở rộng 
#     # Trả về một clip nhỏ quanh bbox
#     return keyframes[max(0, frame_index - 5):min(len(keyframes), frame_index + 5)]  # Ví dụ trích 10 keyframes quanh bbox