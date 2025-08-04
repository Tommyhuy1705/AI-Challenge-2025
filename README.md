## Project Structure  
```plaintext
AI Challenge 2025/
├── app_GUI/                        # Giao diện người dùng & API xử lý
│   ├── API.py                      # FastAPI hoặc các endpoint chính
│   ├── handlers.py                 # Kết nối các thành phần NLP/Image/Audio
│   └── interface.py                # Giao diện người dùng (Streamlit)
│
├── configs/                        # Cấu hình model, prompt, pipeline
│   ├── model_config.yaml           # Cấu hình cho các model
│   └── prompt_templates.json       # Prompt mẫu cho training hoặc inference
│
├── data/                           # Dữ liệu gốc và đã xử lý
│   ├── processed/                  # Dữ liệu sau khi tiền xử lý
│   ├── prompts/                    # Dữ liệu prompt dạng JSON
│   └── raw/                        # Dữ liệu thô ban đầu (ảnh, audio, video, text)
│
├── datasets/                       # Script để format & tải dữ liệu
│   ├── format_audio_dataset.py     # Format dữ liệu âm thanh
│   └── format_video_dataset.py     # Format dữ liệu video
│
├── docs/                           # Tài liệu mô tả hệ thống
│
├── logs/                           # Thư mục lưu log khi training/inference
│
├── models/                         # Các mô hình chính
│   ├── audio/                      # Model xử lý âm thanh
│   ├── clip/                       # Model CLIP xử lý ảnh + text
│   ├── llama/                      # Model LLM
│   └── multimodal_agent.py         # Lớp kết hợp các model thành 1 agent tổng
│
├── notebooks/                      # Jupyter Notebook thử nghiệm
│   ├── EDA.ipynb                   # Phân tích dữ liệu ban đầu
│   ├── inference_demo.ipynb        # Demo inference nhiều modal
│   └── prompt_tuning.ipynb         # Tuning prompt / adapter
│
├── retrieval/                      # Tìm kiếm nội dung theo vector
│   ├── audio_index.py              # Tìm kiếm theo đặc trưng audio
│   ├── image_index.py              # Tìm kiếm theo đặc trưng ảnh
│   └── search_engine.py            # Bộ máy tìm kiếm chính
│
├── scripts/                        # Script demo/test nhanh
│   ├── demo_streamlit.py           # Demo giao diện
│   ├── infer_image.py              # Chạy inference ảnh
│   └── test_prompt.py              # Kiểm thử prompt
│
├── test_model/                     # Kiểm thử và benchmark model
│
├── training/                       # Quá trình huấn luyện model
│   ├── evaluate.py                 # Đánh giá model
│   ├── train.py                    # Entry point training
│   └── trainer.py                  # Logic training
│
├── utils/                          # Hàm tiện ích
│   ├── logger.py                   # Ghi log
│   ├── metrics.py                  # Hàm đo độ chính xác, F1, BLEU, ...
│   └── visualization.py            # Hàm vẽ biểu đồ, attention,...
│
├── .gitignore                      # File loại trừ khi push Git
├── main.py                         # Chạy toàn bộ hệ thống end-to-end
├── README.md                       # Mô tả project
└── requirements.txt                # Các thư viện cần cài
```
