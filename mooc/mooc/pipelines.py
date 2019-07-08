# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MoocPipeline(object):
    def process_item(self, item, spider):
        return item

from scrapy.conf import settings
import pymongo

class MongoPipeline(object):
	def __init__(self):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB')

	def process_item(self, item, spider):
		record=dict(item)
		record['_id']=record['id']
		record.pop('id')
	
		collection_name=item.get('my_type',spider.name)
		if 'my_type' in item:
			record.pop('my_type')
	
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

class ItemStorePipeline(object):
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
		if self.file:
			self.file.write(']\n')
			self.file.close()


import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import re

class MaterialFilePipeline(FilesPipeline):

	def get_media_requests(self,item,info):
		if item.get('my_type')!='resource':
			return

		contentType=item['contentType']
		url=""
		filename=""
		index=str(item['position']+1)
		if contentType==1:
			url=item['resource']['flvHdUrl']
			# 1005808092_9ca763084ece43b7b388aaa07bc8a663_hd.flv
			filename="["+index+"]"+item['name']+"_"+url.split('_')[-1]
			print('video:',filename)
		elif contentType==3:
			url=item['resource']['textOrigUrl']
			# &download=%E8%B4%AA%E5%BF%83.pdf
			filename="["+index+"]"+item['name']+"."+url.split('.')[-1]
			print('doc:',filename)
		elif contentType==4:
			url=item['resource']['url']
			# ?fileName=week9.zip&nosKey=xxxx
			# filename:week9.zip
			filename="["+index+"]"+item['name']+"."+item['resource']['filename'].split('.')[-1]
			print('attachment:',filename)
		else:
			raise DropItem('unknow contentType: %s' % contentType)
			return

		#print('download:',filename)
		yield scrapy.Request(
			url
			,meta={
				'filename':filename
				,'course_name':item['course_name']
				,'chapter_name':item['chapter_name']
			})

	def file_path(self,request,response=None,info=None):
		filepath=self.parse_to_valid_filename(request.meta['course_name'])+"/"+self.parse_to_valid_filename(request.meta['chapter_name'])+"/"+self.parse_to_valid_filename(request.meta['filename'])
		#print(filepath)
		return filepath

	def parse_to_valid_filename(self,title):
		rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
		new_title = re.sub(rstr, "_", title)  		# 替换为下划线
		return new_title

	def item_completed(self,results, item, info):
		#print(results)
		#item['images']=results
		r = [ x for ok, x in results if ok]
		if not r:
			raise DropItem("Item contains no file")
		#print(r)
		#item['file'] = results
		item['file']=r[0]
		item['status']='Done'
		return item

class MaterialMongoPipeline(object):
	def __init__(self):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB')

	def process_item(self, item, spider):
		if item.get('my_type')!='resource':
			return

		collection_name=spider.name
		record={
			'resource':item['resource']
			,'file':item['file']
			,'material_crawl':item['status']
		}
		result=self.db[collection_name].update_one({'_id':item['id']},{'$set':record})
		# print(result.raw_result)
		return item

	def open_spider(self,spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
		#print(self.client.list_database_names())
		#print(self.db.list_collection_names())

	def close_spider(self,spider):
		self.client.close()
