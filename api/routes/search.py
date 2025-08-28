from flask import Blueprint, request, jsonify
from core.engine.dispatcher import call_api, navigate

search_bp = Blueprint('search', __name__)

@search_bp.route('/query', methods=['POST'])
def search_query():
    """
    REST API Endpoint để tìm kiếm video dựa trên mô tả của người dùng.
    
    Cách sử dụng:
    Gửi POST request đến endpoint: /api/search/query
    
    Request Body (JSON):
    {
        "query": "mô tả nội dung video cần tìm"
    }
    
    Response Format:
    {
        "response": {
            "key0": "chạy",
            "frames": [
                {
                    "keyframeId": "frame123",
                    "keyframePath": "/path/to/frame.jpg"
                }
            ]
        },
        "success": true
    }
    
    Error Response:
    {
        "error": "Mô tả lỗi",
        "success": false
    }
    
    Lưu ý:
    - API sử dụng GPT-OSS để phân tích query và tự động chọn function phù hợp
    - Đối với tìm kiếm theo trình tự, model sẽ tự động sử dụng find_flow function
    - Kết quả trả về bao gồm các keyframe phù hợp với yêu cầu tìm kiếm
    - Các keyframe được sắp xếp theo độ phù hợp với query
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing query in request", 
                "success": False
            }), 400
            
        # Call GPT-OSS API with the query
        response = call_api(data['query'])
        
        # Navigate will handle function calling and return appropriate response
        result = navigate(response)
        
        return jsonify({
            "response": result,
            "success": True
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e), 
            "success": False
        }), 500
