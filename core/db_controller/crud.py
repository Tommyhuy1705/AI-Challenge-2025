"""
CRUD operations for Weaviate Vector DB.
All functions accept a Weaviate client from connect.py.
"""

import weaviate
from weaviate import Client
from weaviate.auth import AuthApiKey
from weaviate.classes.config import Configure, DataType, Property, VectorDistances, GenerativeSearches
import weaviate.classes.config as wvc
from weaviate.classes.query import MetadataQuery, Filter, QueryReference

COLLECTION_NAME = "aic-2025"

def get_info_by_frameId(client: Client, frame_id: str, collection_name: str = COLLECTION_NAME) -> dict:
    frame_col = client.collections.get("Keyframe")
    info = frame_col.query.fetch_objects(
        filters=Filter.by_property("keyframeId").equal(frame_id),
        #include_vector=True,
        return_properties=["keyframeId", "keyframePath", "videoId", "objects", "timestamp", "frameIndex"]
    )
    return info

def get_info_by_videoId(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> dict:
    video_col = client.collections.get("Video")
    info = video_col.query.fetch_objects(
        filters=Filter.by_property("videoId").equal(video_id),
        #include_vector=True,
        return_properties=["videoId", "videoPath", "keywords", "keyframeIds", "keyframePaths", "timestamps", "frameIndices"]
    )
    return info

def get_all_frames_by_vector(client: Client, vector: str, limit: int = 5, collection_name: str = COLLECTION_NAME):
    video_col = client.collections.get("Keyframe")
    frames = video_col.query.near_vector(
        near_vector=vector,
        limit=limit,
        include_vector=True,
        return_properties=["keyframeId", "keyframePath"]
    )
    return frames

def get_all_frames_by_videoId(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> dict:
    video_col = client.collections.get("Video")
    frames = video_col.query.fetch_objects(
        filters=Filter.by_property("videoId").equal(video_id),
        #include_vector = True,
        return_properties = ["keyframeIds", "keyframePaths"]
    )
    return frames

def get_keyword_by_videoId(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> dict:
    video_col = client.collections.get("Video")
    keywords = video_col.query.fetch_objects(
        filters=Filter.by_property("videoId").equal(video_id),
        include_vector = True,
        return_properties = ["keywords"]
    )
    return keywords

def get_objects_by_frameId(client: Client, frame_id: str, collection_name: str = COLLECTION_NAME) -> dict:
    frame_col = client.collections.get("Keyframe")
    objects = frame_col.query.fetch_objects(
        filters=Filter.by_property("keyframeId").equal(frame_id),
        include_vector = True,
        return_properties = ["objects"]
    )
    return objects

def get_vector_by_frameId(client: Client, frame_id: str, collection_name: str = COLLECTION_NAME):
    frame_col = client.collections.get("Keyframe")
    vectors = frame_col.query.fetch_objects(
        filters=Filter.by_property("keyframeId").equal(frame_id),
        include_vector = True,
        #return_properties = ["vectorFrame"]
    )
    return vectors
def get_timestamp_by_frameId(client: Client, frame_id: str, collection_name: str = COLLECTION_NAME):
    frame_col = client.collections.get("Keyframe")
    timestamp = frame_col.query.fetch_objects(
        filters=Filter.by_property("keyframeId").equal(frame_id),
        #include_vector = True,
        return_properties = ["timestamp"]
    )
    return timestamp

def get_videoId_by_frameId(client: Client, frame_id: str, limit: int = 3, collection_name: str = COLLECTION_NAME) -> dict:
    frame_col = client.collections.get("Keyframe")
    videoFrame = frame_col.query.fetch_objects(
        filters=Filter.by_property("keyframeId").equal(frame_id),
        limit = limit,
        return_references=[
            QueryReference(
                link_on="inVideo",
                return_properties=["videoId"]
            )
        ]
    )
    return videoFrame

def update_by_videoId(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> bool:
    video_col = client.collections.get("Video")
    updateObject = video_col.data.update(
        uuid = video_id,
        properties = {
            "videoId": "abcd",
            "videoPath": "abcd",
            "keywords": ["keyword1", "keyword2"],
            "keyframeIds": ["frame1.jpg", "frame2.jpg"]
        }
    )
    return True
    
def delete_videoId_by_id(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> bool:
    uuid_to_delete = video_id
    video_col = client.collections.get("Video")
    deleteObject = video_col.data.delete_by_id(
        uuid= uuid_to_delete
    )
    return True

def delete_multipleObjects_by_id(client: Client, video_id: str, collection_name: str = COLLECTION_NAME) -> bool:
    video_col = client.collections.get("Video")
    deleteObject = video_col.data.delete_many(
        where=Filter.by_property("videoId").like("_____*")
    )
    return True