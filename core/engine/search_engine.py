import os
from core.boostrap import ModelRegistry
from core.db_controller.crud import get_all_frames_by_vector
from core.db_controller.connect import connect_db

def _extract_id_path(obj):
    """Lấy keyframeId, keyframePath từ object Weaviate."""
    props = getattr(obj, "properties", {}) or {}
    return props.get("keyframeId"), props.get("keyframePath"), props.get("frameIndex")

def _normalize_score(meta: dict, fallback_rank: int) -> float:
    """
    Chuẩn hoá điểm về [0,1].
    Nếu không có similarity thì fallback = 1/(1+rank).
    """
    if not isinstance(meta, dict):
        return 1.0 / (1.0 + fallback_rank)

    if "certainty" in meta and isinstance(meta["certainty"], (int, float)):
        c = float(meta["certainty"])
        return max(0.0, min(1.0, c))

    if "distance" in meta and isinstance(meta["distance"], (int, float)):
        d = max(0.0, float(meta["distance"]))
        return 1.0 / (1.0 + d)

    if "score" in meta and isinstance(meta["score"], (int, float)):
        s = float(meta["score"])
        # giả sử cosine [-1,1] → đưa về [0,1]
        return max(0.0, min(1.0, (s + 1.0) / 2.0))

    return 1.0 / (1.0 + fallback_rank)

def search(keyword: list[str], limit: int = 5, alpha_main: float = 0.25) -> dict:
    """
    Search theo keyword chính (keyword[0]) → rerank bằng các keyword phụ.
    - Điểm được pha trộn: rerank_score = α * main_score + (1-α) * mean(secondary_scores)
    """
    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    if not keyword:
        raise ValueError("keyword must not be empty")

    keyw_vectors = [clip_model.encode_text(k) for k in keyword]

    # Connect
    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)

    try:
        init_limit = max(limit * 20, 50)

        # 1) Query MAIN
        main_keyword, main_vec = keyword[0], keyw_vectors[0]
        main_res = get_all_frames_by_vector(client, vector=main_vec, limit=init_limit)

        main_frames = []
        main_score_map = {}
        for rank, obj in enumerate(getattr(main_res, "objects", []) or []):
            fid, fpath, findex = _extract_id_path(obj)
            if not fid:
                continue
            score = _normalize_score(
                getattr(obj, "metadata", None) or getattr(obj, "additional", None) or {},
                rank
            )
            main_score_map[fid] = score
            main_frames.append({
                "keyframeId": fid,
                "keyframeIndex": findex,
                "keyframePath": fpath,
                "main_rank": rank
            })

        if not main_frames:
            return {
                "main_keyword": main_keyword,
                "rerank_keywords": keyword[1:],
                "frames": []
            }

        # 2) Query phụ và tạo score_map
        secondary_score_maps = []
        for sub_idx, sub_vec in enumerate(keyw_vectors[1:]):
            sub_res = get_all_frames_by_vector(client, vector=sub_vec, limit=init_limit)
            score_map = {}
            objs = getattr(sub_res, "objects", []) or []
            for idx, obj in enumerate(objs):
                fid, _ = _extract_id_path(obj)
                if not fid:
                    continue
                score = _normalize_score(
                    getattr(obj, "metadata", None) or getattr(obj, "additional", None) or {},
                    idx
                )
                score_map[fid] = score
            secondary_score_maps.append(score_map)

        # 3) Pha trộn điểm: main_score (α) + mean phụ (1-α)
        for f in main_frames:
            fid = f["keyframeId"]
            main_s = main_score_map.get(fid, 0.0)
            if secondary_score_maps:
                sec_scores = [smap.get(fid, 0.0) for smap in secondary_score_maps]
                sec_mean = sum(sec_scores) / len(secondary_score_maps)
            else:
                sec_mean = 0.0
            f["rerank_score"] = alpha_main * main_s + (1 - alpha_main) * sec_mean

        # 4) Sort & cắt top-k
        main_frames.sort(key=lambda x: (-x["rerank_score"], x["main_rank"]))
        top_frames = [
            {"keyframeId": f["keyframeId"], "keyframePath": f["keyframePath"]}
            for f in main_frames[:limit]
        ]

        return {
            "main_keyword": main_keyword,
            "rerank_keywords": keyword[1:],
            "frames": top_frames
        }

    finally:
        client.close()
