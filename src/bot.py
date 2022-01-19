import urllib.request
import redis
import re
import pandas as pd
import locale
from datetime import datetime
import telebot
from telebot import types
from telebot import custom_filters
import time

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
red = redis.Redis(host='localhost', port=6379, db=1, password=None, socket_timeout=None)

token = '5055960243:AAE0ZNGoZnO0BeqEMxGnLrSf9jEyiCTlGR0'
bot = telebot.TeleBot(token, threaded=True)

greeting = "Приветствую, тебя путник. Я помогу тебе выбрать концерт в Питере.\n" \
           "Для поиска используй команду /search"

choice_genre = "Выберите жанр мероприятия:"
choice_date = "Введите диапозон дат (Пример: 01.01-31.12):"

genres_code = ['folk_mer', 'dance', 'humor', 'shou', 'klassika', 'rock', 'estrada',
          'dzhaz', 'folk', 'shanson', 'hip-hop', 'electro',
          'tvorcheskiy-vecher', 'otherkoncert', 'clubs', 'natsionalnye']

genres = ['Фольклорные мероприятия', 'Танец', 'Юмор', 'Шоу', 'Классика','Рок', 'Поп/Эстрада',
          'Джаз', 'Народная/Фолк', 'Авторская/Шансон/Романсы', 'Хип-хоп/Рэп', 'Электронная музыка',
          'Творческий вечер', 'Другое', 'Клубы', 'Национальные мероприятия']


class States:
    genre = 1
    date = 2


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, greeting)


@bot.message_handler(commands="search")
def search(message):
    genre_markup = types.ReplyKeyboardMarkup()
    genre_1 = types.KeyboardButton('Фольклорные мероприятия')
    genre_2 = types.KeyboardButton('Танец')
    genre_3 = types.KeyboardButton('Юмор')
    genre_4 = types.KeyboardButton('Шоу')
    genre_5 = types.KeyboardButton('Классика')
    genre_6 = types.KeyboardButton('Рок')
    genre_7 = types.KeyboardButton('Поп/Эстрада')
    genre_8 = types.KeyboardButton('Джаз')
    genre_9 = types.KeyboardButton('Народная/Фолк')
    genre_10 = types.KeyboardButton('Авторская/Шансон/Романсы')
    genre_11 = types.KeyboardButton('Хип-хоп/Рэп')
    genre_12 = types.KeyboardButton('Электронная музыка')
    genre_13 = types.KeyboardButton('Творческий вечер')
    genre_14 = types.KeyboardButton('Другое')
    genre_15 = types.KeyboardButton('Клубы')
    genre_16 = types.KeyboardButton('Национальные мероприятия')

    genre_markup.row(genre_1, genre_10)
    genre_markup.row(genre_16, genre_9)
    genre_markup.row(genre_2, genre_3, genre_4, genre_5)
    genre_markup.row(genre_6, genre_7, genre_8, genre_11)
    genre_markup.row(genre_14, genre_15, genre_13, genre_12)

    bot.set_state(message.from_user.id, States.genre)
    bot.send_message(message.from_user.id, choice_genre, reply_markup=genre_markup)


@bot.message_handler(state=States.genre)
def get_genre(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, choice_date, reply_markup=markup)
    bot.set_state(message.from_user.id, States.date)
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = genres_code[genres.index(message.text)]


@bot.message_handler(state=States.date)
def get_date(message):
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(message.from_user.id, f"Ищем билеты {data['genre']}...")
        data['date'] = message.text
    # bot.register_next_step_handler(message, scrap)
        scrap(message)


def scrap(message):

    bot.send_message(message.from_user.id, 'Еще немного...')
    show_concerts(message)


def show_concerts(message):
    bot.send_message(message.from_user.id, 'Got it')
    with bot.retrieve_data(message.from_user.id) as data:
        d = []
        datelist = []

        bot.send_message(message.from_user.id, data['date'])

        m_f = re.search(r'(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2])-', data['date']).group()[:-1] + '.22'
        m_t = re.search(r'-(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2])', data['date']).group()[1:] + '.22'
        d_f = datetime.strptime(m_f, '%d.%m.%y').date()
        d_t = datetime.strptime(m_t, '%d.%m.%y').date()

        for day in pd.date_range(min(d_f, d_t), max(d_f, d_t)):
            day, month = day.strftime('%d %b').split(' ')
            datelist.append(f'{day} {month.capitalize()}')

        for date in datelist:
            for key in red.scan_iter(f"{data['genre']}:{date}*:*"):
                for i in red.hscan(key):
                    if i != 0:
                        d.append(i)

        for t in range(len(d)):
            img = open('out.jpg', 'wb')
            img.write(urllib.request.urlopen(d[t].get(b'img').decode('utf-8')).read())
            img.close()
            img = open('out.jpg', 'rb')

            markup = types.InlineKeyboardMarkup()
            open_btn = types.InlineKeyboardButton(text='Купить билет', url=d[t].get(b'href').decode('utf-8'))
            markup.add(open_btn)

            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, caption=f"{d[t].get(b'title').decode('utf-8')}\n"
                                                              f"{d[t].get(b'time').decode('utf-8')}\n"
                                                              f"{d[t].get(b'cost').decode('utf-8')}",
                           reply_markup=markup)
            img.close()
            if len(d)>10:
                time.sleep(1)
            else:
                time.sleep(0.5)


if __name__ == '__main__':

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.enable_saving_states()

    bot.polling(none_stop=True, interval=0)

