import os
import json
import telebot
from telebot import types
import yt_dlp

BOT_TOKEN = os.getenv('7999780412:AAHUJK--461tTUtKdtRBmZNG9jDlGGtbjvM')
bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = 'users.json'
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = []

def save_user(chat_id):
    if chat_id not in users:
        users.append(chat_id)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)

@bot.message_handler(commands=['start'])
def cmd_start(m):
    save_user(m.chat.id)
    bot.send_message(m.chat.id, "👋 Send me a YouTube, Facebook, or Instagram video link and I'll give you download options.")

@bot.message_handler(func=lambda m: True)
def handle_url(m):
    save_user(m.chat.id)
    url = m.text.strip()
    bot.send_message(m.chat.id, "⏳ Retrieving info...")

    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get('title', 'Video')
        formats = info.get('formats', [])
        markup = types.InlineKeyboardMarkup()

        seen = set()
        for f in formats:
            if f.get('ext') == 'mp4' and f.get('format_note') not in seen:
                seen.add(f.get('format_note'))
                markup.add(types.InlineKeyboardButton(
                    text=f"MP4 {f.get('format_note')}",
                    url=f.get('url')
                ))
        for f in formats:
            if f.get('acodec') != 'none' and f.get('ext') in ('m4a', 'mp3'):
                markup.add(types.InlineKeyboardButton(
                    text="🎵 Download MP3",
                    url=f.get('url')
                ))
                break

        bot.send_message(m.chat.id, f"🎬 *{title}*
Choose a format:", reply_markup=markup, parse_mode='Markdown')

    except Exception as e:
        bot.send_message(m.chat.id, f"❌ Error: {e}")

bot.infinity_polling()
