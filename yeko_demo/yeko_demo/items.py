# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YekoDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CourseItem(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    type=scrapy.Field()
    
class UnitItem(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    type=scrapy.Field()
    parent_id=scrapy.Field()
    
class LessonItem(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    type=scrapy.Field()
    parent_id=scrapy.Field()
    doc=scrapy.Field()
    path=scrapy.Field()
    file=scrapy.Field()
    status=scrapy.Field()

class CommentItem(scrapy.Item):
	id=scrapy.Field()
	course=scrapy.Field()
	unit=scrapy.Field()
	lesson=scrapy.Field()
	doc=scrapy.Field()
	teacher=scrapy.Field()
	teacher_id=scrapy.Field()
	time=scrapy.Field()
	content=scrapy.Field()

