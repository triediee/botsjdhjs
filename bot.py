import os
import threading
from flask import Flask
import telebot
from google import genai

# Инициализируем мини-сервер для Render, чтобы он не ругался на порты
app = Flask(__name__)

@app.route('/')
def home():
    return "Jarvis is online and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Получаем ключи
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = (
    "Ты — Джарвис, продвинутый персональный ИИ-ассистент. "
    "Твоя задача — четко, грамотно и эффективно помогать пользователю во всем, "
    "решать его задачи и отвечать на вопросы. Общайся в уверенном и полезном стиле."
)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro-002',
            contents=message.text,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
            },
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Сэр, произошла ошибка в системе: {e}")

if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке, чтобы он занимал порт для Render
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    print("Джарвис запущен...")
    bot.infinity_polling()
