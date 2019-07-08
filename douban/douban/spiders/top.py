# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from douban.items import Top250Item


class TopSpider(RedisCrawlSpider):
    name = 'top'

    allowed_domains = ['movie.douban.com']

    # start_urls -- no need
    # could get from Redis - set `redis_key='...'`
    # (default setting:`START_URLS_KEY='%(name)s:start_urls'`)
    # start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(
            LinkExtractor(allow=r'\?start=\d+.*', restrict_xpaths='//div[@class="paginator"]')
            , callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        records = response.xpath('//ol[@class="grid_view"]//div[@class="item"]')
        for r in records:
            infoPath = r.xpath('./div[@class="info"]')
            picPath = r.xpath('./div[@class="pic"]//img')

            item = Top250Item()
            link = infoPath.xpath('./div[@class="hd"]/a/@href').get()
            item['id'] = link.split('/')[-2]
            item['title'] = infoPath.xpath('./div[@class="hd"]/a/span[@class="title"]/text()').extract_first()
            item['rate'] = infoPath.xpath(
                './div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['quote'] = infoPath.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            item['cover'] = {
                'name': picPath.xpath('./@alt').get()
                , 'url': picPath.xpath('./@src').get()
            }
            yield item
