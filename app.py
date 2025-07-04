from flask import Flask
from config import Config
from routes import main_bp, api_bp
import os
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Criar pasta de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)