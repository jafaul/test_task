FROM python:3.12.8-slim

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir --force-reinstall -r requirements.txt psycopg2-binary && \
    pip uninstall redis -y && \
    pip install --no-cache-dir redis

EXPOSE 8000
