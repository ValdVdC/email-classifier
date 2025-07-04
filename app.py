from flask import Flask
from config import Config
from routes import main_bp, api_bp
from keepalive import start_keep_alive, stop_keep_alive
import os
import logging
import atexit
import signal
import sys

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar logging para produção
    if os.environ.get('FLASK_ENV') == 'production':
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # Criar pasta de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app

app = create_app()

def shutdown_handler(signum, frame):
    logging.info("Received shutdown signal, stopping keep-alive service...")
    stop_keep_alive()
    sys.exit(0)

# Registrar handlers de shutdown
atexit.register(stop_keep_alive)
signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    # Iniciar keep-alive em produção
    if is_production:
        start_keep_alive()
    
    if is_production:
        # Configurações para produção
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=False,
            threaded=True,  # Importante para múltiplas requisições
            use_reloader=False
        )
    else:
        # Configurações para desenvolvimento
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=True
        )