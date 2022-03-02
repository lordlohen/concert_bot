import random
import time
import urllib.parse
import schedule
import argparse

# import urllib3.packages.six
# from twisted.internet import reactor
import redis

import scrapy
# from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/74.0.3729.169 Safari/537.36',
    'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) ' +
    'Version/10.0 YaBrowser/17.4.3.195.10 Mobile/14A346 Safari/E7FBAF'
]


class BotSpider(scrapy.Spider):
    genre_codes = ['folk_mer', 'dance', 'humor', 'shou', 'klassika', 'rock', 'estrada', 'dzhaz', 'folk', 'shanson',
                   'hip-hop', 'electro', 'tvorcheskiy-vecher', 'otherkoncert', 'clubs', 'natsionalnye']
    # city_codes = ['msk', 'spb', 'aba', 'anapa', 'arh', 'astr', 'brn', 'belgorod', 'blag', 'bryansk', 'nov', 'vl', 'vlm',
    #               'vlg', 'vologda', 'vrn', 'gel', 'ekb', 'ivanovo', 'izhevsk', 'irk', 'yola', 'kzn', 'kgd', 'klg',
    #               'kemerovo', 'kirov', 'krd', 'krs', 'krym', 'kursk', 'lzr', 'lipetsk', 'mgn', 'murm', 'nabchelny',
    #               'nn', 'novokuznetsk', 'nvrsk', 'nsk', 'omsk', 'orenburg', 'orel', 'orsk', 'pnz', 'perm', 'ptz',
    #               'pskov', 'rnd', 'rzn', 'smr', 'saransk', 'saratov', 'smolensk', 'sochi', 'sk', 'oskol', 'sur',
    #               'tambov', 'tver', 'tlt', 'tomsk', 'tula', 'tmn', 'ulan', 'ulyanovsk', 'ufa', 'hbr', 'chaik',
    #               'cheboksary', 'chel', 'cher', 'chita', 'sakh', 'yar']
    city_codes = ['msk', 'spb', 'tver']

    data = []
    name = 'bot_spider'

    @classmethod
    def genre_urls(cls, genre_code):
        return [f'https://{city_code}.kassir.ru/bilety-na-koncert/{genre_code}?sort=0' for city_code in cls.city_codes]

    def start_requests(self):
        genre_code = self.settings.get('GENRE_CODE')
        for url in self.genre_urls(genre_code):
            city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'city': city})

    def parse(self, response, **kwargs):
        city = kwargs['city']
        genre_code = self.settings.get('GENRE_CODE')
        redis_uri = self.settings.get('REDIS_URI')
        redis_conn = redis.from_url(redis_uri, socket_timeout=None)

        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            event_time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{city}:{genre_code}:{event_time}:{title_encoded}"

            redis_conn.hmset(key_name, {
                'city': city,
                'genre': genre_code,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': event_time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })
        redis_conn.close()

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


def crawling(redis_uri):
    redis_conn = redis.from_url(redis_uri, socket_timeout=None)
    redis_conn.flushdb()
    redis_conn.close()

    # genre_code = self.settings.get('GENRE_CODE')
    # redis_conn = self.settings.get('REDIS_CONNECTION')

    for genre_code in BotSpider.genre_codes:
        process = CrawlerProcess({
            'USER_AGENT': agents[random.randint(0, 2)],
            'GENRE_CODE': genre_code,
            'REDIS_URI': redis_uri
        })

        process.crawl(BotSpider)

    process.start()
    print('Process stopped')


def main(args):
    crawling(args.redis_uri)
    schedule.every().monday.at('10:00').do(crawling, args.redis_uri)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--redis-uri', type=str, default='redis://localhost:6379/1', help='Redis server URI')
    main(parser.parse_args())
