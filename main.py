import os
import logging
import telebot

# Set up logging level
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Create bot object
bot = telebot.TeleBot('6077818884:AAFlRVcwF6lrkLcINmR1ZsRx0IR-6LsRJyw')

# Create command buttons for easy command input
new_pack_btn = telebot.types.KeyboardButton('/new_pack <имя стикерпака>')
add_sticker_btn = telebot.types.KeyboardButton('/add_sticker <имя стикерпака>')

# Create reply markup keyboard
reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
reply_markup.add(new_pack_btn, add_sticker_btn)


# Create command handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Привет! Я бот для создания стикер-паков. Чтобы создать новый стикер-пак, просто отправь мне стикеры!",
                     reply_markup=reply_markup)


@bot.message_handler(commands=['new_pack'])
def new_sticker_pack(message):
    try:
        # Get the name of the new sticker pack from the user
        name = message.text.split()[1]

        # Create a new sticker pack
        bot.create_new_sticker_set(user_id=message.from_user.id,
                                   name=name,
                                   title=name,
                                   emojis="🤖")

        # Send a message to the user
        bot.send_message(chat_id=message.chat.id, text=f"Стикер-пак {name} успешно создан!")

    except IndexError:
        # If the user did not provide a name for the new sticker pack, prompt them to do so
        bot.send_message(chat_id=message.chat.id,
                         text="Пожалуйста, укажите имя стикер-пака в следующем формате: /new_pack <имя стикерпака>")


@bot.message_handler(commands=['add_sticker'])
def add_sticker(message):
    try:
        # Get the name of the sticker pack from the user
        pack_name = message.text.split()[1]

        # Get the ID of the sticker the user sent
        sticker_id = message.sticker.file_id

        # Add the sticker to the sticker pack
        bot.add_sticker_to_set(user_id=message.from_user.id,
                               name=pack_name,
                               emojis="🤖",
                               png_sticker=sticker_id)

        # Send a message to the user
        bot.send_message(chat_id=message.chat.id, text="Стикер успешно добавлен в стикер-пак!")

    except IndexError:
        # If the user did not provide a name for the sticker pack, prompt them to do so
        bot.send_message(chat_id=message.chat.id,
                         text="Пожалуйста, укажите имя стикер-пака в следующем формате: /add_sticker <имя стикерпака>")

    except telebot.apihelper.ApiException as e:
        # If the sticker pack does not exist or the sticker could not be added to it, inform the user
        bot.send_message(chat_id=message.chat.id, text=f"Не удалось добавить стикер в стикер-пак: {e.description}")


# Start polling for new messages
bot.polling(none_stop=True)
