def count_objects(tracker: list[dict], target: str) -> int: #thêm class chứa model 
    return len([obj for obj in tracker if obj['label'] == target])  # Ví dụ: con mèo = 8

def classify_action(clip: list[str]) -> str:
    # Gọi mô hình phân loại hành động
    return "đang chạy"

import torch
import torchvision
from PIL import Image
from torchvision import transforms


class detectObjectImage:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.load()
        
    def load(self):
        if self.model is not None:
            return  
        try:
            self.model = 
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")
        
    def release(self):
        self.model = None
        torch.cuda.empty_cache()    
    