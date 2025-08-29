import os
import math
from core.boostrap import ModelRegistry
from core.db_controller.crud import get_all_frames_by_vector
from core.db_controller.connect import connect_db

def _extract_id_path(obj):
    """Lấy keyframeId, keyframePath từ object Weaviate."""
    props = getattr(obj, "properties", {}) or {}
    return props.get("keyframeId"), props.get("keyframePath")

def _score_from_obj(obj):
    """
    Cố gắng lấy điểm tương tự nếu có (distance/certainty/score).
    Trả về None nếu không có.
    """
    # Nhiều client để trong obj.metadata / obj.additional
    meta = getattr(obj, "metadata", None) or getattr(obj, "additional", None) or {}
    # Ưu tiên 'certainty' (cao hơn là tốt) rồi tới -distance (thấp hơn là tốt)
    if isinstance(meta, dict):
        if "certainty" in meta and isinstance(meta["certainty"], (int, float)):
            return float(meta["certainty"])  # lớn hơn tốt hơn
        if "distance" in meta and isinstance(meta["distance"], (int, float)):
            # distance nhỏ hơn tốt hơn → đảo dấu để lớn hơn là tốt hơn
            return -float(meta["distance"])
        if "score" in meta and isinstance(meta["score"], (int, float)):
            return float(meta["score"])
    return None

def search(keyword: list[str], limit: int = 5) -> dict:
    """
    Approach #3: Search theo keyword chính (keyword[0]) → rerank bằng các keyword phụ.
    Không intersect cứng, tránh rỗng vì động từ/trạng thái.
    """
    clip_model = ModelRegistry.clip_model
    if not clip_model:
        raise ValueError("CLIP model is not loaded")

    if not keyword:
        raise ValueError("keyword must not be empty")

    # Encode text → đa số implementation OK với string/list string
    keyw_vectors = [clip_model.encode_text(k) for k in keyword]

    # Connect
    url = os.getenv("WEAVIATE_URL")
    key = os.getenv("WEAVIATE_API_KEY")
    client = connect_db(url, key)

    try:
        init_limit = max(limit * 20, 50)  # rộng hơn để rerank có ý nghĩa

        # 1) Query MAIN
        main_keyword, main_vec = keyword[0], keyw_vectors[0]
        main_res = get_all_frames_by_vector(client, vector=main_vec, limit=init_limit)

        main_frames = []
        for rank, obj in enumerate(getattr(main_res, "objects", []) or []):
            fid, fpath = _extract_id_path(obj)
            if not fid:
                continue
            main_frames.append({
                "keyframeId": fid,
                "keyframePath": fpath,
                "main_rank": rank  # tie-break sau khi rerank
            })

        if not main_frames:
            # Không có gì cho keyword chính thì trả rỗng sớm
            return {
                "main_keyword": main_keyword,
                "rerank_keywords": keyword[1:],
                "frames": []
            }

        # 2) Chuẩn bị map để rerank từ các keyword phụ:
        #    Với mỗi keyword phụ: query riêng → tạo map {keyframeId: score}
        secondary_keywords = keyword[1:]
        secondary_vecs = keyw_vectors[1:]

        # Danh sách dict score_map theo từng keyword phụ
        secondary_score_maps = []
        for sub_vec in secondary_vecs:
            sub_res = get_all_frames_by_vector(client, vector=sub_vec, limit=init_limit)
            score_map = {}
            objs = getattr(sub_res, "objects", []) or []
            for idx, obj in enumerate(objs):
                fid, _ = _extract_id_path(obj)
                if not fid:
                    continue
                s = _score_from_obj(obj)
                if s is None:
                    # fallback nếu DB không trả similarity: dùng inverse-rank
                    s = 1.0 / (1.0 + idx)
                score_map[fid] = float(s)
            secondary_score_maps.append(score_map)

        # 3) Tính điểm rerank cho từng frame trong main_frames
        #    - aggregate = trung bình (hoặc tổng) điểm các map phụ
        #    - nếu frame không xuất hiện trong một sub-map → điểm 0 cho keyword đó
        for f in main_frames:
            fid = f["keyframeId"]
            if secondary_score_maps:
                scores = []
                for smap in secondary_score_maps:
                    scores.append(smap.get(fid, 0.0))
                # dùng mean để tránh thiên lệch
                agg = sum(scores) / len(scores)
            else:
                agg = 0.0
            f["rerank_score"] = float(agg)

        # 4) Sort: ưu tiên rerank_score desc, tie-break bằng main_rank asc
        main_frames.sort(key=lambda x: (-x["rerank_score"], x["main_rank"]))

        # 5) Cắt top-k
        top_frames = [
            {"keyframeId": f["keyframeId"], "keyframePath": f["keyframePath"]}
            for f in main_frames[:limit]
        ]

        return {
            "main_keyword": main_keyword,
            "rerank_keywords": secondary_keywords,
            "frames": top_frames
        }

    finally:
        client.close()
