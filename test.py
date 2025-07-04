import os
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Testa se as variáveis foram carregadas
groq_key = os.environ.get('GROQ_API_KEY')
secret_key = os.environ.get('SECRET_KEY')

print("GROQ_API_KEY:", "✓ Carregada" if groq_key else "✗ Não encontrada")
print("SECRET_KEY:", "✓ Carregada" if secret_key else "✗ Não encontrada")

if groq_key:
    print(f"GROQ_API_KEY começa com: {groq_key[:10]}...")