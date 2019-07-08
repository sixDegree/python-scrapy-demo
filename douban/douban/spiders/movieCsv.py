# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose
import datetime


class MoviecsvSpider(scrapy.Spider):
    name = 'movieCsv'
    allowed_domains = ['movie.douban.com']

    # start_urls = ['http://movie.douban.com/']

    def start_requests(self):
        with open("movie.csv", 'rU') as f:
            reader = csv.DictReader(f)
            for line in reader:
                print(line)
                # OrderedDict([('src_url', 'http://movie.douban.com/'),
                # ('src_selector', '#screening li[data-title]'),
                # ('title', '::attr(data-title)'),
                # ('rate', '::attr(data-rate)'),
                # ('url', 'li.poster>a::attr(href)'),
                # ('cover', 'li.poster img::attr(src)'),
                # ('id', '::attr(data-trailer)')])
                yield scrapy.Request(url=line.pop('src_url'), callback=self.parse, meta={'rule': line})

    def parse(self, response):
        line = response.meta['rule']
        src_selector = response.css(line.pop('src_selector'))
        for s in src_selector:
            item = Item()
            loader = ItemLoader(item=item, selector=s)
            for name, exp in line.items():
                if exp:
                    item.fields[name] = Field()
                    loader.add_css(name, exp)

            item.fields['crawl_date'] = Field() # Field(output_processor=Identity())
            loader.add_value('crawl_date', datetime.datetime.now(), str)

            loader.default_output_processor = Join()
            yield loader.load_item()
