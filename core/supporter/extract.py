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

import torch
from typing import List
from keybert import KeyBERT

class KeywordExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.load()
        
    def load(self):
        if self.model is not None:
            return  
        try:
            self.model = KeyBERT()
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")
        
    def release(self):
        self.model = None
        torch.cuda.empty_cache()

    def extract_keywords(self, text: str) -> List[str]:
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=5
        )
        return [kw for kw, _ in keywords]