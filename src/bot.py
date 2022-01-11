import urllib.request

import telebot
from telebot import types
from telebot import custom_filters
import json
import time

from rock_scraper.rock_scraper.spiders.rock_spider import ConcertsSpider

token = '5055960243:AAE0ZNGoZnO0BeqEMxGnLrSf9jEyiCTlGR0'
bot = telebot.TeleBot(token, threaded=False)

greeting = "Приветствую, тебя путник. Я помогу тебе выбрать концерт в Питере.\n" \
           "Для поиска используй команду /search"

choice_genre = "Выберите жанр мероприятия:"
choice_date = "Введите диапозон дат (Пример: 01.01.2022-31.12.2022):"

genres_code = ['', 'dance', 'humor', 'shou', 'klassika', 'rock', 'estrada',
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
        data['date_from'], data['date_to'] = message.text.split('-')
    # bot.register_next_step_handler(message, scrap)
    scrap(message)


def scrap(message):
    print('got it')
    with bot.retrieve_data(message.from_user.id) as data:
        ConcertsSpider.start(data['genre'], data['date_from'], data['date_to'])
    bot.send_message(message.from_user.id, 'Еще немного...')
    bot.delete_state(message.from_user.id)
    # bot.register_next_step_handler(message, show_concerts)
    show_concerts(message)


def show_concerts(message):
    # bot.send_message(message.from_user.id, 'reading json and send msg')
    with open('concerts.json') as f:
        data = json.load(f)

    for t in range(len(data)):
        img = open('out.jpg', 'wb')
        img.write(urllib.request.urlopen(data[t]['img']).read())
        img.close()
        img = open('out.jpg', 'rb')

        markup = types.InlineKeyboardMarkup()
        open_btn = types.InlineKeyboardButton(text='Купить билет', url=data[t]['href'])
        markup.add(open_btn)

        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img, caption=f"{data[t]['title']}\n{data[t]['time']}\n{data[t]['cost']}",
                       reply_markup=markup)
        img.close()

        time.sleep(0.5)


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.enable_saving_states()

    bot.polling(none_stop=True, interval=0)

