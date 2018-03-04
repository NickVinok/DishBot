import telebot
import config
import sqlite3
from telebot import types

bot = telebot.TeleBot(token=config.TOKEN)

"""
@bot.message_handler(content_types=["text"])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(url_button)
    bot.send_message(message.chat.id,
     "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)
"""
@bot.message_handler(commands = ["start"])
def greetings(message):
    bot.send_message(message.chat.id, config.GREETING_MESSAGE)

@bot.message_handler(commands=["help"])
def instructions(message):
    bot.send_message(message.chat.id, config.INSTRUCTION_MESSAGE)

@bot.message_handler(commands=["go"])
def action(message):
    bot.send_message(message.chat.id, "Здесь начнётся основная программа")

if __name__ == '__main__':
    bot.polling(none_stop = True)
