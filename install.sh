#!/bin/bash

# Остановить скрипт при ошибке
set -e

echo "🚀 Начинаем установку окружения для бота..."

chmod +x start.sh
chmod +x stop.sh
chmod +x update.sh

# 1. Обновление системы
echo "🔄 Обновление пакетов..."
sudo apt update && sudo apt upgrade -y

# 2. Установка базовых зависимостей
echo "📦 Установка базовых утилит (curl, git, и т.д.)..."
sudo apt install -y curl git python3 python3-pip python3-venv apt-transport-https ca-certificates software-properties-common

# 3. Установка Docker
if ! command -v docker &> /dev/null
then
    echo "🐳 Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker установлен."
else
    echo "🐳 Docker уже установлен, пропускаем."
fi

# 4. Установка Docker Compose
echo "🛠 Установка Docker Compose..."
sudo apt install -y docker-compose-plugin
sudo apt install docker-compose -y

# 5. Установка Poetry
if ! command -v poetry &> /dev/null
then
    echo "📜 Установка Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    # Добавляем Poetry в PATH для текущей сессии
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "✅ Poetry установлен."
else
    echo "📜 Poetry уже установлен, пропускаем."
fi

echo "--------------------------------------------------"
echo "🎉 Установка завершена!"
echo "⚠️  ВАЖНО: Чтобы применить изменения прав Docker и путей Poetry,"
echo "   выполните команду: source ~/.bashrc"
echo "   или просто перезайдите на сервер по SSH."
echo "--------------------------------------------------"