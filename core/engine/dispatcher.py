# điều hương gpt oss
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from core.engine.search_engine import search

def call_api(user_query: str):
    load_dotenv()
    hf_token = os.getenv("HF_SECRET")

    client = OpenAI(
    base_url="https://router.huggingface.co/v1",
        api_key=hf_token,)

    #Lấy file json -> gán vào my_tools
    BASE_DIR = os.path.dirname(__file__)
    json_path = os.path.join(BASE_DIR, "..", "function_calling.json") # Từ engine/ → ra ngoài core/ → file json
    with open(os.path.abspath(json_path), "r", encoding="utf-8") as functions_calling:
        my_tools = json.load(functions_calling)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user", 
                "content": f'{user_query}'
            }
        ],
        tools = my_tools,
        tool_choice="auto"
    )
    
    # print(completion.choices[0].message.to_json()) # in ra toàn bộ content từ api.
    return completion

def navigate(response: dict):
    '''
    - Nhận output từ call api
    - Main Function: Hàm xử lý dictionary từ output của gpt oss -> if else -> gửi key đến search_engine
    '''
    msg = response.choices[0].message

    # Nếu model trả về tool_call
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            args_str = tool_call.function.arguments
            args = json.loads(args_str)  # parse JSON string

            if fn_name == "search":
                result = search(**args)
                print("Function result:", result)
                # Có thể trả về trực tiếp cho user
                return f"Function S is running..."
            
            elif fn_name == "find_flow":
                # result = find_flow(**args)
                print("Function result:", result)
                # Có thể trả về trực tiếp cho user
                return result
    else:
        # Không có tool_call, chỉ in content
        print("Model content:", msg.content)
        return msg.content