import telebot

token='наш токен'
bot=telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")

  
bot.infinity_poling()