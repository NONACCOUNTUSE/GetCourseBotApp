import os
import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')  # Получите у @BotFather
WEB_APP_URL = "https://your-username.github.io/telegram-bot"  # ЗАМЕНИТЕ на ваш GitHub Pages URL

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

def create_main_keyboard():
    """Создаем клавиатуру с кнопкой Web App"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_btn = KeyboardButton(
        text="🎮 Открыть контроллер", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(web_app_btn)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Обработчик команды /start"""
    welcome_text = """
🤖 GetCourse Auto-Bot Controller

Привет! Я помогу автоматизировать работу с GetCourse.

🎯 Возможности:
• Автоматический вход в систему
• Авто-ответы на тесты  
• Управление через удобный интерфейс

Нажмите кнопку ниже чтобы открыть контроллер управления:
"""
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_main_keyboard()
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    """Обработка данных из Web App"""
    try:
        data = message.web_app_data.data
        user_id = message.from_user.id
        
        bot.send_message(
            message.chat.id,
            f"📱 Получена команда из Web App: {data}"
        )
        
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка обработки команды: {str(e)}"
        )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработка всех остальных сообщений"""
    if message.text == "🎮 Открыть контроллер":
        bot.send_message(
            message.chat.id,
            "Нажмите на кнопку ниже чтобы открыть контроллер:",
            reply_markup=create_main_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Используйте /start для начала работы или нажмите кнопку контроллера 👇",
            reply_markup=create_main_keyboard()
        )

if __name__ == "__main__":
    print("🤖 Telegram Bot запущен!")
    print(f"🌐 Web App URL: {WEB_APP_URL}")
    bot.infinity_polling()