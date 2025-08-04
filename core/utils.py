def getKeyword(query: str) -> list[str]:
    return ["keyword1", "keyword2", "keyword3"]  # Ví dụ từ khóa

def getVector(path: str) -> list[float]:
    return [0.1, 0.2, 0.3] * 768  # Ví dụ vector

def getKeywordByVector(path: str) -> list[str]:
    return ["keyword1", "keyword2", "keyword3"]  # Ví dụ từ khóa

def searchByKeyword(keyword: str) -> list[str]:
    return ["keyword1", "keyword2", "keyword3"] # Ví dụ ảnh

def calSimilarity(vector1: list[float], vector2: list[float]) -> float:
    return 0.8 # Ví dụ độ tương đồng

def search_vector(vector: list[float]) -> list[str]:
    return ["con chó", "đang chạy", "bãi cỏ"]

def call_llm(prompt: str) -> str:
    print(f"Prompt to lLM: {prompt}")
    return "Một con chó đang chạy trên bãi cỏ vào buổi chiều"

def transcribe_audio(path: str) -> str:
    return "Một con chó chạy trong công viên. Sau đó, gặp một đứa bé đang chơi."

def transcribe_audio(path: str, start: float, end: float) -> str:
    return "Một con chó chạy trong công viên. Sau đó, gặp một đứa bé đang chơi."

def processQueryOnTranscript(transcript: str, query: str) -> str:
    prompt = f"""
        \"\"\"{transcript}\"\"\"

        {query}
    """
    result = call_llm(prompt)
    return result # Ví dụ: "Đoạn hội thoại này nói về một con mèo lười đang phơi nắng ngoài sân."

def extractKeyframes(path: str) -> list[str]:
    return ["frame1.jpg", "frame2.jpg", "frame3.jpg"]  # Ví dụ keyframes

def detectObjectImage(path: str, target: str) -> list[dict]:
    return [{"bbox": [10, 20, 30, 40], "label": target}]  # Ví dụ phát hiện vật thể

def detectObjectVideo(path: str, target: str) -> list[dict]:
    return [{"bbox": [10, 20, 30, 40], "label": target}]  # Ví dụ phát hiện vật thể trong video

def countObjects(tracker: list[dict], target: str) -> int:
    return len([obj for obj in tracker if obj['label'] == target])  # Ví dụ: con mèo = 8

def extractClipAroundBbox(keyframes: list[str], frame_index: int, bbox: dict) -> list[str]:
    # Trả về một clip nhỏ quanh bbox
    return keyframes[max(0, frame_index - 5):min(len(keyframes), frame_index + 5)]  # Ví dụ trích 10 keyframes quanh bbox

def classifyAction(clip: list[str]) -> str:
    # Gọi mô hình phân loại hành động
    return "đang chạy"