import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
CONFIG = {
    'SHOW_AUTHOR': True,         # Показывать имя отправителя в группах
    'DELETE_ORIGINAL': True,     # Удалять сообщение пользователя
    'SHOW_PRETTY_LINK': True,    # Отображать текстовую ссылку под превью
    'SEND_AS_REPLY': False       # Отправлять как ответ (reply) на сообщение
}

TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TG_BOT_TOKEN not found in .env")

bot = telebot.TeleBot(TOKEN)

# Оптимизированный паттерн
URL_PATTERN = re.compile(r'(https?://)?((?:[\w-]+\.)*)(instagram\.com|tiktok\.com)(\S*)')

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = URL_PATTERN.search(message.text)
    if not match:
        return

    # Разбор ссылки
    protocol = match.group(1) if match.group(1) else "https://"
    subdomains = match.group(2) if match.group(2) else ""
    main_domain = match.group(3)
    path = match.group(4) if match.group(4) else ""
    
    path_no_args = path.split("?")[0]

    # Формируем компоненты
    hidden_url = f"{protocol}{subdomains}kk{main_domain}{path}"
    full_original_url = f"{protocol}{subdomains}{main_domain}{path}"
    pretty_url = f"{protocol}{subdomains}{main_domain}{path_no_args}".rstrip("/")
    
    # --- Сборка сообщения ---
    # 1. Скрытая ссылка для превью (всегда есть)
    reply_text = f'<a href="{hidden_url}">&#8203;</a>'
    
    # 2. Добавляем имя, если это группа и настройка включена
    is_private = message.chat.type == 'private'
    author_part = ""
    if not is_private and CONFIG['SHOW_AUTHOR']:
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
        author_part = f'<a href="tg://user?id={user.id}">@{full_name}</a>'

    # 3. Добавляем ссылку, если включено
    link_part = ""
    if CONFIG['SHOW_PRETTY_LINK']:
        link_part = f'<a href="{full_original_url}">{pretty_url}</a>'

    # Собираем части вместе
    if author_part and link_part:
        reply_text += f"{link_part}\n\n{author_part}"
    else:
        reply_text += author_part + link_part
    
    if not CONFIG['SHOW_AUTHOR'] and not CONFIG['SHOW_PRETTY_LINK']:
        reply_text += "."

    print(reply_text)

    # Определяем, отвечать реплаем или нет
    reply_to = message.message_id if CONFIG['SEND_AS_REPLY'] else None

    # Отправка
    bot.send_message(
        chat_id=message.chat.id,
        text=reply_text,
        parse_mode='HTML',
        reply_to_message_id=reply_to
    )
    
    # Удаление оригинала (с проверкой конфига)
    if CONFIG['DELETE_ORIGINAL']:
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            print(f"Log: Could not delete message. {e}")

if __name__ == '__main__':
    print(f"🚀 Бот запущен с конфигом: {CONFIG}")
    bot.infinity_polling()