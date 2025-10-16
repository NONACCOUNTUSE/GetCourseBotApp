// Конфигурация
const API_BASE_URL = 'https://your-app.onrender.com'; // ЗАМЕНИТЕ на ваш Render URL

// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;

// Элементы интерфейса
const statusElement = document.getElementById('status');
const logsElement = document.getElementById('logs');

// Инициализация
tg.expand();
tg.ready();

// Функция отправки команды
async function sendCommand(command) {
    showStatus('⏳ Выполняю команду...');
    addLog(`➡️ Отправка: ${command}`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                command: command,
                user_id: tg.initDataUnsafe.user?.id || 'unknown'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus('✅ ' + data.message);
            addLog(`✅ Успех: ${data.message}`);
        } else {
            showStatus('❌ ' + data.message);
            addLog(`❌ Ошибка: ${data.message}`);
        }
    } catch (error) {
        showStatus('❌ Ошибка соединения');
        addLog(`❌ Сеть: ${error.message}`);
    }
}

// Вспомогательные функции
function showStatus(message) {
    statusElement.textContent = message;
}

function addLog(message) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logsElement.appendChild(logEntry);
    logsElement.scrollTop = logsElement.scrollHeight;
}

// Обработчики кнопок (уже есть в HTML)