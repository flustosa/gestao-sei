# Aplicação Web - Gestão SEI
<p>Aplicação para uso pelas equipes de gestão negocial do Sistema Eletrônico de Processos (SEI) - Utiliza comunicação via webservice (REST e SOAP) para envio de requisições ao Sistema Eletrônico de Processos (SEI), contendo, inicialmente, apenas a funcionalidade de **bloqueio** e **desbloqueio** de processos, além do lançamento de andamento após a operação.</p>

<p>Versão em Flask, ainda pendente de melhorias em javascript no frontend, priorizando inicialmente as funcionalidades de negócio.</p>


## Requisitos
 - Requisito Mínimo é o SEI 4.0 (ou superior) e o [Módulo Rest WSSEI](https://github.com/pengovbr/mod-wssei "Clique e acesse") - Não foi testado em outras versões do SEI ou do Módulo WSSEI. 


## Procedimentos para Instalação em Docker
1. Clonar o projeto
2. Verificar configurações de portas no docker-compose.yml (host configurado na porta 8000 e container na porta 5000)
	- Cuidado ao alterar a localização dos volumes no yml, pois está organizado de forma que não tenha conflito com a subida do ambiente sem uso do Docker, quando utilizar as [orientações para desenvolvimento](#orientações-para-desenvolvimento).
3. Fazer uma cópia do arquivo "env.env" com o nome de ".env" e inserir os dados do Órgão, especialmente o ambiente que será instalado (dev/hom/prod).
4. Fazer o build do projeto
```sudo docker compose build```
5. Subir projeto com docker compose:
```sudo docker compose up -d```


## Orientações Negociais
1. Para o funcionamento da aplicação é necessário parametrizar o acesso externo, seguindo os seguintes passos no SEI:
	- Acessar o menu "Administração" > "Sistemas" > "Novo";
	- Selecionar o Órgão, informar uma Sigla para o Sistema (essa será a identificação utilizada para configurar a comunicação) e o Nome (o nome somente é visualizado internamente pela gestão do SEI).
	- Após criar o Sistema, acessar a funcionalidade de "Serviços" (desenho de engrenagem amarela), criar um novo serviço em "Novo", preencher os campos de Identificação e Descrição, selecionar o campo "Chave de Acesso" e salvar.
	- Na tela de Serviços do sistema recém criado, acessar o link de "Gerar Chave de Acesso" (símbolo de chave) - Após gerar a chave, anotar em local seguro para inserir na tela de "Configurações" do aplicativo. Recomenda-se não selecionar a opção "Gerar links de acesso externos" na tela de configuração do Serviço.
	- Essa configuração já permite a comunicação entre a aplicação e o SEI, porém ainda é necessário inserir as permissões que serão liberadas para realização pelo Gestão SEI. Para isso, acessar a opção "Operações" na tela de Serviços e incluir as operações em "Novo".
	- A operação mínima para funcionamento do Gestão SEI é a de "Bloquear Processo", sendo recomendável indicar apenas uma unidade (geralmente a unidade de protocolo, caso se trate de processos enviados externamente que não foram bloqueados automaticamente) e "Todos" na opção "Tipo do processo".
2. O "Gestão - SEI" valida o acesso dos usuários e permite o acesso apenas daqueles que possuem o perfil "Administrador" do Sistema SEI, devidamente cadastrado no SIP. Se houver mais de um perfil com o nome "Administrador", o sistema escolherá o primeiro, seguindo a ordem alfabética.
3. Foi inserida uma opção para desativar a validação do NUP para o bloqueio dos processos, de forma que seja possível bloquear processos antigos, mas também em ambientes de teste, em que o SEI não foi instalado com a máscara padrão do NUP.

## Orientações para desenvolvimento

O ambiente de desenvolvimento utiliza o framework nativo do Flask para rodar a aplicação, porém, conforme indicado na [documentação oficial](https://flask.palletsprojects.com/en/2.3.x/deploying/), não é recomendado o seu uso em produção, sendo necessário integrar um *WSGI Server* (Gunicorn, Waitress, mod_wsgi, etc).<br>
Como não é necessário subir outros frameworks ou aplicações (como nginx e servidores de BD), não é necessário utilizar containers, porém recomenda-se o uso de ambiente virtual do Python (venv, pyenv, etc), para que seja possível instalar e utilizar as dependências do projeto de forma isolada.<br>
Para facilitar a configuração do ambiente, com a criação do ambiente virtual, exclusão e recriação do BD em SQLite (apagar e recriar as tabelas), foi inserido um Makefile com essa parametrização.
Dessa forma, no caso de adotar algum outro módulo para criação de ambientes virtuais, diferente do venv, é importante ajustar o Makefile.</p>


### Pré-requisitos
- [Git](https://git-scm.com/)
- [venv](https://docs.python.org/pt-br/3/library/venv.html) # ou outra ferramenta de ambientes virtuais
- [Docker](https://www.docker.com/)
- [Docker-compose](https://docs.docker.com/compose/install/linux/)

- Make (Base debian: ```sudo apt-get install make``` ou ```sudo apt-get install build-essential```)

### Passos para configuração do ambiente de desenvolvimento (sem uso do Docker)

#### 1. Clonar o repositório na máquina de desenvolvimento local

O primeiro passo será clonar o repositório na máquina local de desenvolvimento. Isto pode ser feito através do comando:

```bash
git clone git@gitlab.mcom.gov.br:felipe.lustosa/gestao-sei.git
```

#### 2. Subir ambiente de desenvolvimento

Utilizando os comandos utilitários pré-configurados no Makefile, iremos inicializar o ambiente de desenvolvimento local virtualizado em containers docker através da execução do comando abaixo:

```bash
make init
make run
```

Para reconstruir a estrutura da base de dados, necessário somente se houver mudança na estrutura das tabelas, deverá ser executado o comando abaixo:

```bash
make restartdb
```

