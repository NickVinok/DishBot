import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)


''''
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)
'''


@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Поехали", callback_data="test")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Привет! Я твой помощник в выборе блюда.", reply_markup=keyboard)

if __name__ == '__main__':
     bot.polling(none_stop=True)
