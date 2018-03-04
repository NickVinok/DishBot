import telebot
import config
import sqlite3
from telebot import types
from db_work import initiate_query

bot = telebot.TeleBot(token=config.TOKEN)

meal_time = ["Обед", "Завтрак", "Ужин", "Легко перекусить"]
diet = ["Детям", "Вегетарианская", "Низкоуглеводная", "Низкокалорийная", "Обычное"]
difficulty = ["Для новичка","Средней сложности","Сложное"]
cooking_method = ["В духовке", "Жарим", "Консервируем", "Варим"]
cooking_time = ["<45 мин", "45-120 мин", "120< мин"]
listOfChoises = ["", "","", "", ""]

@bot.message_handler(commands = ["start"])
def greetings(message):
    bot.send_message(message.chat.id, config.GREETING_MESSAGE)

@bot.message_handler(commands=["help"])
def instructions(message):
    bot.send_message(message.chat.id, config.INSTRUCTION_MESSAGE)

@bot.message_handler(commands=["go"])
def action(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*[types.KeyboardButton(meal) for meal in meal_time])
    markup.add("Мне повезёт")
    message = bot.send_message(message.chat.id,"Давай определимся с твоими предпочтениями на сегодня", reply_markup=markup)
    bot.register_next_step_handler(message, test)

def test(msg):
    if msg.text in meal_time:
        listOfChoises[0] = msg.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*[types.KeyboardButton(die) for die in diet])
        msg = bot.send_message(msg.chat.id,"а?", reply_markup=markup)
        bot.register_next_step_handler(msg, test)
    elif msg.text in diet:
        listOfChoises[1] = msg.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*[types.KeyboardButton(diff) for diff in difficulty])
        msg = bot.send_message(msg.chat.id,"а?", reply_markup=markup)
        bot.register_next_step_handler(msg, test)
    elif msg.text in difficulty:
        listOfChoises[2] =msg.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*[types.KeyboardButton(method) for method in cooking_method])
        msg = bot.send_message(msg.chat.id,"а?", reply_markup=markup)
        bot.register_next_step_handler(msg, test)
    elif msg.text in cooking_method:
        listOfChoises[3] = msg.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*[types.KeyboardButton(time) for time in cooking_time])
        msg = bot.send_message(msg.chat.id,"а?", reply_markup=markup)
        bot.register_next_step_handler(msg, test)
    elif msg.text in cooking_time:
        listOfChoises[4] = msg.text
        result = initiate_query(listOfChoises)
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Вот твой рецепт", url=result[1])
        keyboard.add(url_button)
        bot.send_message(msg.chat.id, result[0], reply_markup=keyboard)
        bot.send_message(msg.chat.id, "Bon Appetit")




if __name__ == '__main__':
    bot.polling(none_stop = True)
