import os
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

VERCEL_URL = "https://movie-bott-five.vercel.app"

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(
            "🎬 شاهد الفيلم",
            url=f"{VERCEL_URL}"
        )
    )

    bot.send_message(
        message.chat.id,
        "🎬 أهلا بيك في Movie Bot",
        reply_markup=kb
    )

bot.polling()
