import telebot
import requests
import time
from telebot import types

BOT_TOKEN = "8605809944:AAFX_9TlV2CBfISMpAZJrtR25kU1DB2uIP4"
TMDB_API_KEY = "2df7966b11c2fa17ff9606fd8eb710fb"
VERCEL_SITE_URL = "https://movie-bott-five.vercel.app/"

bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.set_chat_menu_button(
        menu_button=types.MenuButtonWebApp(
            type="web_app",
            text="SaraFlix 🍿",
            web_app=types.WebAppInfo(url=VERCEL_SITE_URL)
        )
    )
except:
    pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 **SaraFlix** 🍿\n\nSend me any movie or series name!", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def search_media(message):
    query = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    
    try:
        response = requests.get(url).json()
        results = response.get("results", [])
        if not results:
            bot.reply_to(message, "❌ No results found!")
            return

        valid = [r for r in results if r.get("media_type") in ["movie", "tv"]][:3]
        if not valid:
            bot.reply_to(message, "❌ No matched movies or series.")
            return

        for media in valid:
            media_id = media["id"]
            media_type = media["media_type"]
            title = media.get("title") or media.get("name")
            overview = media.get("overview")

            if not overview or overview == "":
                detail_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}?api_key={TMDB_API_KEY}&language=en"
                details = requests.get(detail_url).json()
                overview = details.get('overview', "No overview available.")

            poster = media.get("poster_path")
            watch_url = f"{VERCEL_SITE_URL}watch.html?id={media_id}&type={media_type}"

            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("🎬 Watch Now", url=watch_url))

            type_label = "🎬 Movie" if media_type == "movie" else "📺 Series"
            text = f"{type_label}: **{title}**\n\n📝 **Story:** {overview}"

            if poster:
                img = f"https://image.tmdb.org/t/p/w500{poster}"
                bot.send_photo(message.chat.id, img, caption=text, reply_markup=kb, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Error, try again later.")

print("Bot is running...")
while True:
    try:
        bot.infinity_polling()
    except:
        time.sleep(5)
