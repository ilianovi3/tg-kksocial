import os
import re
import telebot
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TG_BOT_TOKEN не найден в .env")

bot = telebot.TeleBot(TOKEN)

# Регулярное выражение для поиска доменов
PATTERN = r'(https?://)?(?:www\.)?(instagram\.com|tiktok\.com)(\S*)'

@bot.message_handler(content_types=['text'])
def replace_links(message):
    match = re.search(PATTERN, message.text)
    
    if match:
        # Разбор ссылки
        protocol = match.group(1) if match.group(1) else "https://"
        domain = match.group(2)
        path = match.group(3) if match.group(3) else ""
        
        new_url = f"{protocol}kk{domain}{path}"
        
        # Получаем имя и фамилию
        user = message.from_user
        first_name = user.first_name
        last_name = user.last_name if user.last_name else ""
        
        # Формируем полное имя (убираем лишние пробелы, если фамилии нет)
        full_name = f"{first_name} {last_name}".strip()
        
        # Создаем упоминание в виде ссылки по ID пользователя
        # Это сработает как гиперссылка на профиль
        user_link = f'<a href="tg://user?id={user.id}">@{full_name}</a>'
        
        # Итоговый текст сообщения
        reply_text = f"{new_url}\n\n{user_link}"
        
        # Отправка нового сообщения
        bot.send_message(
            chat_id=message.chat.id,
            text=reply_text,
            parse_mode='HTML',
            disable_web_page_preview=False
        )
        
        # Удаление старого сообщения
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")


if __name__ == '__main__':
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()
