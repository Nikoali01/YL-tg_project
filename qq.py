import random
import logging
import telebot
from telebot import types
from database import dbworker

#нужные переменные, настройки
full_amount = 0
bot = telebot.TeleBot('1796084805:AAGjrMJCKVF-rqFVKJlC7yeu4Kv8sNrfm9k')
ids = set()
global state
state = "inactive"
tokens = "8%231"
db = dbworker('db.db')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
NICKNAME, MAIN = range(2)

#кнопочки в начале
def TypeOfAction():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = types.KeyboardButton(text="Вступить в чат")
    keyboard.add(button_1)
    button_2 = types.KeyboardButton(text="Создать чат")
    keyboard.add(button_2)
    return keyboard

#хэндлер команды /start
@bot.message_handler(commands=['start'])
def start(message):
    db.exit(message.from_user.id)
    bot.send_message(message.chat.id,
                     'Приветствую, этот бот создаёт чаты для общения.\nДля того, чтобы ваши друзья смогли узнать вас, поменяйте свой ник в Телеграм.\nНиже выберите тип действий.',
                     reply_markup=TypeOfAction())
    telegram_id = message.from_user.id
    db.user(telegram_id)

#хэндлер текста
@bot.message_handler(content_types=['text'])
def getting_tok(message):
    if message.text == "Удалить бд":
        db.delliting()
    elif message.text == "Выйти из чата":
        ah = db.getting_chat(message.from_user.id)
        ah = ah[0]
        spis1 = db.getting_connected(ah)
        for i in range(len(spis1)):
            if message.from_user.id != spis1[i]:
                bot.send_message(spis1[i], f"Пользователь '{message.from_user.id}' покинул чат.")
        db.exit(message.from_user.id)
        bot.send_message(message.chat.id, "Вы успешно покинули чат")
    elif message.text == "Вступить в чат":
        bot.send_message(message.chat.id, "Введите уникальный токен")
    elif message.text == "Создать чат":
        bot.send_message(message.chat.id, "Создание...")
        telegram_id = message.from_user.id
        new_chat_id = random.randint(1, 10000)
        while True:
            if db.chat_exists(new_chat_id):
                new_chat_id = random.randint(1, 10000)
            else:
                telegram_id = message.from_user.id
                chat_id = new_chat_id
                db.add_chat(telegram_id, chat_id)

                bot.send_message(message.chat.id, f"Токен вашего чата: {new_chat_id}, сообщите его друзьям.")
                break

    else:
        if message.text.isdigit():
            telegram_id = message.from_user.id
            if db.chat_exists(int(message.text)) and (not db.getting_act(telegram_id)):
                print('ex')
                bot.send_message(message.chat.id, "Осуществляется вход, подождите немного...")
                telegram_id = message.from_user.id
                db.giving_activity(telegram_id, int(message.text))
                print(1)
                ah = db.getting_chat(message.from_user.id)
                ah = ah[0]
                spis1 = db.getting_connected(ah)
                for i in range(len(spis1)):
                    if message.from_user.id != spis1[i]:
                        bot.send_message(spis1[i], f"Пользователь '{message.from_user.id}' присоединился к чату")
                bot.send_message(message.chat.id, "Вы успешно присоединились к чату!")
            elif db.getting_act(telegram_id):
                bot.send_message(message.chat.id, "Вы уже состоите в чате")
            else:
                bot.send_message(message.chat.id, "Чат с таким токеном не найден!")
        else:
            ah = db.getting_chat(message.from_user.id)
            ah = ah[0]
            spis1 = db.getting_connected(ah)
            for i in range(len(spis1)):
                if message.from_user.id != spis1[i]:
                    bot.send_message(spis1[i], f"{message.from_user.first_name}: {message.text}")

#работа бота
bot.polling()
