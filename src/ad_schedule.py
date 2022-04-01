from datetime import datetime
import time
import redis
import schedule

from src.bot import send_message_to_users

ads_base = redis.Redis(host='localhost', port=6379, db=3, password=None, socket_timeout=None)


def ad(ad_date, ad_time):
    print('got')
    ad_day = str(ad_date.day)
    ad_month = str(ad_date.month)

    a = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    if ad_month in a:
        ad_month = f'0{ad_month}'
    if ad_day in a:
        ad_day = f'0{ad_day}'

    c = 0
    for key in ads_base.scan_iter(f'{ad_date.year}-{ad_month}-{ad_day} {ad_time}'):
        c += 1
        for i in ads_base.hscan(key):
            if i != 0:
                send_message_to_users(i.get(b'text').decode('utf-8'))
        ads_base.delete(f'{ad_date.year}-{ad_month}-{ad_day} {ad_time}')
    if c == 0:
        send_message_to_users('Здесь могла быть Ваша реклама!')


if __name__ == '__main__':
    schedule.every().day.at('08:00').do(ad, ad_date=datetime.now(), ad_time='8:00')
    schedule.every().day.at('12:00').do(ad, ad_date=datetime.now(), ad_time='12:00')
    schedule.every().day.at('16:00').do(ad, ad_date=datetime.now(), ad_time='16:00')
    schedule.every().day.at('20:00').do(ad, ad_date=datetime.now(), ad_time='20:00')

    while True:
        schedule.run_pending()
        time.sleep(1)
