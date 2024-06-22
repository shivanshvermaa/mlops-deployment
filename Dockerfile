FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY ./fastapi-logs /fastapi-logs
# Uncomment if building locally
# COPY .env /app/.env

# ENV ENV_FILE_PATH /app/.env