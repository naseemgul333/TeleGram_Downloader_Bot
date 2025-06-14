import os, json
import telebot

BOT_TOKEN = os.getenv('7999780412:AAHUJK--461tTUtKdtRBmZNG9jDlGGtbjvM')
bot = telebot.TeleBot(BOT_TOKEN)

with open('users.json', 'r') as f:
    users = json.load(f)

MESSAGE = """📢 Update from the bot owner!

Follow our new channel @YourChannelName 🔔
"""

for uid in users:
    try:
        bot.send_message(uid, MESSAGE)
    except Exception:
        pass
