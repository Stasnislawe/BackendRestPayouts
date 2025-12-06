FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python зависимости напрямую через pip
COPY pyproject.toml .

# Устанавливаем зависимости без Poetry
RUN pip install --no-cache-dir \
    django==4.2 \
    djangorestframework \
    celery[redis] \
    psycopg2-binary \
    python-dotenv \
    drf-spectacular \
    eventlet

# Копируем весь проект
COPY . .

# Создаем пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]