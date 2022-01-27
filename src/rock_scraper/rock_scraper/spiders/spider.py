import random
import time
import urllib.parse
import schedule

import urllib3.packages.six
from twisted.internet import reactor
import redis

import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess

red = redis.Redis(host='localhost', port=6379, db=1, password=None, socket_timeout=None)

agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 YaBrowser/17.4.3.195.10 Mobile/14A346 Safari/E7FBAF']


class RockSpider(scrapy.Spider):
    name = "rock"
    data = []
    genre = 'rock'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = RockSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class DanceSpider(scrapy.Spider):
    name = "dance"
    data = []
    genre = 'dance'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = DanceSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            yield red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class FolkMerSpider(scrapy.Spider):
    name = "folkmer"
    data = []
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/?sort=0'
                ]
    city = ''
    genre = 'folk_mer'

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = FolkMerSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            yield red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class HumorSpider(scrapy.Spider):
    name = "humor"
    data = []
    genre = 'humor'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = HumorSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ShouSpider(scrapy.Spider):
    name = "shou"
    data = []
    genre = 'shou'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = ShouSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class KlassikaSpider(scrapy.Spider):
    name = "klassika"
    data = []
    genre = 'klassika'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = KlassikaSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class EstradaSpider(scrapy.Spider):
    name = "estrada"
    data = []
    genre = 'estrada'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = EstradaSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class DzhazSpider(scrapy.Spider):
    name = "dzhaz"
    data = []
    genre = 'dzhaz'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = DzhazSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class FolkSpider(scrapy.Spider):
    name = "folk"
    data = []
    genre = 'folk'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = FolkSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ShansonSpider(scrapy.Spider):
    name = "shanson"
    data = []
    genre = 'shanson'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ShansonSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class HipHopSpider(scrapy.Spider):
    name = "hip-hop"
    data = []
    genre = 'hip-hop'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = HipHopSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ElectroSpider(scrapy.Spider):
    name = "electro"
    data = []
    genre = 'electro'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ElectroSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class TvorSpider(scrapy.Spider):
    name = "tvorcheskiy-vecher"
    data = []
    genre = 'tvorcheskiy-vecher'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = TvorSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class OtherSpider(scrapy.Spider):
    name = "otherkoncerts"
    data = []
    genre = 'otherkoncerts'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = OtherSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ClubsSpider(scrapy.Spider):
    name = "clubs"
    data = []
    genre = 'clubs'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ClubsSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class NatsSpider(scrapy.Spider):
    name = "natsionalnye"
    data = []
    genre = 'natsionalnye'
    url_list = [f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://msk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://aba.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://anapa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://arh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://astr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://brn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://belgorod.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://blag.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://bryansk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vl.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vlg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vologda.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://vrn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://gel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ekb.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ivanovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://izhevsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://irk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yola.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kgd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://klg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kemerovo.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kirov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krs.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://krym.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://kursk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lzr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://lipetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://mgn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://murm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nabchelny.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://novokuznetsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://nvrsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://nsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://omsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orenburg.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://orsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pnz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://perm.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ptz.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://pskov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rnd.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://rzn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saransk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://saratov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://smolensk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sochi.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://oskol.kassir.ru/bilety-na-koncert/{genre}?sort=0',

                f'https://sur.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tambov.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tver.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tlt.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tomsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tula.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://tmn.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulan.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ulyanovsk.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://ufa.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://hbr.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chaik.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cheboksary.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chel.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://cher.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://chita.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://sakh.kassir.ru/bilety-na-koncert/{genre}?sort=0',
                f'https://yar.kassir.ru/bilety-na-koncert/{genre}?sort=0'
                ]
    city = ''

    def start_requests(self):
        for url in self.url_list:
            self.city = url[8:url.index('.')]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = NatsSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{self.city}:{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
                'city': self.city,
                'genre': genre,
                'title': title,
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': time,
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


def crawling():
    red.flushdb()
    process = CrawlerProcess({
        'USER_AGENT': agents[random.randint(0, 2)]
    })

    process.crawl(RockSpider)
    process.crawl(DanceSpider)
    process.crawl(FolkMerSpider)
    process.crawl(ShouSpider)
    process.crawl(KlassikaSpider)
    process.crawl(EstradaSpider)
    process.crawl(DzhazSpider)
    process.crawl(FolkSpider)
    process.crawl(ShansonSpider)
    process.crawl(HipHopSpider)
    process.crawl(ElectroSpider)
    process.crawl(TvorSpider)
    process.crawl(OtherSpider)
    process.crawl(ClubsSpider)
    process.crawl(NatsSpider)
    process.crawl(HumorSpider)

    process.start()
    print('Process stoped')


if __name__ == '__main__':
    crawling()
    schedule.every().monday.at('10:00').do(crawling)
    while True:
        schedule.run_pending()
        time.sleep(60)
