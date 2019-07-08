# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import datetime


class HotMovieSpider(scrapy.Spider):
    name = 'hotMovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        # loader=ItemLoader(item=MovieItem(),response=response)
        movieSelectors = response.xpath("//*[@id='screening']//li[@data-title]")
        for s in movieSelectors:
            loader = ItemLoader(item=MovieItem(), selector=s)

            loader.add_css('title', '::attr(data-title)', TakeFirst(), MapCompose(str.strip))
            loader.add_xpath('rate', './@data-rate', TakeFirst())
            loader.add_xpath('url', ".//li[@class='poster']/a/@href", TakeFirst())
            loader.add_xpath('cover', ".//li[@class='poster']//img/@src", TakeFirst())
            loader.add_css('id', "::attr(data-trailer)", TakeFirst(), re=r'\d+')

            # loader.add_value('crawl_date', datetime.datetime.now())
            loader.add_value('crawl_date', str(datetime.datetime.now()))  # Join() only used for str List

            loader.default_output_processor = Join()  # add for convert field value List to String

            yield loader.load_item()
