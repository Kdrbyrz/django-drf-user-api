FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y netcat
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./docker-entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
