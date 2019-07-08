# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from douban_demo.items import Top250Item #,CoverItem

class Top250Spider(CrawlSpider):
    name = 'top250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(
            LinkExtractor(allow=r'\?start=\d+.*',restrict_xpaths='//div[@class="paginator"]')
            , callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        # records=response.xpath('//ol[@class="grid_view"]//div[@class="item"]/div[@class="info"]')
        # for r in records:
        #     item=Top250Item()
        #     link=r.xpath('./div[@class="hd"]/a/@href').get()
        #     item['id']=link.split('/')[-2]
        #     item['title']=r.xpath('./div[@class="hd"]/a/span[@class="title"]/text()').extract_first()
        #     item['rate']=r.xpath('./div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
        #     item['quote']=r.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
        #     yield item
        # records=response.xpath('//ol[@class="grid_view"]//div[@class="item"]/div[@class="pic"]//img')
        # for r in records:
        #     item=CoverItem()
        #     item['name']=r.xpath('./@alt').get()
        #     item['url']=r.xpath('./@src').get()
        #     print(item['url'])
        #     yield item

        records=response.xpath('//ol[@class="grid_view"]//div[@class="item"]')
        for r in records:
            infoPath=r.xpath('./div[@class="info"]')
            picPath=r.xpath('./div[@class="pic"]//img')

            item=Top250Item()
            link=infoPath.xpath('./div[@class="hd"]/a/@href').get()
            item['id']=link.split('/')[-2]
            item['title']=infoPath.xpath('./div[@class="hd"]/a/span[@class="title"]/text()').extract_first()
            item['rate']=infoPath.xpath('./div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['quote']=infoPath.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            item['cover']={
                'name':picPath.xpath('./@alt').get()
                ,'url':picPath.xpath('./@src').get()
            }
            yield item


