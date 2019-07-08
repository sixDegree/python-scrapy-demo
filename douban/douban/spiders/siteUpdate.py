# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider


class SiteUpdateSpider(SitemapSpider):
    name = 'siteUpdate'
    allowed_domains = ['mafengwo.cn']

    sitemap_urls=['http://www.mafengwo.cn/sitemapIndex.xml']
    sitemap_rules=[
        (r'/v\d+','parse_shop')         # for parse web page(eg:html)
    ]
    sitemap_follow=[r'/shop-\d+.xml']   # for scrapy deep sitemap loc

    def sitemap_filter(self, entries):
         for entry in entries:
             # 1. entry: sitemap object(
             # <sitemap>
             #  <loc>http://www.mafengwo.cn/shop-0.xml</loc>
             #  <lastmod>2019-07-03</lastmod>
             # </sitemap>
             # )
             # 2. entry: url object(
             # <url>
             #  <loc>http://www.mafengwo.cn/v100292</loc>
             #  <lastmod>2019-07-03 02:51:02</lastmod>
             #  <changefreq>weekly</changefreq>
             #  <priority>0.7</priority>
             # </url>
             # )
             if entry['loc'].find('.xml')!=-1 or entry['loc'].find('mddid')==-1:
                 # print("entry", entry)
                 yield entry

    def parse_shop(self,response):
        # get response from detail web url page(not sitemap loc)
        # eg: http://www.mafengwo.cn/v100292  (html)
        if response.status==200:
            item={}
            item['title']=response.css('.t1').xpath('string(.)').get()
            # 使用split()去除`\xa0`，即`&nbsp`（编码原因变成了`\xa0`字符，`strip()`和`replace()`均无法有效去除该字符）
            intro="".join(response.css('.address p').xpath('string(.)').getall()).split()
            item['introduce']=" ".join(intro)
            return item