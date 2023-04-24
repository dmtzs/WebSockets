FROM python:3.10

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "websocket.py"]