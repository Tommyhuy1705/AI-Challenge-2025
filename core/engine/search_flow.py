from dotenv import load_dotenv
import os
from collections import defaultdict
from core.boostrap import ModelRegistry
from core.db_controller.crud import get_all_frames_by_vector,get_info_by_frameId
from core.db_controller.connect import connect_db
from weaviate.classes.query import Filter

def search_in_video(client, video_id: str, vector, min_index: int = 0, limit: int = 10):
    frame_col = client.collections.get("Keyframe")
    results = frame_col.query.near_vector(
        near_vector=vector,
        limit=limit,
        filters=(
            Filter.by_property("videoId").equal(video_id) &
            Filter.by_property("frameIndex").greater_than(min_index)
        ),
        return_properties=["keyframeId", "keyframePath"]
    )

    frames = []
    for obj in results.objects:
        props = obj.properties
        frames.append({
            "keyframeId": props.get("keyframeId"),
            "keyframePath": props.get("keyframePath"),
        })
    return frames


def find_flow(state: list[str], limit: int = 150, top_k: int = 100):
    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    # encode vector cho từng state
    state_vectors = [clip_model.encode_text(s) for s in state]

    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)

    # Step 1: search anchor cho state[0]
    anchor_frames = get_all_frames_by_vector(client, state_vectors[0], limit=limit)

    frames_result = []   # list frame flow hợp lệ
    combos = []          # để build combo như trước

    for obj in anchor_frames.objects:
        props0 = obj.properties
        frame_id = props0.get("keyframeId")
        frame_path = props0.get("keyframePath")

        # enrich từ frameId
        info0 = get_info_by_frameId(client, frame_id)
        if not info0.objects:
            continue

        info_props0 = info0.objects[0].properties
        vid = info_props0.get("videoId")
        idx0 = info_props0.get("frameIndex")
        if not vid or idx0 is None:
            continue

        current_frames = [{
            "keyframeId": frame_id,
            "keyframePath": frame_path,
            "videoId": vid,
            "frameIndex": idx0,
        }]

        last_index = idx0
        valid_flow = True

        # Step 2: sequential cho state tiếp theo
        for s, vec in zip(state[1:], state_vectors[1:]):
            candidates = search_in_video(client, video_id=vid, vector=vec, min_index=last_index + 1, limit=limit)
            if not candidates:
                valid_flow = False
                break

            best = candidates[0]
            frame_id = best["keyframeId"]
            frame_path = best["keyframePath"]

            info = get_info_by_frameId(client, frame_id)
            if not info.objects:
                valid_flow = False
                break

            info_props = info.objects[0].properties
            current_frames.append({
                "keyframeId": frame_id,
                "keyframePath": frame_path,
                "videoId": info_props.get("videoId"),
                "frameIndex": info_props.get("frameIndex"),
            })
            last_index = info_props.get("frameIndex")

        if valid_flow:
            frame_indices = [f["frameIndex"] for f in current_frames]
            diffs = [frame_indices[i+1] - frame_indices[i] for i in range(len(frame_indices)-1)]
            score = sum(diffs)

            # lưu cho combo
            combos.append((vid, frame_indices, score))

            # lưu cho frames
            frames_result.append(current_frames)

    client.close()

    # sort combo
    combos = sorted(combos, key=lambda x: x[2])[:top_k]
    combo_strs = [f"{vid}, {','.join(map(str, idxs))}" for vid, idxs, _ in combos]

    return {
        "combo": combo_strs,
        "frames": frames_result
        
    }

