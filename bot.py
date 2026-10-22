import os
import telebot
from google import genai

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
            model='gemini-3.8-flash',
            contents=message.text,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
            },
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Сэр, произошла ошибка в системе: {e}")

if __name__ == "__main__":
    print("Джарвис запущен...")
    bot.infinity_polling()
