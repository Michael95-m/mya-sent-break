# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm -rf /root/.cache

COPY . .

RUN chmod +x ./startup.sh

CMD ["./startup.sh"]
