import streamlit as st
from typing import List, Dict
import random



def render_search_form():
    """Render thanh nhập query."""
    with st.form("search_form"):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        query = col1.text_input("Enter your query")
        optional = col2.text_input("Optional query")
        sql_filter = col3.text_input("Optional SQL filter (video_name, frame_id)")
        limit = col4.number_input("Limit", value=100, min_value=1, step=1)

        file = st.file_uploader("Image query or Text file query", type=["jpg", "png", "txt", "zip"])

        submitted = st.form_submit_button("Search")

        if submitted:
            return query, optional, sql_filter, limit, file
    return None, None, None, None, None


def render_image_card(video_id: str, frame: str):
    """Render 1 card chứa ảnh + nút hành động."""
    st.image("https://via.placeholder.com/150", caption=f"{video_id}_{frame}", width=150)
    cols = st.columns(3)
    with cols[0]:
        st.button("Image", key=f"{video_id}_{frame}_img")
    with cols[1]:
        st.button("Youtube", key=f"{video_id}_{frame}_yt")
    with cols[2]:
        st.button("Similar", key=f"{video_id}_{frame}_sim")


def render_results(results: Dict[str, List[str]]):
    """Render kết quả theo nhóm video_id."""
    for video_id, frames in results.items():
        st.markdown(f"### {video_id}")
        cols = st.columns(5)
        for i, frame in enumerate(frames):
            with cols[i % 5]:
                render_image_card(video_id, frame)


def main():
    st.title("Search for Data")

    if st.button("Session Data Clear"):
        st.session_state.clear()

    query, optional, sql_filter, limit, file = render_search_form()

    if query:
        st.write(f"Query 1: {query}, Query 2: {optional}, SQL Filter: {sql_filter if sql_filter else 'None'}")

        # results = mock_search_engine(query, optional, sql_filter, file)
        render_results(results)


if __name__ == "__main__":
    main()
