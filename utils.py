def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS