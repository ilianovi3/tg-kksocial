# --- ЭТАП 1: Сборка зависимостей ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Устанавливаем только самое необходимое для установки пакетов
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости в системный путь (внутри образа)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

# --- ЭТАП 2: Финальный образ ---
FROM python:3.12-slim

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . ./

CMD ["python", "main.py"]