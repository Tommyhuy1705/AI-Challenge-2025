from dotenv import load_dotenv
import os
from core.boostrap import ModelRegistry
from core.db_controller.crud import get_all_frames_by_vector
from core.db_controller.connect import connect_db

def find_flow(state: list[str], limit: int = 5):
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

    #Connect
    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)

    results = []

    # Search
    for i, (s, vec) in enumerate(zip(state, state_vectors)):
        frames = get_all_frames_by_vector(client=client, vector=vec, limit=limit)

        frame_list = []
        for obj in frames.objects:
            props = obj.properties
            frame_list.append({
                "keyframeId": props.get("keyframeId"),
                "keyframePath": props.get("keyframePath")
            })

        results.append({
            "state": s,
            "frames": frame_list
        })

    return results
