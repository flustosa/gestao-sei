SHELL := /bin/bash 

ENV=venv

help: ## Mostra essa ajuda. Voce pode usar tab para completar os comandos
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//' | sed -e 's|^\ ||'

check: ## Verifica a existência do arquivo ".env"
	@if [ ! -f ".env" ]; then \
		echo "Arquivo .env não encontrado. Criando um novo a partir do template env.env, ajuste os parâmetros para rodar o programa." >&2 ; \
		cp env.env .env; \
		exit 1; \
	else \
		echo "Arquivo .env encontrado. Ajuste os parâmetros para rodar o programa." ; \
	fi

env: ## Cria e acessa o ambiente virutal do python e instala os requisitos.
	python3 -m venv ${ENV} && source ${ENV}/bin/activate && pip install -r requirements.txt


db: ## Cria a estrutura e inicia o banco de dados (sqlite) com o Flask
	@echo -e "Iniciando o DB"
	source ${ENV}/bin/activate && cd app_sei && flask db init
	@echo Migrando o DB
	source ${ENV}/bin/activate && cd app_sei && flask db migrate
	@echo Fazendo o upgrade do DB
	source ${ENV}/bin/activate && cd app_sei && flask db upgrade


run: check ## Ativa o ambiente virtual (venv) e roda o app
	source venv/bin/activate && python3 main.py


init:	env db ## Faz a sequência de atualizar repositórios (pull), cria o ambiente virtual (env) e cria o DB (sqlite)


cleardb: # Apaga estrutura do DB
	@echo Removendo pasta "/instance"
	rm -rf instance
	@echo Removendo pasta "/migrations"
	cd app_sei && rm -rf migrations


restartdb: cleardb db ## Apaga e recria o Banco de Dados (SQLite)


