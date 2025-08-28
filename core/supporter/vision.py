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
            self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
            self.model.to(self.device).eval()
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")
        
    def release(self):
        self.model = None
        torch.cuda.empty_cache()    
    def detect(self, image_path: str, threshold: float = 0.5):
        img = Image.open(image_path).convert("RGB")

        transform = transforms.Compose([transforms.ToTensor()])
        img_tensor = transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(img_tensor)

        results = []
        for label, score, box in zip(outputs[0]['labels'], outputs[0]['scores'], outputs[0]['boxes']):
            if score >= threshold:
                results.append({
                    "label": label.item(),
                    "score": score.item(),
                    "box": box.tolist()
                })
        return results
