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