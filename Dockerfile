# Образ микросервиса приложения «Студия танцев» (Flask + SQLite)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала только зависимости — этот слой кэшируется и не пересобирается без изменения requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Затем исходный код приложения и тесты
COPY . .

# Приложение работает не от root (требование безопасности контейнеров)
RUN useradd --create-home appuser \
    && mkdir -p /app/instance \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Docker сам проверяет, что приложение отвечает на /health
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=5 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)" || exit 1

# gunicorn — промышленный WSGI-сервер вместо встроенного сервера Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "run:app"]
