FROM python:3.11.1-slim

EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y postgresql-client 
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y netcat 
RUN apt-get clean

RUN mkdir /fastapi
WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /fastapi

CMD [ "python3", "main.py" ]