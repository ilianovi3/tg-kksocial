import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Новое регулярное выражение:
# (https?://)?      - протокол (группа 1)
# ([\w-]+\.)* - любые поддомены, например 'vt.', 'www.' (группа 2)
# (instagram\.com|tiktok\.com) - основной домен (группа 3)
# (\S*)             - путь и аргументы (группа 4)
PATTERN = r'(https?://)?([\w-]+\.)*(instagram\.com|tiktok\.com)(\S*)'

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = re.search(PATTERN, message.text)
    if not match:
        return

    protocol = match.group(1) if match.group(1) else "https://"
    subdomains = match.group(2) if match.group(2) else "" # Например, "vt."
    main_domain = match.group(3) # "tiktok.com"
    path = match.group(4) if match.group(4) else ""
    
    # Очистка пути от query-параметров для визуальной ссылки
    path_no_args = path.split("?")[0]

    # Ссылка для отображения (с поддоменом, без аргументов)
    pretty_url = f"{protocol}{subdomains}{main_domain}{path_no_args}"
    
    # Полная оригинальная ссылка (для клика)
    full_original_url = f"{protocol}{subdomains}{main_domain}{path}"
    
    # Ссылка для превью (kk вставляется ПЕРЕД основным доменом)
    # Получится https://vt.kktiktok.com/...
    hidden_url = f"{protocol}{subdomains}kk{main_domain}{path}"
    
    # Сборка сообщения
    reply_text = f'<a href="{hidden_url}">&#8203;</a>'
    reply_text += f'<a href="{full_original_url}">{pretty_url}</a>'
    
    if message.chat.type != 'private':
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
        reply_text += f'\n<a href="tg://user?id={user.id}">@{full_name}</a>'
    
    
    bot.send_message(
        chat_id=message.chat.id,
        text=reply_text,
        parse_mode='HTML'
    )
    
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Ошибка удаления: {e}")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()