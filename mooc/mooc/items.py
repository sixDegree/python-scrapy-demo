# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CategoryItem(scrapy.Item):
	id=scrapy.Field()
	name=scrapy.Field()
	parent_id=scrapy.Field()
	link_name=scrapy.Field()
	type=scrapy.Field()
	weight=scrapy.Field()
	#children=scrapy.Field()
	parent_name=scrapy.Field()
	checked=scrapy.Field()
	my_type=scrapy.Field()

class CourseItem(scrapy.Item):
	id=scrapy.Field()
	name=scrapy.Field()
	short_name=scrapy.Field()
	channel=scrapy.Field()
	status=scrapy.Field()
	learner_count=scrapy.Field()
	video_id=scrapy.Field()
	video_url=scrapy.Field()
	content=scrapy.Field()

	term=scrapy.Field()
	school=scrapy.Field()
	lector=scrapy.Field()
	tag=scrapy.Field()

	product_type=scrapy.Field()
	course_type=scrapy.Field()
	gmt_create=scrapy.Field()
	publish_time=scrapy.Field()

	page_index=scrapy.Field()
	category_id=scrapy.Field()
	category_name=scrapy.Field()

	my_type=scrapy.Field()

class PaginationItem(scrapy.Item):
	category_id=scrapy.Field()
	category_name=scrapy.Field()
	page_index=scrapy.Field()
	

	
