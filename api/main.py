import os
from dotenv import load_dotenv
import sys
from flask import Flask
from routes.chat import chat_bp
from routes.search import search_bp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(search_bp, url_prefix='/api/search')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
