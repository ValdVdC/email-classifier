from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from services import extract_text_from_file, process_email
from utils import allowed_file
import os
import logging

logger = logging.getLogger(__name__)

# Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'groq_configured': bool(os.environ.get('GROQ_API_KEY'))
    })

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            email_content = extract_text_from_file(file_path, filename)
            
            if not email_content:
                return jsonify({'error': 'Não foi possível extrair texto do arquivo'}), 400
            
            result = process_email(email_content)
            os.remove(file_path)  # Limpar arquivo temporário
            
            return jsonify(result)
        
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

    except Exception as e:
        logger.error(f"Erro no upload: {str(e)}")
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500

@api_bp.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Texto não fornecido'}), 400
        
        email_content = data['text'].strip()
        
        if not email_content:
            return jsonify({'error': 'Texto vazio'}), 400
        
        result = process_email(email_content)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Erro no processamento de texto: {str(e)}")
        return jsonify({'error': f'Erro ao processar texto: {str(e)}'}), 500