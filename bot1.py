import telebot
from telebot import types
from text_info import button_text, bot_message, img_url, chat_message
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_API_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
target_chat = os.getenv("CHAT")

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton(button_text.get('start'))
    markup.add(start_button)


    # приветсвенное сообщение для команды /start
    #bot.send_message(message.chat.id, text=bot_message.get('greeting').format(message.from_user), reply_markup=markup)
    #bot.send_photo(message.chat.id, photo=open(img_url.get('bot_logo'), 'rb'), caption=bot_message.get('greeting'))
    # Сначала форматируем строку с именем пользователя
    formatted_greeting = bot_message['greeting'].format(message.from_user)

    # Затем передаем отформатированную строку в качестве параметра caption
    bot.send_photo(
        message.chat.id,
        photo=open(img_url.get('bot_logo'), 'rb'),
        caption=formatted_greeting,
        reply_markup=markup  # <---- Здесь должно быть указано ваше меню-клавиатура
    )



@bot.message_handler(commands=['show_buttons'])
def show_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    hi_button = types.KeyboardButton(button_text.get('acquaintance'))
    send_msg = types.KeyboardButton("Оставить заявку")
    markup.add(hi_button)
    markup.add(send_msg)

    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id, "/start - Начальное сообщение")
    bot.send_message(message.chat.id, "/show_buttons - Кнопки: Ремонт смартфонов, оставить заявку")

# Обработчик нажатия на кнопку
@bot.message_handler(commands=['check'])
def handle_button_click(message):
    # Отправляем сообщение с предложением ввести текст
    bot.send_message(message.chat.id, 'Я передам ваше сообщение. Просто введите сообщение, которое хотите отправить:')

# Обработчик ввода сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Копируем сообщение
    bot.forward_message(chat_id=target_chat, from_chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler(content_types=['text'])
def button(message):
    if message.text == button_text.get('start'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        hi_button = types.KeyboardButton(button_text.get('acquaintance'))
        send_msg = types.KeyboardButton("Оставить заявку")
        markup.add(hi_button)
        markup.add(send_msg)

        bot.send_message(message.chat.id, bot_message.get('what_you_want'), reply_markup=markup)

    elif message.text == button_text.get('acquaintance'):
        bot.send_message(message.chat.id,
                         text=chat_message.get('hi_message'))

    elif message.text == 'Оставить заявку':
        bot.send_message(message.chat.id, 'В разработке')


bot.polling(none_stop=True, interval=0)