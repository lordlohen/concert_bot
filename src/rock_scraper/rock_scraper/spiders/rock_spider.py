import scrapy
import json
from scrapy.crawler import CrawlerProcess


class ConcertsSpider(scrapy.Spider):
    name = "concerts"
    data = []
    url = ''

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        for concert in response.css('div.event-card'):
            # response.setCharacterEncoding("UTF-8")
            yield self.data.append({
                'title': concert.css('div.event-card__caption div.title a::text').get().strip(),
                'img': concert.css('div.poster a img::attr(data-src)').get(),
                'href': concert.css('div.event-card__caption div.title a::attr(href)').get(),
                'time': concert.css('div.event-card__caption time nobr::text ').get().strip(),
                'cost': concert.css('div.event-card__caption div.cost::text').get().strip().replace(' ', '.')
            })

        next_page = response.css('a.more.js-pager-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        with open("concerts.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    @staticmethod
    def start(genre=' ', date_from='', date_to=''):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        if date_from != '' and date_to !='' and genre != '':
            ConcertsSpider.url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?date_from={date_from}&date_to={date_to}&sort=0'
        elif genre != ' ':
            ConcertsSpider.url = f'https://spb.kassir.ru/bilety-na-koncert/{genre}?sort=0'
        else:
            ConcertsSpider.url = f'https://spb.kassir.ru/bilety-na-koncert/'

        process.crawl(ConcertsSpider)
        process.start()
