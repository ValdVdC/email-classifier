from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from services import extract_text_from_file, process_email
from utils import allowed_file
import os
import logging
from datetime import datetime
import time

logger = logging.getLogger(__name__)

# Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Variável para armazenar o último acesso
last_activity = datetime.now()

@main_bp.route('/')
def index():
    global last_activity
    last_activity = datetime.now()
    return render_template('index.html')

@main_bp.route('/health')
def health_check():
    """Endpoint de health check melhorado para manter a aplicação ativa"""
    global last_activity
    last_activity = datetime.now()
    
    # Simular alguma atividade para manter o processo ativo
    current_time = datetime.now()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': current_time.isoformat(),
        'uptime': str(current_time - last_activity),
        'groq_configured': bool(os.environ.get('GROQ_API_KEY')),
        'message': 'Application is running and active'
    })

@main_bp.route('/keepalive')
def keep_alive():
    """Endpoint específico para manter a aplicação ativa"""
    global last_activity
    last_activity = datetime.now()
    
    # Fazer uma pequena operação para manter o processo ativo
    import random
    dummy_calc = sum(range(100))  # Pequena operação matemática
    
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now().isoformat(),
        'pid': os.getpid(),
        'random_check': random.randint(1, 1000),
        'calc_result': dummy_calc
    })

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    global last_activity
    last_activity = datetime.now()
    
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
    global last_activity
    last_activity = datetime.now()
    
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