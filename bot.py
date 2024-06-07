import telebot
from telebot import types

import schedule

from tag_consts import *
from bot_token import BOT_TOKEN
from db import ProblemsDataBase
from users import Users

bot = telebot.TeleBot(BOT_TOKEN)
db = ProblemsDataBase()

users = Users()


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # Adding buttons for each tag
    for tag in idTags.keys():
        button = telebot.types.InlineKeyboardButton(tag, callback_data=tag)
        keyboard.add(button)
    button = telebot.types.InlineKeyboardButton("random", callback_data="random")
    keyboard.add(button)
    bot.send_message(message.chat.id,
                     """Hello, I am a codeforces bot. 
    If you want to subscribe type `subscribe`/""",
                     reply_markup=keyboard,
                     parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call: types.CallbackQuery):
    chatId = call.message.chat.id

    if call.data in idTags.keys():
        problem = db.get_one_problem_by_tag(idTags.get(call.data))
        bot.send_message(chat_id=chatId, text=problem, parse_mode='Markdown')
        bot.answer_callback_query(call.id)
    elif call.data == "random":
        problem = db.get_random_problem()
        bot.send_message(chat_id=chatId, text=problem, parse_mode='Markdown')
        bot.answer_callback_query(call.id)


def send_daily(chatId: str, username: str):
    problem = db.get_random_problem()
    schedule.every().day.at("12:00").do(

        bot.send_message(
            chatId,
            f"""Hi, {username}, daily problem:
            {problem}"""
        )
    )


@bot.message_handler(commands=['subscribe'])
def subscribe_message(message: types.Message):
    """заносит пользователя в список и добавляет в таймер"""
    users.add_user(chatId=message.chat.id, username=message.from_user.username)
    send_daily(message.chat.id, message.from_user.username)
    bot.reply_to(message, "Scheduler started. Daily messages will be sent at 10:00 AM.")


if __name__ == '__main__':
    bot.infinity_polling()

    all_users = users.get_user_list()
    for user in all_users:
        send_daily(user.chat_id, user.username)
