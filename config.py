import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB