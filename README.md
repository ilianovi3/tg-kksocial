# 🚀 TG KKSOCIAL

Telegram-бот на базе `pyTelegramBotAPI`, который автоматически исправляет ссылки **Instagram** и **TikTok**, добавляя префикс `kk` к домену. Это позволяет корректно отображать предпросмотр видео в Telegram.

## ✨ Функции
- **Авто-замена:** `instagram.com` -> `kkinstagram.com`, `tiktok.com` -> `kktiktok.com`.
- **Чистый чат:** Бот удаляет исходное сообщение пользователя после замены.
- **Упоминание:** Бот тегает пользователя, приславшего ссылку.
- **Docker-ready:** Полная поддержка развертывания через Docker и Docker Compose.

## 🛠 Технологии
- [Python 3.11+](https://www.python.org/)
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Poetry](https://python-poetry.org/) (управление зависимостями)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Быстрый старт
### Установка
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git
cd /srv
git clone https://github.com/ilianovi3/tg-kksocial tg-kksocial
cd tg-kksocial
chmod +x install.sh
./install.sh
cp .env.example .env
```

### Запуск
```bash
docker-compose up -d
```