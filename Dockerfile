FROM python:3.10-slim-buster

WORKDIR /gestao-sei

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /gestao-sei

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
