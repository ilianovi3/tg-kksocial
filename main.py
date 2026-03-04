import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

PATTERN = r'(https?://)?(?:www\.)?(instagram\.com|tiktok\.com)(\S*)'

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = re.search(PATTERN, message.text)
    if not match:
        return

    protocol = match.group(1) if match.group(1) else "https://"
    domain = match.group(2)
    path = match.group(3) if match.group(3) else ""
    
    # Ссылка, которую мы "прячем" для превью
    hidden_url = f"{protocol}kk{domain}{path}"
    
    user = message.from_user
    full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
    
    # Собираем магическое сообщение:
    # 1. Невидимая ссылка в самом начале (важно для превью)
    # 2. Имя пользователя как ссылка на профиль
    reply_text = (
        f'<a href="{hidden_url}">&#8203;</a>'  # Невидимый символ со ссылкой
        f'<a href="tg://user?id={user.id}">{full_name}</a>'
    )
    
    bot.send_message(
        chat_id=message.chat.id,
        text=reply_text,
        parse_mode='HTML',
        disable_web_page_preview=False # Обязательно False, чтобы превью работало
    )
    
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Ошибка удаления: {e}")

if __name__ == '__main__':
    bot.infinity_polling()