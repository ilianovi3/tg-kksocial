#!/bin/bash

# Останавливаем выполнение при любой ошибке
set -e

echo "🚀 Начинаю процесс обновления..."

# Переходим в рабочую директорию
cd /srv/tg-kksocial

echo "🛑 Останавливаю контейнеры..."
docker-compose down

echo "📥 Обновляю tg-kksocial..."
git pull

echo "🛠 Собираю образы и запускаю сервисы..."
docker-compose build
docker-compose up -d

echo "✅ Обновление успешно завершено!"