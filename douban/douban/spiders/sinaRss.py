# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider


class SinaRssSpider(XMLFeedSpider):
    name = 'sinaRss'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://blog.sina.com.cn/rss/1246151574.xml']
    iterator = 'iternodes' # This is actually unnecessary, since it's the default value
    itertag = 'item'       # change it accordingly

    def parse_node(self, response, selector):
        item = {}
        item['title'] = selector.xpath('title/text()').get()
        item['link'] = selector.xpath('link/text()').get()
        return item
