from core.models.clip_model import CLIPModel

class ModelRegistry:
   clip_model: CLIPModel = None

def load_clip_model():
   ModelRegistry.clip_model = CLIPModel.load()