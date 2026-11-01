FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ /app/server/
WORKDIR /app/server

EXPOSE 8000
# start.sh: makemigrations -> migrate -> seed sample data -> collectstatic -> gunicorn
CMD ["sh", "start.sh"]
