import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'SHOW_AUTHOR': True,
    'DELETE_ORIGINAL': True,
    'SHOW_PRETTY_LINK': True,
    'SEND_AS_REPLY': False,
    'attach_user_text': True,
    
    'REPLY_TEMPLATE': """{hidden_url_preview}
{user_message}

{pretty_url}
{author}"""
}

TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# group(1) - протокол, group(2) - поддомены, group(3) - опциональный kk, group(4) - домен, group(5) - путь
URL_PATTERN = re.compile(r'(?i)(?<!\w)(https?://)?((?:[\w-]+\.)*)(kk)?(instagram\.com|tiktok\.com)(\S*)')

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = URL_PATTERN.search(message.text)
    if not match:
        return

    raw_protocol = match.group(1)
    fixed_protocol = raw_protocol if raw_protocol else "https://"
    
    subdomains = match.group(2) if match.group(2) else ""
    # group(3) — это kk, нам оно не нужно при построении URL
    main_domain = match.group(4).lower()
    path = match.group(5) if match.group(5) else ""
    
    path_no_args = path.split("?")[0]

    # Превью-ссылка — всегда с kk
    hidden_url = f"{fixed_protocol}{subdomains}kk{main_domain}{path}"
    
    # Оригинальная ссылка — всегда без kk
    full_original_url = f"{fixed_protocol}{subdomains}{main_domain}{path}"
    
    # Красивый текст — без протокола и поддоменов
    pretty_link_text = f"{main_domain}{path_no_args}".rstrip("/")

    hidden_url_preview = f'<a href="{hidden_url}">&#8203;</a>'
    
    user_message = ""
    if CONFIG['attach_user_text']:
        user_message = URL_PATTERN.sub('', message.text).strip()
    
    pretty_url = ""
    if CONFIG['SHOW_PRETTY_LINK']:
        pretty_url = f'<a href="{full_original_url}">🔗 {pretty_link_text}</a>'
        
    author = ""
    if CONFIG['SHOW_AUTHOR'] and message.chat.type != 'private':
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
        author = f'<a href="tg://user?id={user.id}">👤 {full_name}</a>'

    final_text = CONFIG['REPLY_TEMPLATE'].format(
        hidden_url_preview=hidden_url_preview,
        user_message=user_message,
        pretty_url=pretty_url,
        author=author
    )

    final_text = final_text.replace("\n"*3, "\n"*2).strip().strip("\n")

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
    print(f"🚀 Бот запущен")
    bot.infinity_polling()