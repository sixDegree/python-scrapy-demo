# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
import pymongo
import re

class LessonSpider(scrapy.Spider):
	name = 'lesson'
	allowed_domains = ['www.icourse163.org']
	#start_urls = ['http://www.icourse163.org/']
	lesson_url="https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr"
	form_data={
		'callCount':'1'
		,'scriptSessionId':'${scriptSessionId}190'
		,'c0-scriptName':'CourseBean'
		,'c0-methodName':'getMocTermDto'
		,'c0-id':'0'
		,'c0-param0':'number:205957211'	#tid
		,'c0-param1':'number:0'
		,'c0-param2':'boolean:true'
		,'batchId':'1'
	}

	custom_settings={
		"ITEM_PIPELINES" :{
		   'mooc.pipelines.MongoPipeline': 300,
		   'mooc.pipelines.ItemStorePipeline': 310,
		}
		,"ITEM_STORE":"./"
	}

	def __init__(self,course_id=None):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB')
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
		self.course_id=course_id

	def start_requests(self):
		query={
			'lesson_crawl':{'$ne':'Done'}
		}
		if self.course_id:
			query['_id']=int(self.course_id)

		for course in self.db['course'].find(query,{'term.id':1,'name':1}):
			term_id=course['term']['id']
			self.form_data['c0-param0']='number:'+str(term_id)
			yield scrapy.FormRequest(
				self.lesson_url
				,formdata=self.form_data
				,meta={
					'course_id':course['_id']
					,'term_id':term_id
					,'course_name':course['name']
				}
				,callback=self.parse
			)

	def closed(self,reason):
		print('closed `lesson` spider:',reason)
		self.client.close()

	def parse(self, response):
		course_id=response.meta['course_id']
		term_id=response.meta['term_id']
		course_name=response.meta['course_name']
		print("parse:",course_id,term_id,course_name)

		ls=re.findall(r's\d+\.\w+=.*;',response.body.decode('utf-8'))
		if not ls or len(ls)==0:
			print('fail:',course_name)
			self.db['course'].update_one({'_id':course_id},{'$set':{'lesson_crawl':'Fail'}})
			return
			
		lsMap={}
		for i in ls:
			item=i.encode('utf-8').decode('unicode_escape')
			props=re.split(r's\d+.',item)
			record={}
			if item.find("lessons")!=-1 or item.find("units")!=-1:
				record['my_type']="lesson"
			else:
				record['my_type']="material"

			for p in props:
				if not p:
					continue
				results=re.split(r'=|;',p)
				#print(results)
				if len(results)>1 and results[1]!='null' and results[1]!='':
					record[results[0]]=results[1]
					#print(results[0],results[1])
			# print(record)
			key=record.get('id')
			if key:
				record['id']=int(key)
				record['name']=re.sub(r'"','',record['name'])
				if record.get('chapterId'):
					record['chapterId']=int(record['chapterId'])
				if record.get('lessonId'):
					record['lessonId']=int(record['lessonId'])
				if record.get('contentId'):
					record['contentId']=int(record['contentId'])
				if record.get('position'):
					record['position']=int(record['position'])
				if record.get('contentType'):
					record['contentType']=int(record['contentType'])
				if record.get('termId'):
					record['termId']=int(record['termId'])

				record['course_id']=course_id
				record['course_name']=course_name
				lsMap[record['id']]=record

		#print(lsMap)
		i=1
		for k,v in lsMap.items():
			if v.get('chapterId'):
				chapter_record=lsMap.get(v['chapterId'])
				v['chapter_name']=chapter_record['name']
			if v.get('lessonId'):
				lesson_record=lsMap.get(v['lessonId'])
				v['lesson_name']=lesson_record['name']
			if v.get('contentType')==2 and v.get('contentId'):
				exam_record=lsMap.get(v['contentId'])
				exam_record['chapterId']=v.get('chapterId')
				exam_record['lessonId']=v.get('id')
				lsMap[exam_record['id']].update(exam_record)

			#print(i,k,v['name'],v['position'])
			yield v
			i+=1
		self.db['course'].update_one({'_id':course_id},{'$set':{'lesson_crawl':'Done'}})

