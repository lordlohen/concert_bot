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
redis_users = redis.Redis(host='localhost', port=6379, db=2, password=None, socket_timeout=None)


# print(len(red.keys()))
# for key in red.scan_iter(f"*:rock:*:*"):
#     print(key)

token = '5055960243:AAE0ZNGoZnO0BeqEMxGnLrSf9jEyiCTlGR0'
bot = telebot.TeleBot(token, threaded=True)

greeting = "Приветствую, тебя путник. Я помогу тебе выбрать концерт в Питере.\n" \
           "Для поиска используй команду /search"

choice_city = "Выберите город"
choice_genre = "Выберите жанр мероприятия:"
choice_date = "Введите диапозон дат (Пример: 01.01-31.12):"

genres_code = ['folk_mer', 'dance', 'humor', 'shou', 'klassika', 'rock', 'estrada',
          'dzhaz', 'folk', 'shanson', 'hip-hop', 'electro',
          'tvorcheskiy-vecher', 'otherkoncert', 'clubs', 'natsionalnye']

genres = ['Фольклорные мероприятия', 'Танец', 'Юмор', 'Шоу', 'Классика','Рок', 'Поп/Эстрада',
          'Джаз', 'Народная/Фолк', 'Авторская/Шансон/Романсы', 'Хип-хоп/Рэп', 'Электронная музыка',
          'Творческий вечер', 'Другое', 'Клубы', 'Национальные мероприятия']

cities = ['Москва', 'Санкт-Петербург', 'Абакан', 'Анапа', 'Архангельск', 'Астрахань', 'Барнаул', 'Белгород',
          'Благовещенск', 'Брянск', 'Вел. Новгород', 'Владивосток', 'Владимир', 'Волгоград', 'Вологда', 'Воронеж',
          'Геленджик', 'Екатеринбург', 'Иваново', 'Ижевск', 'Иркутск', 'Йошкар-Ола', 'Казань', 'Калининград', 'Калуга',
          'Кемерово', 'Киров', 'Краснодар', 'Красноярск', 'Крым', 'Курск', 'Лазаревское', 'Липецк', 'Магнитогорск',
          'Мурманск', 'Набережные Челны', 'Ниж. Новгород', 'Новокузнецк', 'Новороссийск', 'Новосибирск', 'Омск',
          'Оренбург', 'Орёл', 'Орск', 'Пенза', 'Пермь', 'Петрозаводск', 'Псков', 'Ростов-на-Дону', 'Рязань', 'Самара',
          'Саранск', 'Саратов', 'Смоленск', 'Сочи', 'Ставрополь', 'Старый оскол', 'Сургут', 'Тамбов', 'Тверь',
          'Тольятти', 'Томск', 'Тула', 'Тюмень', 'Улан-Удэ', 'Ульяновск', 'Уфа', 'Хабаровск', 'Чайковский', 'Чебоксары',
          'Челябинск', 'Череповец', 'Чита', 'Южно-Сахалинск', 'Ярославль']

cities_code = ['msk', 'spb', 'aba', 'anapa', 'arh', 'astr', 'brn', 'belgorod', 'blag', 'bryansk', 'nov', 'vl', 'vlm',
               'vlg', 'vologda', 'vrn', 'gel', 'ekb', 'ivanovo', 'izhevsk', 'irk', 'yola', 'kzn', 'kgd', 'klg',
               'kemerovo', 'kirov', 'krd', 'krs', 'krym', 'kursk', 'lzr', 'lipetsk', 'mgn', 'murm', 'nabchelny', 'nn',
               'novokuznetsk', 'nvrsk', 'nsk', 'omsk', 'orenburg', 'orel', 'orsk', 'pnz', 'perm', 'ptz', 'pskov', 'rnd',
               'rzn', 'smr', 'saransk', 'saratov', 'smolensk', 'sochi', 'sk', 'oskol', 'sur', 'tambov', 'tver', 'tlt',
               'tomsk', 'tula', 'tmn', 'ulan', 'ulyanovsk', 'ufa', 'hbr', 'chaik', 'cheboksary', 'chel', 'cher',
               'chita', 'sakh', 'yar']


class States:
    genre = 1
    date = 2
    city_changed = 3
    search = 4


def send_message_to_users(msg):
    for i in redis_users.scan_iter('*'):
        id = i.decode('utf-8')[5::]
        bot.send_message(id, msg)


def get_all_users():
    return str(redis_users.dbsize())


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id not in redis_users.scan_iter(f'user:{message.from_user.id}'):
        redis_users.set(name=f'user:{message.from_user.id}', value=message.from_user.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['city'] = ''
    bot.send_message(message.from_user.id, greeting)


@bot.message_handler(commands="city")
def city(message):
    city_markup = types.ReplyKeyboardMarkup()
    cities_btn = []
    for c in range(len(cities)):
        cities_btn.append(types.KeyboardButton(cities[c]))
        city_markup.add(cities_btn[c])
    bot.set_state(message.from_user.id, States.city_changed)
    bot.send_message(message.from_user.id, choice_city, reply_markup=city_markup)


@bot.message_handler(state=States.city_changed)
def city_changed(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['city'] = cities_code[cities.index(message.text)]
        print(data['city'])
    markup = types.ReplyKeyboardRemove()
    bot.set_state(message.from_user.id, States.search)
    bot.send_message(message.from_user.id, "Город выбран!\n Введите /search что бы начать поиск!", reply_markup=markup)


@bot.message_handler(commands="search", state=States.search)
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
        print(data['genre'])


@bot.message_handler(state=States.date)
def get_date(message):
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(message.from_user.id, f"Ищем билеты {data['genre']}...")
        if message.text != '/search':
            data['date'] = message.text
        print(data['date'])
    # bot.register_next_step_handler(message, scrap)
    scrap(message)


def scrap(message):

    bot.send_message(message.from_user.id, 'Еще немного...')
    show_concerts(message)


def show_concerts(message):
    with bot.retrieve_data(message.from_user.id) as data:
        print(data)
        d = []
        dateList = []

        m_f = re.search(r'(3[01]|[12][0-9]|0?[1-9])\.(1[0-2]|0?[1-9])-', data['date']).group()[
              :-1] + f'.{datetime.now().year}'
        m_t = re.search(r'-(3[01]|[12][0-9]|0?[1-9])\.(1[0-2]|0?[1-9])', data['date']).group()[
              1:] + f'.{datetime.now().year}'

        d_f = datetime.strptime(m_f, '%d.%m.%Y')  # .date()
        d_t = datetime.strptime(m_t, '%d.%m.%Y')  # .date()

        if d_t < d_f:
            d_t = d_t.replace(year=d_t.year + 1)

        d_f = d_f.date()
        d_t = d_t.date()

        for day in pd.date_range(min(d_f, d_t), max(d_f, d_t)):
            day, month = day.strftime('%d %b').split(' ')
            dateList.append(f'{day} {month.capitalize()}')

        for date in dateList:
            # print(f'DEBUG: {date}')
            # print(f"DEBUG: {data['city']}:{data['genre']}:{date}:*")
            for key in red.scan_iter(f"{data['city']}:{data['genre']}:{date}*:*"):
                print(f'DEBUG: {key}')
                for i in red.hscan(key):
                    if i != 0:
                        print(f'DEBUG: {i}')
                        d.append(i)

        for t in range(len(d)):
            print('-', end='')
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