import random
import urllib.parse
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = RockSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = DanceSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            yield red.hmset(key_name, {
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
    url = 'https://spb.kassir.ru/bilety-na-koncert/?sort=0'
    genre = 'folk_mer'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = FolkMerSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            yield red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = HumorSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = ShouSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = KlassikaSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = EstradaSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = DzhazSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")

            genre = FolkSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ShansonSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = HipHopSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ElectroSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = TvorSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = OtherSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = ClubsSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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
    url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):

            genre = NatsSpider.genre
            time = concert.css('div.event-card__caption time nobr::text ').get().strip()
            title = concert.css('div.event-card__caption div.title a::text').get().strip()
            title_encoded = urllib.parse.quote_plus(title)

            key_name = f"{genre}:{time}:{title_encoded}"

            red.hmset(key_name, {
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


if __name__ == '__main__':
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
