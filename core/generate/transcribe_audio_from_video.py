from core.supporter.helper import transcribe_audio, processQueryOnTranscript
import re
def transcribe_audio_from_video(query: str, srces: list[str]) -> dict:
    """
    Purpose: Tóm tắt nội dung đoạn hội thoại trong video.

    Circumtance: user nhập query, user có thể chọn 1 hoặc nhiều video để tóm tắt nội dung hội thoại.

    Args: 
        query (str): Câu truy vấn của người dùng.
        srces (list[str]): Đường dẫn đến ảnh hoặc video nguồn.

    Returns:
        dict: Kết quả JSON, ví dụ:
            {
                "frame": số-thứ-tự-của-frame,
                "bbox": [x1, y1, x2, y2],
                "label": tên-vật-thể,
                "action": tên-hành-động
            }

    Pipelines: Trích xuất audio từ video -> Chuyển audio thành text -> Đưa text và query cho LLM -> Trả về kết quả.
    """
    time_val = re.search(r'phút\s+(\d+)\s+đến\s+(\d+)', query)
    
    if time_val:
        start = time_val.group(1)
        end = time_val.group(2)
    else:
        start = None
        end = None

    results = dict()
    for id, video in enumerate(srces):
        transcript = transcribe_audio(video, start, end)
        answer = processQueryOnTranscript(transcript, query) # Ghép transcript và query vào một prompt, gửi cho LLM, nhận kết quả.

        results[f'vid_id_{id}'] = {
            "video": video,
            "summary": answer
        }

    return results