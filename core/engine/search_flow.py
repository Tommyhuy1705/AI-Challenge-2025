from core.boostrap import ModelRegistry
from core.db_controller.crud

def find_flow(state: list[str]):
    """
    It searches and identifies the exact frames corresponding to a sequence of key states within an action. 
    The function maps each state to its matching frame in the correct temporal order. 
    (e.g., steps in a dance, or phases in a high jump).
    The function maps each state to its matching frame in the correct temporal order.
    """
    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    state_vectors = [clip_model.encode_text(s) for s in state]

    #Search
    for i, vec in enumerate(state_vectors):
        # Find the most similar frame in the video for each state vector
        # frames = 
        # fottmat dict id,path
        pass
