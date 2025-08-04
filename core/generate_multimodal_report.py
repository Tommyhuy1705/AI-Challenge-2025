from core.utils import getVector, search_vector, call_llm, transcribe_audio, extract_keyframes
import os
def generate_multimodal_report(path: str):
    """
    Purpose: Tạo báo cáo ngắn về nội dung đa phương thức (image + video + audio + text).

    Circumtance: Khi người dùng muốn tạo một báo cáo tổng hợp về nội dung của một video bao gồm hình ảnh mô tả, transcript và thời gian.

    Args:
        video_path (str): Đường dẫn tới video cần phân tích.

    Returns:
        str: Đoạn báo cáo được sinh ra, bao gồm tóm tắt + mô tả ảnh + thời gian xuất hiện.

    Pipelines: 
        Trích xuất frame chính từ video -> Mô tả từng frame bằng vision + LLM ->
        Trích transcript từ audio -> Tóm tắt toàn video -> Tổng hợp tất cả thành báo cáo định dạng text.
    """


    if not os.path.exists(path):
        return " Video is not exist"
    
    keyframes = extract_keyframes(path) # return List[Dict] chứa 'frame_path', 'timestamp'

    descriptions = []
    for frame in keyframes:
        vector = getVector(frame['frame_path'])
        info = search_vector(vector)
        caption = call_llm(f"Mô tả nội dung ảnh tại thời điểm {frame['timestamp']}: {info}")
        descriptions.append({
            "frame_path": frame['frame_path'],
            "timestamp": frame['timestamp'],
            "description": caption
        })

    # Trích đoạn hội thoại từ audio trong video
    transcript = transcribe_audio(path)
    summary = call_llm("Tóm tắt nội dung chính của video dựa trên đoạn transcript sau:\n{transcript}")

    #Tạo báo cáo tổng hợp
    report = {
        "video_path": path,
        "summary": summary,
        "keyframes": descriptions,
    }

    return report