"""
Unit tests for Weaviate Vector DB connection and CRUD operations.
"""
import os
import sys
import pytest
import torch
import clip
import weaviate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from weaviate.classes.init import Auth
from core.db_controller.connect import connect_db
from core.db_controller.crud import (get_info_by_frameId, get_info_by_videoId, get_all_frames_by_vector, get_all_frames_by_videoId, get_keyword_by_videoId,
get_objects_by_frameId, get_vector_by_frameId, get_timestamp_by_frameId, get_videoId_by_frameId, update_by_videoId,delete_videoId_by_id, delete_multipleObjects_by_id)

#@pytest.fixture(scope="module")

def test_get_all_frames_by_vector(client, text= None):
    #text = "dog"
    text_tokens = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_vector = model.encode_text(text_tokens).cpu().numpy().flatten().tolist()
    
    results = []
    frames = get_all_frames_by_vector(client, text_vector, limit=10)
    # video_col = client.collections.get("Keyframe")
    # frames = video_col.query.near_vector(
    #     near_vector=text_vector,
    #     limit=10,
    #     include_vector=True,
    #     return_properties=["keyframeId", "keyframePath"]
    # )
    for obj in frames.objects:
            props = obj.properties
            print(f"keyframeId: {props.get('keyframeId')}, keyframePath: {props.get('keyframePath')}")
            results.append(props)

    return results

def test_get_info_by_frameId(client, frame_id: str):
    info = get_info_by_frameId(client, frame_id)
    print("[Info by FrameId]", info.objects[0].properties if info.objects else "Not found")
    return info


def test_get_info_by_videoId(client, video_id: str):
    info = get_info_by_videoId(client, video_id)
    print("[Info by VideoId]", info.objects[0].properties if info.objects else "Not found")
    return info


def test_get_all_frames_by_videoId(client, video_id: str):
    frames = get_all_frames_by_videoId(client, video_id)
    print("[Frames by VideoId]", frames.objects[0].properties if frames.objects else "Not found")
    return frames


def test_get_keyword_by_videoId(client, video_id: str):
    keywords = get_keyword_by_videoId(client, video_id)
    print("[Keywords by VideoId]", keywords.objects[0].properties if keywords.objects else "Not found")
    return keywords


def test_get_objects_by_frameId(client, frame_id: str):
    objects = get_objects_by_frameId(client, frame_id)
    print("[Objects by FrameId]", objects.objects[0].properties if objects.objects else "Not found")
    return objects


def test_get_vector_by_frameId(client, frame_id: str):
    vectors = get_vector_by_frameId(client, frame_id)
    print("[Vector by FrameId]", vectors.objects[0].vector if vectors.objects else "Not found")
    return vectors


def test_get_timestamp_by_frameId(client, frame_id: str):
    ts = get_timestamp_by_frameId(client, frame_id)
    print("[Timestamp by FrameId]", ts.objects[0].properties if ts.objects else "Not found")
    return ts


def test_get_videoId_by_frameId(client, frame_id: str):
    videoId = get_videoId_by_frameId(client, frame_id)
    print("[VideoId by FrameId]", videoId.objects[0].properties if videoId.objects else "Not found")
    return videoId


def test_update_by_videoId(client, video_id: str):
    success = update_by_videoId(client, video_id)
    print(f"[Update by VideoId] Success: {success}")
    return success


def test_delete_videoId_by_id(client, video_id: str):
    success = delete_videoId_by_id(client, video_id)
    print(f"[Delete by VideoId] Success: {success}")
    return success


def test_delete_multipleObjects_by_id(client):
    success = delete_multipleObjects_by_id(client, "dummy")
    print(f"[Delete multiple objects] Success: {success}")
    return success

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    model.share_memory()

    # client = weaviate.connect_to_weaviate_cloud(
    #     cluster_url="https://jvs15pzsv21z89h3lcpq.c0.asia-southeast1.gcp.weaviate.cloud/",
    #     auth_credentials=Auth.api_key("dEo0TkZVNVBwZWVKRDUyQ19vSFNOWDBnY0Rrbkt3V3hFQ1BHc1Y3ZmZrdE5RVTR0RFlUTTV5UnhmZlFnPV92MjAw"),
    # )

    load_dotenv()
    url = os.getenv("WEAVIATE_URL")

    api = os.getenv("WEAVIATE_API_KEY")
    try:
        client = connect_db(url, api)
    except Exception as e:
        print(f"Failed to connect to Weaviate: {e}")


    if client.is_ready():
        print("Connection to Weaviate is ready.")
        text = "woman red dress cup"
        frame_id = "L26_V331_018"
        video_id = "L26_V331"

        info = test_get_info_by_frameId(client, frame_id)
        print(info)

        info_video = test_get_info_by_videoId(client, video_id)
        print(info_video)

        test = test_get_all_frames_by_vector(client, text)
        print(test)

        frames_id = test_get_all_frames_by_videoId(client, video_id)
        print(frames_id)

        keyword_video = test_get_keyword_by_videoId(client, video_id)
        print(keyword_video)

        objects_frame = test_get_objects_by_frameId(client, frame_id)
        print(objects_frame)

        vector_frameId = test_get_vector_by_frameId(client, frame_id)
        print(vector_frameId)

        time_frameId = test_get_timestamp_by_frameId(client, frame_id)
        print(time_frameId)

        video_from_frame = test_get_videoId_by_frameId(client, frame_id)
        print(video_from_frame)

        # test_update_by_videoId(client, "your-video-uuid")
        # test_delete_videoId_by_id(client, "your-video-uuid")
        # test_delete_multipleObjects_by_id(client)
    else:
        print("Failed to connect to Weaviate.")
    
    client.close()
    print("Client connection closed.")
    
