import telebot

from tag_consts import *
from bot_token import BOT_TOKEN
from db import ProblemsDataBase


bot=telebot.TeleBot(BOT_TOKEN)
db = ProblemsDataBase()


@bot.message_handler(commands=['start'])
def start_message(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  button1 = telebot.types.InlineKeyboardButton(text=IMPLEMENTATION, callback_data=IMPLEMENTATION)
  button2 = telebot.types.InlineKeyboardButton(text=MATH, callback_data=MATH)
  keyboard.add(button1, button2)
  bot.send_message(message.chat.id, "Привет ✌️ ", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == IMPLEMENTATION:
        problem = db.get_one_problem_by_tag(idTags.get(IMPLEMENTATION))
        bot.answer_callback_query(callback_query_id=call.id, text=problem, show_alert=False)
    elif call.data == MATH:
        problem = db.get_one_problem_by_tag(2)
        bot.answer_callback_query(callback_query_id=call.id, text=problem)
  
bot.infinity_polling()