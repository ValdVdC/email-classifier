import threading
import time
import requests
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KeepAliveService:
    def __init__(self, app_url=None, interval=600):  # 10 minutos por padrão
        self.app_url = app_url or os.environ.get('APP_URL', 'https://vald-email-classifier.onrender.com')
        self.interval = interval  # segundos
        self.running = False
        self.thread = None
        
    def start(self):
        """Inicia o serviço de keep-alive"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
            self.thread.start()
            logger.info(f"Keep-alive service started - pinging {self.app_url} every {self.interval} seconds")
    
    def stop(self):
        """Para o serviço de keep-alive"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Keep-alive service stopped")
    
    def _keep_alive_loop(self):
        """Loop principal do keep-alive"""
        while self.running:
            try:
                # Aguarda o intervalo antes do primeiro ping
                time.sleep(self.interval)
                
                if not self.running:
                    break
                
                # Faz o ping para o endpoint de health
                response = requests.get(
                    f"{self.app_url}/health",
                    timeout=30,
                    headers={'User-Agent': 'KeepAlive-Internal/1.0'}
                )
                
                if response.status_code == 200:
                    logger.info(f"Keep-alive ping successful - {datetime.now()}")
                else:
                    logger.warning(f"Keep-alive ping failed with status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Keep-alive ping error: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in keep-alive: {str(e)}")

# Instância global do serviço
keep_alive_service = KeepAliveService()

def start_keep_alive():
    """Função para iniciar o keep-alive"""
    # Só ativa em produção
    if os.environ.get('FLASK_ENV') == 'production':
        keep_alive_service.start()

def stop_keep_alive():
    """Função para parar o keep-alive"""
    keep_alive_service.stop()