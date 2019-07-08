# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo

class DoubanDemoPipeline(object):
	def process_item(self, item, spider):
		pass

# class MoviePipeline(object):
# 	def __init__(self,mongo_uri,mongo_db):
# 		self.mongo_uri=mongo_uri
# 		self.mongo_db=mongo_db
# 		self.collection_name='movies'

# 	@classmethod
# 	def from_crawler(cls,crawler):
# 		return cls(
# 			mongo_uri=crawler.settings.get('MONGO_CONN_STR')
# 			,mongo_db=crawler.settings.get('MONGO_DB','scrapy')
# 		)

# 	def open_spider(self,spider):
# 		self.client = pymongo.MongoClient(self.mongo_uri)
# 		self.db = self.client[self.mongo_db]

# 	def close_spider(self,spider):
# 		self.client.close()

# 	def process_item(self, item, spider):
# 		self.db[self.collection_name].insert(dict(item))
# 		return item

class MongoPipeline(object):
	def __init__(self):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB','scrapy')

	def process_item(self, item, spider):
		record=dict(item)
		record['_id']=record['id']
		record.pop('id')
		result=self.db[spider.name].update_one({'_id':record['_id']},{'$set':record},upsert=True)
		# print(result.raw_result)
		return item

	def open_spider(self,spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
		#print(self.client.list_database_names())
		#print(self.db.list_collection_names())

	def close_spider(self,spider):
		self.client.close()

import os
import json

class ItemFilePipeline(object):
	def __init__(self):
		self.filepath=settings['ITEM_STORE']
        
	def open_spider(self,spider):
		filename=os.path.join(self.filepath,spider.name+'.json')
		self.file=open(filename,'w',encoding='utf-8')
		self.file.write('[\n')

	def process_item(self,item,spider):
		#print(item)
		record=json.dumps(dict(item),ensure_ascii=False)
		#print(record)
		self.file.write(record+",\n")
		return item

	def close_spider(self,spider):
		self.file.write(']\n')
		self.file.close()

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from douban_demo.items import Top250Item

class CoverImagesPipeline(ImagesPipeline):
	def get_media_requests(self,item,info):
		if isinstance(item,Top250Item):
			cover=item['cover']
			ext=cover['url'].split('.')[-1]
			yield scrapy.Request(cover['url'],meta={'image_name':cover['name']+"."+ext})

	def item_completed(self,results, item, info):
		#item['images']=results
		r = [(x['path'],x['checksum']) for ok, x in results if ok]
		if not r:
		    raise DropItem("Item contains no images")
		item['cover']['path'] = r[0][0]
		item['cover']['checksum']=r[0][1]
		return item

	def file_path(self,request,response=None,info=None):
		return 'full/%s' % request.meta['image_name']





