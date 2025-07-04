let selectedFile = null;
let isProcessing = false;
let currentRequest = null;
        
        // Funcionalidade de drag and drop
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const filePreview = document.getElementById('filePreview');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            // Validar tipo de arquivo
            const allowedTypes = ['.txt', '.pdf'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!allowedTypes.includes(fileExtension)) {
                showError('Formato de arquivo não suportado. Use apenas .txt ou .pdf');
                return;
            }
            
            // Validar tamanho (10MB)
            if (file.size > 10 * 1024 * 1024) {
                showError('Arquivo muito grande. Tamanho máximo: 10MB');
                return;
            }
            
            selectedFile = file;
            showFilePreview(file);
            
            // Desabilitar área de texto quando arquivo é selecionado
            const textSection = document.getElementById('textInputSection');
            textSection.classList.add('disabled');
        }
        
        function showFilePreview(file) {
            const fileName = document.getElementById('fileName');
            const fileSize = document.getElementById('fileSize');
            const fileIcon = document.getElementById('fileIcon');
            
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileIcon.textContent = file.name.endsWith('.pdf') ? '📄' : '📝';
            
            filePreview.style.display = 'block';
            hideError();
        }
        
        function removeFile() {
            selectedFile = null;
            filePreview.style.display = 'none';
            fileInput.value = '';
            
            // Reabilitar área de texto
            const textSection = document.getElementById('textInputSection');
            textSection.classList.remove('disabled');
        }
        
        function confirmUpload() {
            if (!selectedFile) {
                showError('Nenhum arquivo selecionado.');
                return;
            }
            
            if (isProcessing) return;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            showLoading();
     
            const controller = new AbortController();
            currentRequest = controller;
            
            fetch('/upload', {
                method: 'POST',
                body: formData,
                signal: controller.signal
            })
            .then(response => response.json())
            .then(data => {
                currentRequest = null;
                hideLoading();
                if (data.error) {
                    showError(data.error + (data.details ? ': ' + data.details : ''));
                } else {
                    showResults(data);
                    if (selectedFile) {
                        removeFile();
                    }
                }
            })
            .catch(error => {
                currentRequest = null;
                hideLoading();
                if (error.name !== 'AbortError') {
                    showError('Erro ao processar arquivo: ' + error.message);
                }
            });
        }
        
        function processText() {
        const text = document.getElementById('emailText').value.trim();
        if (!text) {
            showError('Por favor, insira o texto do email.');
            return;
        }
        
        if (isProcessing) return; 
        
        showLoading();
        
        const controller = new AbortController();
        currentRequest = controller;
        
        fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
            signal: controller.signal
        })
        .then(response => response.json())
        .then(data => {
            currentRequest = null;
            hideLoading();
            if (data.error) {
                showError(data.error + (data.details ? ': ' + data.details : ''));
            } else {
                showResults(data);
                if (selectedFile) {
                    removeFile();
                }
            }
        })
        .catch(error => {
            currentRequest = null;
            hideLoading();
            if (error.name !== 'AbortError') {
                showError('Erro ao processar texto: ' + error.message);
            }
        });
    }
        
        function showLoading() {
            document.getElementById('loadingOverlay').style.display = 'flex';
            document.getElementById('results').style.display = 'none';
            document.getElementById('clearBtn').style.display = 'none';
            hideError();
            isProcessing = true;
        }
        
        function hideLoading() {
            document.getElementById('loadingOverlay').style.display = 'none';
            isProcessing = false;
        }
        
        function showError(message) {
            const errorElement = document.getElementById('errorMessage');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            document.getElementById('results').style.display = 'none';
        }
        
        function hideError() {
            document.getElementById('errorMessage').style.display = 'none';
        }
        
        function showResults(data) {
            // Atualizar classificação
            const badge = document.getElementById('classificationBadge');
            const details = document.getElementById('classificationDetails');
            
            badge.textContent = data.classification;
            badge.className = 'classification-badge ' + 
                (data.classification === 'PRODUTIVO' ? 'productive' : 'unproductive');
            
            details.textContent = data.classification_details || 'Classificação realizada com sucesso.';
            
            // Atualizar confiança
            const confidence = data.confidence || 7;
            document.getElementById('confidenceText').textContent = confidence;
            document.getElementById('confidenceFill').style.width = (confidence * 10) + '%';
            
            // Atualizar resposta sugerida
            document.getElementById('suggestedResponse').textContent = data.suggested_response;
            
            // Mostrar botão limpar
            document.getElementById('clearBtn').style.display = 'inline-block';
            
            // Mostrar resultados
            document.getElementById('results').style.display = 'block';
            hideError();
        }

        function clearResults() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('clearBtn').style.display = 'none';
            document.getElementById('emailText').value = '';
            hideError();
        }
        function cancelProcessing() {
            if (currentRequest) {
                currentRequest.abort();
                currentRequest = null;
            }
            isProcessing = false;
            hideLoading();
            showError('Processamento cancelado pelo usuário.');
        }
        function copyResponse() {
            const response = document.getElementById('suggestedResponse').textContent;
            navigator.clipboard.writeText(response).then(() => {
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.textContent;
                btn.textContent = '✅ Copiado!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        }
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
        
        function toggleTheme() {
            const body = document.body;
            const themeBtn = document.getElementById('themeToggle');
            
            if (body.classList.contains('dark-mode')) {
                body.classList.remove('dark-mode');
                themeBtn.classList.remove('dark-active');
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.add('dark-mode');
                themeBtn.classList.add('dark-active');
                localStorage.setItem('theme', 'dark');
            }
        }
        
        // Carregar tema salvo
        window.addEventListener('load', () => {
            const savedTheme = localStorage.getItem('theme');
            const themeBtn = document.getElementById('themeToggle');
            
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
                themeBtn.classList.add('dark-active');
            }
        });