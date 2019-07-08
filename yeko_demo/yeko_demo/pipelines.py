# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo

class YekoDemoPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
	def __init__(self):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB','scrapy')

	def process_item(self, item, spider):
		record=dict(item)
		record['_id']=record['id']
		record.pop('id')
	
		collection_name=item.get('type',spider.name)
		if 'type' in item:
			record.pop('type')
	
		result=self.db[collection_name].update_one({'_id':record['_id']},{'$set':record},upsert=True)
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

class CommentPipeline(object):
	def __init__(self):
		self.filepath=settings['ITEM_STORE']
        
	def open_spider(self,spider):
		print('comment pipeline open')
		if spider.name=='comment':
			filename=os.path.join(self.filepath,spider.name+'.txt')
			self.file=open(filename,'w',encoding='utf-8')

	def process_item(self,item,spider):
		#print(item)
		if spider.name=='comment':
			#record=json.dumps(dict(item),ensure_ascii=False)
			#self.file.write(record+",\n")
			for key,value in dict(item).items():
				if key=='content':
					self.file.write("\n"+value+"\n")
				else:
					self.file.write(key+" : "+value+"\n")
			self.file.write("\n########################################################\n\n")
		return item

	def close_spider(self,spider):
		if self.file:
			self.file.close()


import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from yeko_demo.items import LessonItem
import re

class MeterialsPipeline(FilesPipeline):

	meterial_download_uri='https://class.121talk.cn/Public/Uploads/Materials/'
	
	def parse_to_valid_filename(self,title):
		rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
		new_title = re.sub(rstr, "_", title)  		# 替换为下划线
		return new_title

	def get_media_requests(self,item,info):
		if isinstance(item,LessonItem) and item.get('doc',None):
			ext=item['doc'].split('.')[-1]
			filename=self.parse_to_valid_filename(item['name']+"."+ext)
			yield scrapy.Request(
				self.meterial_download_uri+item['doc']
				,meta={'filename':filename,'path':item['path']})

	def file_path(self,request,response=None,info=None):
		return request.meta['path']+"/"+request.meta['filename']

	def item_completed(self,results, item, info):
		#item['images']=results
		r = [ x for ok, x in results if ok]
		if not r:
			raise DropItem("Item contains no images")
		#item['file'] = results
		item['file']=r[0]
		item['status']='Done'
		item.pop('path')
		return item



