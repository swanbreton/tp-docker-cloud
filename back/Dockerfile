FROM python:3.11-alpine

RUN apk update && apk add --no-cache curl

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]