import telebot
from telebot import types

from tag_consts import *
from bot_token import BOT_TOKEN
from db import ProblemsDataBase


bot=telebot.TeleBot(BOT_TOKEN)
db = ProblemsDataBase()


@bot.message_handler(commands=['start'])
def start_message(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  # Adding buttons for each tag
  for tag in idTags.keys():
      button = telebot.types.InlineKeyboardButton(tag, callback_data=tag)
      keyboard.add(button)
  bot.send_message(message.chat.id, "Привет ✌️ ", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call: types.CallbackQuery):
    chatId = call.message.chat.id

    if call.data in idTags.keys():
        problem = db.get_one_problem_by_tag(idTags.get(call.data))
        bot.send_message(chat_id=chatId, text=problem, parse_mode='Markdown')
        bot.answer_callback_query(call.id)
   
bot.infinity_polling()