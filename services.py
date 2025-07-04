import os
import re
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from groq import Groq
import logging

logger = logging.getLogger(__name__)

# Inicializar cliente Groq
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Baixar recursos NLTK
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

def extract_text_from_file(file_path, filename):
    """Extrai texto de arquivos TXT ou PDF"""
    try:
        if filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif filename.lower().endswith('.pdf'):
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do arquivo {filename}: {str(e)}")
        return None

def preprocess_text(text):
    """Pré-processa o texto removendo caracteres especiais e stop words"""
    try:
        text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
        return ' '.join(filtered_tokens)
    except:
        return re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)

def classify_email_with_groq(email_content):
    """Classifica o email usando Groq API"""
    try:
        classification_prompt = f"""
        Você é um assistente especializado em classificação de emails para uma empresa do setor financeiro.

        Analise o email abaixo e classifique-o em uma das duas categorias:

        PRODUTIVO: Emails que requerem ação ou resposta específica (solicitações de suporte, atualizações sobre casos, dúvidas sobre sistemas, pedidos de informações importantes)

        IMPRODUTIVO: Emails que não necessitam ação imediata (mensagens de felicitações, agradecimentos, conversas casuais, spam)

        Email para análise:
        {email_content}

        Responda APENAS com:
        Categoria: [PRODUTIVO ou IMPRODUTIVO]
        Confiança: [número de 1-10]
        Razão: [breve explicação da classificação]
        """

        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um classificador de emails especializado em ambiente corporativo financeiro. Seja preciso e objetivo nas classificações."
                },
                {
                    "role": "user",
                    "content": classification_prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.1,
            max_tokens=200
        )

        classification_result = response.choices[0].message.content
        
        if "IMPRODUTIVO" in classification_result.upper():
            category = "IMPRODUTIVO"
        elif "PRODUTIVO" in classification_result.upper():
            category = "PRODUTIVO"
        else:
            categoria_match = re.search(r'Categoria:\s*(PRODUTIVO|IMPRODUTIVO)', classification_result.upper())
            category = categoria_match.group(1) if categoria_match else "PRODUTIVO"
            
        return {
            "category": category,
            "full_response": classification_result,
            "confidence": extract_confidence(classification_result)
        }

    except Exception as e:
        logger.error(f"Erro na classificação com Groq: {str(e)}")
        return {
            "category": "ERRO",
            "full_response": f"Erro ao classificar: {str(e)}",
            "confidence": 0
        }

def generate_response_with_groq(email_content, category):
    """Gera resposta automática baseada na categoria"""
    try:
        if category == "PRODUTIVO":
            response_prompt = f"""
            Você deve escrever uma resposta profissional para este email. Escreva APENAS o texto da resposta, sem introduções ou explicações.

            Email original:
            {email_content}

            Escreva uma resposta que:
            - Confirme o recebimento
            - Indique próximos passos ou timeline
            - Seja profissional e cortês
            - Tenha no máximo 3 parágrafos
            - Use linguagem formal apropriada para ambiente financeiro

            Resposta:
            """
        else:
            response_prompt = f"""
            Você deve escrever uma resposta cordial para este email. Escreva APENAS o texto da resposta, sem introduções ou explicações.

            Email original:
            {email_content}

            Escreva uma resposta que:
            - Seja cordial e educada
            - Confirme o recebimento da mensagem
            - Seja breve (máximo 2 parágrafos)
            - Mantenha tom profissional mas amigável

            Resposta:
            """

        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que escreve respostas de email profissionais. Escreva APENAS o conteúdo da resposta, sem prefácio, explicações ou comentários adicionais."
                },
                {
                    "role": "user",
                    "content": response_prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=300
        )

        # Limpar a resposta removendo possíveis prefácios
        raw_response = response.choices[0].message.content.strip()
        
        # Remover padrões comuns de prefácio
        prefixes_to_remove = [
            "Aqui vai uma resposta automática profissional e útil:",
            "Aqui está uma resposta profissional:",
            "Aqui vai uma resposta cordial:",
            "Aqui está uma resposta cordial:",
            "Resposta automática:",
            "Resposta:",
            "Assunto:",
            "Prezado(a),"
        ]
        
        cleaned_response = raw_response
        for prefix in prefixes_to_remove:
            if cleaned_response.startswith(prefix):
                cleaned_response = cleaned_response[len(prefix):].strip()
        
        # Remover quebras de linha desnecessárias no início
        cleaned_response = cleaned_response.lstrip('\n').strip()
        
        return cleaned_response

    except Exception as e:
        logger.error(f"Erro na geração de resposta com Groq: {str(e)}")
        return f"Erro ao gerar resposta automática: {str(e)}"

def extract_confidence(text):
    """Extrai o nível de confiança da resposta"""
    try:
        confidence_match = re.search(r'Confiança:\s*(\d+)', text)
        return int(confidence_match.group(1)) if confidence_match else 7
    except:
        return 7

def process_email(email_content):
    """Processa o email: classifica e gera resposta"""
    try:
        processed_text = preprocess_text(email_content)
        classification = classify_email_with_groq(email_content)
        
        if classification['category'] == 'ERRO':
            return {
                'error': 'Erro na classificação',
                'details': classification['full_response']
            }
        
        suggested_response = generate_response_with_groq(email_content, classification['category'])
        
        return {
            'success': True,
            'original_content': email_content,
            'processed_content': processed_text,
            'classification': classification['category'],
            'classification_details': classification['full_response'],
            'confidence': classification['confidence'],
            'suggested_response': suggested_response
        }

    except Exception as e:
        logger.error(f"Erro no processamento do email: {str(e)}")
        return {
            'error': 'Erro no processamento',
            'details': str(e)
        }