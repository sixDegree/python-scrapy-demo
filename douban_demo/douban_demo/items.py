# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
	#{'rate': '7.0', 'cover_x': 7142, 'title': '飞驰人生', 'url': 'https://movie.douban.com/subject/30163509/', 'playable': True, 'cover': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2542973862.jpg', 'id': '30163509', 'cover_y': 10000, 'is_new': False}
	rate=scrapy.Field()
	cover_x=scrapy.Field()
	title=scrapy.Field()
	url=scrapy.Field()
	playable=scrapy.Field()
	cover=scrapy.Field()
	cover_y=scrapy.Field()
	id=scrapy.Field()
	cover_y=scrapy.Field()
	is_new=scrapy.Field()

class Top250Item(scrapy.Item):
	# {"id": "1291572", "title": "指环王2：双塔奇兵", "rate": "9.0", "quote": "承前启后的史诗篇章。"}
	title=scrapy.Field()
	id=scrapy.Field()
	rate=scrapy.Field()
	quote=scrapy.Field()
	cover=scrapy.Field()

class CoverItem(scrapy.Item):
	name=scrapy.Field()
	url=scrapy.Field()
	path=scrapy.Field()
	#images=scrapy.Field()
	checksum=scrapy.Field()


	