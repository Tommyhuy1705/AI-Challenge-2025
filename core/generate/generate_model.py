def get_response(prompt: str) -> str:
    print(f"Prompt to LLM: {prompt}")
    return "Một con chó đang chạy trên bãi cỏ vào buổi chiều"

def summary_from_transcript(transcript: str, query: str) -> str:
    prompt = f"""
        \"\"\"{transcript}\"\"\"

        {query}
    """
    result = get_response(prompt)
    return result # Ví dụ: "Đoạn hội thoại này nói về một con mèo lười đang phơi nắng ngoài sân."