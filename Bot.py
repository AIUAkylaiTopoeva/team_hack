import  telebot
from Token import token
from telebot import types

bot = telebot.Telebot(token)

inline_keyboard = types.InlineKeyboardMarkup()

# inline_keyboard =telebot.types.InlineKeyboardMarkup
# buttons  ={}
# for i in range(1, 5):
#     buttons['btn'+str(i)] = telebot.types.InlineKeyboardMarkup(str(i), callback_data=str(i))
#     inline_keyboard.add(buttons['btn'+str(i)])

@bot.meesage_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    btn1 = types.InlineKeyboardButton('последние 10 песни', callback_data='music')



