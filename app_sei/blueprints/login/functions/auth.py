import requests
import json
from flask import helpers
from dotenv import load_dotenv
import os

# Importação das variáveis a partir do arquivo .env
root_path = helpers.get_root_path('app')
load_dotenv(os.path.join(root_path, '.env'))
perfil_acesso = os.getenv('PERFIL_ACESSO')
url_mod_wssei = os.getenv('URL_MOD_WSSEI')
url_auth = url_mod_wssei + 'autenticar'
orgao = os.getenv('ORGAO')

def auth(usuario, senha):
    # Valida os dados de login usando o WSSEI, confere se o usuario tem perfil
    # de administrador e se está ativo. Retorna apenas alguns dados do usuario obtidos do WSSEI,
    # se necessário para outras funcionalidades, adicionar ao dict(usuario_logado).
    headers = {
    }
    payload = {
        "usuario": usuario,
        "senha": senha,
        "contexto": "",
        "orgao": orgao
    }
    try:
        response = requests.request("POST", url_auth, headers=headers, data=payload)
        response_parse = response.content.decode("utf-8", errors="ignore")
        content = json.loads(response_parse)

        if content.get('sucesso'):
            perfis = content['data'].get('perfis')
            usuario_logado = content['data']['loginData'].get('sigla')
            lista_perfis = []
            for perfil in perfis:
                lista_perfis.append(perfil.get('nome'))
            if perfil_acesso in lista_perfis:
                usuario_logado = {
                    "nome_completo": content['data']['loginData'].get('nome'),
                    "sigla_usuario": content['data']['loginData'].get('sigla'),
                    "token": content['data'].get('token'),
                    "acesso": True
                }
                return usuario_logado

            else:
                return {"acesso": False,
                        "mensagem": f"O usuário {usuario_logado} não possui perfil \"{perfil_acesso}\""}

        else:
            return {"acesso:": False,
                    "mensagem": "Usuário ou senha incorretos!"}

    except Exception as e:
        return {"acesso:": False,
                "mensagem": f"Erro: !{e}"}
