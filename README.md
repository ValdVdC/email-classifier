# Classificador de Emails - Case Prático AutoU - Desenvolvimento

Solução inteligente para classificação automática de emails e geração de respostas usando IA.

##  Visão Geral

Este projeto foi desenvolvido como parte do desafio AutoU para criar uma aplicação web que:

- **Classifica emails** em categorias PRODUTIVO ou IMPRODUTIVO
- **Gera respostas automáticas** baseadas na classificação
- **Processa arquivos** .txt e .pdf
- **Interface web intuitiva** para upload e análise

##  Tecnologias Utilizadas

- **Backend**: Python, Flask
- **IA**: Groq API (LLaMA 3)
- **NLP**: NLTK para pré-processamento
- **Frontend**: HTML, CSS, JavaScript
- **Deploy**: Render.com
- **Processamento**: PyPDF2 para PDFs

##  Funcionalidades

###  Classificação Inteligente
- Analisa conteúdo de emails
- Classifica em PRODUTIVO ou IMPRODUTIVO
- Fornece nível de confiança da classificação

###  Geração de Respostas
- Resposta automática contextual
- Diferentes templates para cada categoria
- Linguagem profissional apropriada

###  Processamento de Arquivos
- Upload de arquivos .txt e .pdf
- Extração automática de texto
- Drag & drop interface

###  Interface Amigável
- Design moderno e responsivo
- Feedback visual em tempo real
- Experiência intuitiva

##  Instalação Local

### Pré-requisitos
```bash
Python 3.8+
Conta Groq API (gratuita)
```

### Passos
1. **Clone o repositório**
```bash
git clone https://github.com/ValdVdC/email-classifier.git
cd email-classifier
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
# Crie arquivo .env
GROQ_API_KEY=sua_chave_groq_aqui
SECRET_KEY=sua_chave_secreta_aqui
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://localhost:5000
```

## Deploy no Render

### Configuração Automática
1. **Fork/Clone este repositório**
2. **Conecte ao Render**
   - Vá para [render.com](https://render.com)
   - Conecte sua conta GitHub
   - Selecione este repositório

3. **Configure variáveis de ambiente**
   - `GROQ_API_KEY`: Sua chave da API Groq
   - `SECRET_KEY`: Será gerada automaticamente

4. **Deploy automático**
   - O Render detectará automaticamente o `render.yaml`
   - Build e deploy serão executados automaticamente

### Obter Chave Groq API (Gratuito)
1. Acesse [console.groq.com](https://console.groq.com)
2. Crie conta gratuita
3. Vá em "API Keys"
4. Gere nova chave
5. Copie e use na configuração

##  Estrutura do Projeto

```
email-classifier/
├── app.py                 # Aplicação Flask principal
├── config.py              # Configurações da aplicação
├── routes.py              # Definição das rotas/endpoints
├── services.py            # Lógica de IA e processamento
├── utils.py               # Funções utilitárias
├── test.py                # Testes e validação
├── requirements.txt       # Dependências Python
├── render.yaml           # Configuração deploy Render
├── README.md             # Documentação
├── .env                  # Variáveis ambiente (local)
├── .gitignore            # Arquivos ignorados pelo Git
├── static/               # Arquivos estáticos
│   ├── style.css         # Estilos CSS
│   └── script.js         # JavaScript frontend
├── templates/
│   └── index.html        # Interface web
└── uploads/              # Pasta temporária uploads
```

## Como Funciona

### 1. Processamento de Entrada
- Upload de arquivo ou texto direto
- Extração de texto (TXT/PDF)
- Pré-processamento com NLTK

### 2. Classificação IA
- Prompt especializado para Groq API
- Análise contextual do conteúdo
- Classificação binária: PRODUTIVO/IMPRODUTIVO

### 3. Geração de Resposta
- Template específico por categoria
- Resposta contextual e profissional
- Linguagem apropriada para setor financeiro

### 4. Apresentação
- Interface visual clara
- Indicadores de confiança
- Resposta sugerida formatada


### Melhorar Interface
Edite `templates/index.html`:
- Adicione novos estilos CSS
- Implemente funcionalidades JS
- Integre frameworks (Bootstrap, etc.)

## Exemplos de Uso

### Email Produtivo
```
Assunto: Solicitação de Suporte - Sistema Indisponível

Prezados,

Nosso sistema financeiro está apresentando instabilidade desde às 14h. 
Solicito suporte urgente para resolução.

Atenciosamente,
João Silva
```

**Resultado**: PRODUTIVO (Confiança: 9/10)

### Email Improdutivo
```
Assunto: Feliz Aniversário!

Oi pessoal,

Quero desejar um feliz aniversário para nossa colega Maria!
Parabéns! 🎉

Abraços,
Ana
```

**Resultado**: IMPRODUTIVO (Confiança: 9/10)

## Métricas e Monitoramento

### Endpoint de Saúde
```
GET /health
```

Retorna:
```json
{
  "status": "healthy",
  "groq_configured": true
}
```

### Logs
- Aplicação registra todas as operações
- Erros são logados com detalhes
- Monitoramento via Render dashboard

## Solução de Problemas

### Erro: "Groq API Key não configurada"
```bash
# Verifique se a variável está definida
echo $GROQ_API_KEY

# Configure se necessário
export GROQ_API_KEY="sua_chave_aqui"
```

### Erro: "Arquivo não suportado"
- Verifique se o arquivo é .txt ou .pdf
- Tamanho máximo: 16MB
- Encoding: UTF-8 preferencial

### Erro: "Falha na classificação"
- Verifique conectividade com Groq API
- Confirme se a chave API está válida
- Tente novamente (pode ser limitação temporária)

## Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Agradecimentos

- **AutoU** pela oportunidade do desafio
- **Groq** pela API gratuita de alta qualidade
- **Render** pela plataforma de deploy gratuita
- **Comunidade Open Source** pelas bibliotecas utilizadas

---

*Desenvolvido por Osvaldo Vasconcelos de Carvalho para o Case Prático AutoU*
