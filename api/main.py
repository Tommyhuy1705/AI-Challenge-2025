import os
from dotenv import load_dotenv
import sys
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.models.clip_model import CLIPModel
from core import boostrap
from routes.search import search_bp
load_dotenv()

app = Flask(__name__)

# Register blueprints
# app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(search_bp, url_prefix='/api/search')

if __name__ == '__main__':
    boostrap.load_clip_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
