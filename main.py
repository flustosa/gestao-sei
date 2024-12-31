from app_sei.app import create_app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
    
# TODO: Registro de log em banco
# TODO: Carregar unidades e outros dados no banco
# TODO: Operações em lote
# TODO: Consulta com visualização e download de logs
