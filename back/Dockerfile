FROM python:3.11-alpine

RUN apk update && apk add --no-cache curl

WORKDIR /app

RUN pip install --no-cache-dir flask flask-cors

COPY game_data.py .
COPY app.py .

CMD ["python", "app.py"]