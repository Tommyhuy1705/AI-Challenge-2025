def generate_multimodal_report(path: str):
    """
    Giả lập quá trình tạo báo cáo đa phương thức cho một ảnh.
    Input:
        path (str): ảnh đầu vào (đường dẫn hoặc tên file)
    Output:
        str: báo cáo đa phương thức
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