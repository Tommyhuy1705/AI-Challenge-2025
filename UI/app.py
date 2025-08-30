import streamlit as st
from typing import List, Dict
import requests
from collections import defaultdict
import os
from PIL import Image

API_URL = "http://127.0.0.1:5000/api/search"


def render_search_form():
    """Render thanh nhập query."""
    with st.form("search_form"):
        col1, col2, col3,= st.columns([2, 2, 2])
        query = col1.text_input("Enter your query")
        optional = col2.text_input("Optional query")
        limit = col3.number_input("Limit", value=100, min_value=1, step=1)

        file = st.file_uploader("Image query or Text file query", type=["jpg", "png", "txt", "zip"])

        submitted = st.form_submit_button("Search")

        if submitted:
            return query, optional, limit, file
    return None, None, None, None


def render_image_card(keyframe_id: str, keyframe_path: str):
    """Render 1 card chứa ảnh + nút hành động."""
    st.image("https://via.placeholder.com/150", caption=keyframe_id, width=150)
    st.text(keyframe_path)

    cols = st.columns(3)
    with cols[0]:
        st.button("Image", key=f"{keyframe_id}_img")
    with cols[1]:
        st.button("Youtube", key=f"{keyframe_id}_yt")
    with cols[2]:
        st.button("Similar", key=f"{keyframe_id}_sim")


def render_results(results: List[Dict]):
    """Render kết quả keyframes từ API."""
    st.subheader("Search Results")
    cols = st.columns(5)

    for i, frame in enumerate(results):
        with cols[i % 5]:
            render_image_card(frame["keyframeId"], frame["keyframePath"])

def group_frames_by_video(api_response: dict):
    """
    Gom keyframes theo video từ JSON trả về.
    Trả về dict: {video_id: [list local image paths]}
    """
    grouped = defaultdict(list)

    if not api_response.get("success"):
        return {}

    frames = api_response["response"][0]["frames"]

    for f in frames:
        path = f["keyframePath"]
        video_id = os.path.basename(os.path.dirname(path))
        grouped[video_id].append(path)
    
    

    return dict(grouped)

@st.cache_data
def load_image_from_path(path: str):
    try:
        return Image.open(path)
    except Exception as e:
        print(f"Lỗi khi load ảnh {path}: {e}")
        return None


def main():
    st.title("Search for Data")

    if st.button("Session Data Clear"):
        st.session_state.clear()

    query, optional, limit, file = render_search_form()

    if query:
        st.write(f"Query 1: {query}, Query 2: {optional}, Limit: {limit}, File: {file.name if file else 'None'}")

        # Gửi request tới Flask API
   
        payload = {"query": query}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
    
        
        if data.get("success"):
            resp = data["response"]
            # nếu response là list
            if isinstance(resp, list):
                frames = resp[0].get("frames", [])
            # nếu response là dict
            elif isinstance(resp, dict):
                frames = resp.get("frames", [])
            else:
                st.error("Response format not recognized")
                return

            grouped = group_frames_by_video({"success": True, "response": [{"frames": frames}]})

            try:
                for vid, paths in grouped.items():
                    with st.expander(f" Video: {vid} ({len(paths)} frames)"):
                        cols = st.columns(3)
                        for i, p in enumerate(paths):
                            img = load_image_from_path(p)
                            if img:
                                with cols[i % 3]:
                                    st.image(img, caption=os.path.basename(p), use_column_width=True)
            except Exception as e:
                st.error(f"render error: {e}")
        else:
            st.error("No results found")

        
            
if __name__ == "__main__":
    main()
