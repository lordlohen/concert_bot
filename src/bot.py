import telebot
from telebot import types
from rock_scraper.rock_scraper.spiders.rock_spider import ConcertsSpider

token = '5055960243:AAE0ZNGoZnO0BeqEMxGnLrSf9jEyiCTlGR0'
bot = telebot.TeleBot(token)

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


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    pass
    if message.text == '/start':
        bot.send_message(message.from_user.id, greeting)
    elif message.text == '/genre':
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
        genre_11= types.KeyboardButton('Хип-хоп/Рэп')
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

        bot.send_message(message.from_user.id, choice_genre, reply_markup=genre_markup)
    elif message.text in genres or message.text == '/date':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, choice_date, reply_markup=markup)
    elif message.text.split('-') != '' and message.text != '/search':
        date_from, date_to = message.text.split('-')
    elif message.text == '/search':
        ConcertsSpider.start(genre=' ', date_from='', date_to='')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

