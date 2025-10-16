from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от любых источников

# Глобальный словарь для хранения сессий пользователей
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.bot = None
        self.logs = []
    
    def add_log(self, message):
        self.logs.append(message)
        if len(self.logs) > 50:  # Ограничиваем логи
            self.logs.pop(0)
    
    def initialize_bot(self):
        """Инициализация бота для пользователя"""
        try:
            # Импортируем здесь чтобы избежать проблем с зависимостями
            from playwright.sync_api import sync_playwright
            from colorama import init, Fore
            
            init(autoreset=True)
            
            self.bot = type('Bot', (), {})()  # Заглушка - замените на ваш реальный бот
            
            self.add_log("🤖 Бот инициализирован")
            return True
        except Exception as e:
            self.add_log(f"❌ Ошибка инициализации: {str(e)}")
            return False

def get_user_session(user_id):
    """Получаем или создаем сессию пользователя"""
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
        user_sessions[user_id].initialize_bot()
    return user_sessions[user_id]

@app.route('/')
def home():
    return jsonify({"message": "GetCourse Bot API", "status": "running"})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "sessions": len(user_sessions)})

@app.route('/api/command', methods=['POST'])
def handle_command():
    try:
        data = request.get_json()
        command = data.get('command')
        user_id = data.get('user_id', 'default')
        
        logger.info(f"Command received: {command} from user: {user_id}")
        
        user_session = get_user_session(user_id)
        user_session.add_log(f"Команда: {command}")
        
        # Обработка команд
        if command == 'go_main':
            user_session.add_log("Переход на главную страницу")
            return jsonify({"success": True, "message": "Перешли на главную страницу"})
        
        elif command == 'login':
            user_session.add_log("Попытка входа в систему")
            return jsonify({"success": True, "message": "Запрос на вход отправлен"})
        
        elif command == 'toggle_monitor':
            user_session.add_log("Переключение авто-ответов")
            return jsonify({"success": True, "message": "Авто-ответы переключены"})
        
        elif command == 'take_screenshot':
            user_session.add_log("Скриншот сделан")
            return jsonify({"success": True, "message": "Скриншот сохранен"})
        
        elif command == 'show_links':
            user_session.add_log("Запрос списка ссылок")
            return jsonify({"success": True, "message": "Ссылки показаны"})
        
        elif command == 'show_buttons':
            user_session.add_log("Запрос списка кнопок")
            return jsonify({"success": True, "message": "Кнопки показаны"})
        
        else:
            return jsonify({"success": False, "message": f"Неизвестная команда: {command}"})
            
    except Exception as e:
        logger.error(f"Error handling command: {str(e)}")
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})

@app.route('/api/logs/<user_id>')
def get_logs(user_id):
    user_session = get_user_session(user_id)
    return jsonify({"logs": user_session.logs})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)