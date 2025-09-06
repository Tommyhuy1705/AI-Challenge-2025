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


from collections import defaultdict
import itertools
import os

def find_flow(state: list[str], limit: int = 50, top_k: int = 100, per_video_keep: int = 10):
    """

    """

    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    state_vectors = [clip_model.encode_text(s) for s in state]

    # 2) Kết nối
    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)

    # ---------- PHẦN A: XÂY "response" THEO ĐÚNG FORMAT FLASH, GOM THEO VIDEO ----------
    response_result = []
    # Cho từng state, lấy top frames, enrich videoId + frameIndex rồi group-by video
    for s, vec in zip(state, state_vectors):
        raw = get_all_frames_by_vector(client, vec, limit=limit)

        # group theo videoId
        groups = defaultdict(list)  # vid -> list of (frameIndex, {"keyframeId","keyframePath"})
        for obj in raw.objects:
            props = obj.properties
            kf_id  = props.get("keyframeId")
            kf_path= props.get("keyframePath")

            info = get_info_by_frameId(client, kf_id)
            if not info.objects:
                continue
            ip = info.objects[0].properties
            vid = ip.get("videoId")
            fidx = ip.get("frameIndex")
            if not vid or fidx is None:
                continue

            groups[vid].append((fidx, {"keyframeId": kf_id, "keyframePath": kf_path}))

        # với mỗi video, sort theo frameIndex và giữ tối đa per_video_keep frame
        for vid, items in groups.items():
            items.sort(key=lambda x: x[0])  # theo frameIndex tăng dần
            frames_for_state = [d for _, d in items[:per_video_keep]]

            if frames_for_state:
                response_result.append({
                    "frames": frames_for_state,
                    "state": s
                })

    # ---------- PHẦN B: XÂY "combo" THEO CHUỖI FLOW CÙNG VIDEO ----------
    combos = []
    seen_combo = set()

    # Anchor từ state[0]
    anchor_frames = get_all_frames_by_vector(client, state_vectors[0], limit=limit)

    for obj in anchor_frames.objects:
        props0 = obj.properties
        kf0_id = props0.get("keyframeId")
        kf0_path = props0.get("keyframePath")

        info0 = get_info_by_frameId(client, kf0_id)
        if not info0.objects:
            continue
        ip0 = info0.objects[0].properties
        vid = ip0.get("videoId")
        idx0 = ip0.get("frameIndex")
        if not vid or idx0 is None:
            continue

        flow_ids = [kf0_id]
        last_index = idx0
        ok = True
        idx_list = [idx0]

        # Duyệt các state tiếp theo trong CÙNG video
        for vec in state_vectors[1:]:
            # chỉ lấy frame sau last_index trong video đó
            cands = search_in_video(client, video_id=vid, vector=vec, min_index=last_index + 1, limit=limit)
            if not cands:
                ok = False
                break

            # chọn best đầu tiên
            best = cands[0]
            kf_id = best["keyframeId"]

            info = get_info_by_frameId(client, kf_id)
            if not info.objects:
                ok = False
                break
            ip = info.objects[0].properties
            fidx = ip.get("frameIndex")
            if fidx is None:
                ok = False
                break

            flow_ids.append(kf_id)
            idx_list.append(fidx)
            last_index = fidx

        if not ok:
            continue

        # Tính score (độ liền mạch theo index), nhỏ hơn = tốt hơn
        diffs = [idx_list[i+1] - idx_list[i] for i in range(len(idx_list)-1)]
        if any(d <= 0 for d in diffs):  # đảm bảo tăng dần
            continue
        score = sum(diffs)

        key = (vid, tuple(flow_ids))
        if key in seen_combo:
            continue
        seen_combo.add(key)
        combos.append((score, vid, flow_ids))

    client.close()

    # sort theo score tăng dần (càng liền mạch càng tốt), cắt top_k
    combos.sort(key=lambda x: x[0])
    combos = combos[:top_k]

    combo_strs = []
    for _, vid, flow_ids in combos:
        indices = []
        for kf_id in flow_ids:
            info = get_info_by_frameId(client, kf_id)
            if info.objects:
                idx = info.objects[0].properties.get("frameIndex")
                if idx is not None:
                    indices.append(str(idx))
        combo_strs.append(f"{vid}, {','.join(indices)}")

    return {
        "info": response_result,
        "combo": combo_strs,
        "success": True
    }


