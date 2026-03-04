import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
CONFIG = {
    'SHOW_AUTHOR': True,         # Показывать имя отправителя
    'DELETE_ORIGINAL': True,     # Удалять сообщение пользователя
    'SHOW_PRETTY_LINK': True,    # Отображать текстовую ссылку
    'SEND_AS_REPLY': False,      # Отправлять как ответ
    'attach_user_text': True,    # Извлекать текст пользователя без ссылок
    
    # ШАБЛОН ОТВЕТА
    # {hidden_url_preview} - невидимая ссылка для генерации превью
    # {user_message}       - очищенный текст пользователя
    # {pretty_url}         - кликабельная ссылка
    # {author}             - ссылка на автора
    'REPLY_TEMPLATE': """{hidden_url_preview}
{user_message}
{pretty_url}
{author}"""
}

TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TG_BOT_TOKEN not found in .env")

bot = telebot.TeleBot(TOKEN)

# Паттерн для поиска ссылок
URL_PATTERN = re.compile(r'(https?://)?((?:[\w-]+\.)*)(instagram\.com|tiktok\.com)(\S*)')

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = URL_PATTERN.search(message.text)
    if not match:
        return

    # 1. Разбор ссылки для формирования компонентов
    protocol = match.group(1) if match.group(1) else "https://"
    subdomains = match.group(2) if match.group(2) else ""
    main_domain = match.group(3)
    path = match.group(4) if match.group(4) else ""
    
    path_no_args = path.split("?")[0]
    hidden_url = f"{protocol}{subdomains}kk{main_domain}{path}"
    full_original_url = f"{protocol}{subdomains}{main_domain}{path}"
    pretty_link_text = f"{protocol}{subdomains}{main_domain}{path_no_args}".rstrip("/")

    # 2. Подготовка данных для шаблона
    
    # Скрытая ссылка (пробел нулевой ширины)
    hidden_url_preview = f'<a href="{hidden_url}">&#8203;</a>'
    
    # Текст пользователя (удаляем ссылки и лишние пробелы)
    user_message = ""
    if CONFIG['attach_user_text']:
        user_message = URL_PATTERN.sub('', message.text).strip()
    
    # Красивая ссылка
    pretty_url = ""
    if CONFIG['SHOW_PRETTY_LINK']:
        pretty_url = f'<a href="{full_original_url}">🔗 {pretty_link_text}</a>'
        
    # Автор
    author = ""
    if CONFIG['SHOW_AUTHOR'] and message.chat.type != 'private':
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
        author = f'<a href="tg://user?id={user.id}">👤 {full_name}</a>'

    # 3. Сборка финального текста по шаблону
    final_text = CONFIG['REPLY_TEMPLATE'].format(
        hidden_url_preview=hidden_url_preview,
        user_message=user_message,
        pretty_url=pretty_url,
        author=author
    )

    # Умная очистка: убираем лишние пустые строки, если какие-то поля оказались пустыми
    # Но сохраняем невидимый символ превью
    lines = [line.strip() for line in final_text.splitlines() if line.strip() or '&#8203;' in line]
    final_text = "\n".join(lines)

    # 4. Отправка и удаление
    reply_to = message.message_id if CONFIG['SEND_AS_REPLY'] else None
    
    try:
        bot.send_message(
            chat_id=message.chat.id,
            text=final_text,
            parse_mode='HTML',
            reply_to_message_id=reply_to
        )
        
        if CONFIG['DELETE_ORIGINAL']:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print(f"🚀 Бот запущен. Шаблон активен.")
    bot.infinity_polling()