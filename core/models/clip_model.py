# pip install git+https://github.com/openai/CLIP.git
import torch
import clip

class CLIPModel:
    def __init__(self, model, preprocess):
        self.model = model
        self.preprocess = preprocess
    
    @classmethod
    def load(cls, model, preprocess):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)
        model.share_memory() 
        return cls(model, preprocess)

    def encode_text(self, text):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        text_tokens = clip.tokenize([text]).to(device)
        with torch.no_grad():
            text_vector = self.model.encode_text(text_tokens).cpu().numpy().flatten().tolist()
        return text_vector
