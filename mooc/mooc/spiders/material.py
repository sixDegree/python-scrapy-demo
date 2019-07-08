# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
import pymongo
import re
import json

class MaterialSpider(scrapy.Spider):
	name = 'material'
	allowed_domains = ['www.icourse163.org']
	#start_urls = ['http://www.icourse163.org/']
	meterial_url="https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr"
	form_data={
		'callCount':'1'
		,'scriptSessionId':'${scriptSessionId}190'
		,'c0-scriptName':'CourseBean'
		,'c0-methodName':'getLessonUnitLearnVo'
		,'c0-id':'0'
		,'c0-param0':'number:1212867249'	# contentId
		,'c0-param1':'number:3'				# contentType:1-video,2-exam(db.lesson),3-doc,4-attachment,5-test,6-chat
		,'c0-param2':'number:0'
		,'c0-param3':'number:1212471891'	# id
		,'batchId':'1'
	}

	custom_settings = {
		"SPIDER_MIDDLEWARES":{}
        ,"ITEM_PIPELINES" : {
		   'mooc.pipelines.MaterialFilePipeline':300
		   ,'mooc.pipelines.MaterialMongoPipeline':310
		}
		,"FILES_STORE":'../download/mooc'
		,"MEDIA_ALLOW_REDIRECTS":True
		,"DOWNLOAD_WARNSIZE":150*(2**20)	# 150M
    }

    # scrapy crawl material -a content_id=xxx -a content_type=3
	def __init__(self,course_id,content_type=None):
		self.mongo_uri=settings['MONGO_CONN_STR']
		self.mongo_db=settings.get('MONGO_DB')
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
		if course_id is None:
			raise Exception("No course_id")
		self.course_id=int(course_id)
		self.content_type=content_type

	def start_requests(self):
		query={
			'material_crawl':{'$ne':'Done'}
			,'contentId':{'$exists':True}
			#,'contentType':{'$ne':5}
			,'contentType':{'$nin':[6,5,1]}
			,'course_id': self.course_id	#1001894005
		}
		if self.content_type:
			query['contentType']=int(self.content_type)

		projection={
			'_id':1,'contentId':1,'contentType':1
			,'course_name':1,'chapter_name':1
			,'name':1,'position':1,'jsonContent':1
		}
		for record in self.db['material'].find(query,projection):

			if record.get('contentType')==4 and record.get("jsonContent"):
				#print("attachment:",jsonContent)
				jsonContent=record.get('jsonContent')
				if jsonContent.startswith('"'):
					jsonContent=jsonContent.strip('"')
				result=json.loads(jsonContent)
				#print(result)
				url="https://www.icourse163.org/course/attachment.htm?fileName="+result['fileName']+"&nosKey="+result['nosKey']
				# self.db['material'].update_one({'_id':record['_id']}
				# 	,{'$set':{'material_crawl':'Done','resource_url':url,'jsonContent':jsonContent}})
				resource={'url':url,'filename':result['fileName']}
				self.db['material'].update_one({'_id':record['_id']}
					,{'$set':{'resource':resource,'jsonContent':jsonContent}})
				# continue

			self.form_data['c0-param0']='number:'+str(record['contentId'])
			self.form_data['c0-param1']='number:'+str(record['contentType'])
			self.form_data['c0-param3']='number:'+str(record['_id'])
			yield scrapy.FormRequest(
				self.meterial_url
				,formdata=self.form_data
				,meta={
					'id':record['_id']
					,'name':record['name']
					,'position':record['position']
					,'contentType':record['contentType']
					,'chapter_name':record['chapter_name']
					,'course_name':record['course_name']
				}
				,callback=self.parse
			)

	def closed(self,reason):
		print('closed `material` spider:',reason)
		self.client.close()

	def parse(self, response):
		id=response.meta['id']
		name=response.meta['name']
		position=response.meta['position']
		contentType=response.meta['contentType']
		chapter_name=response.meta['chapter_name']
		course_name=response.meta['course_name']
		print("parse:",id,course_name,chapter_name,name,contentType)

		record={}
		if contentType==1:
			#print('video')
			ls=re.findall(r's\d+\.\w+=.*?;',response.body.decode('utf-8'))
			if not ls or len(ls)==0:
				print('fail:',response.body)
				self.db['material'].update_one({'_id':id}
					,{'$set':{'material_crawl':'Fail'}})
				return
			for item in ls:
				prop=re.split(r's\d+\.|;',item,maxsplit=2)[1]
				pairs=re.split(r'=|\?',prop)
				#print(pairs)
				if len(pairs)>=2 and pairs[1]!='null' and pairs[1]!='':
					record[pairs[0]]=pairs[1].replace('"','')
			
		elif contentType==3:
			#print('doc')
			ls=re.findall(r'(textOrigUrl|textUrl):"(http.*?)"',response.body.decode('utf-8'))
			if not ls or len(ls)==0:
				print('fail:',response.body)
				self.db['material'].update_one({'_id':id}
					,{'$set':{'material_crawl':'Fail'}})
				return
			for item in ls:
				record[item[0]]=item[1]

		elif contentType==4:
			#print('attachment')
			result=self.db['material'].find_one({'_id':id})
			record=result.get('resource')
			if not record:
				print('no resource for material:',name)
				self.db['material'].update_one({'_id':id}
					,{'$set':{'material_crawl':'Fail'}})
				return

		else:
			print('unknow contentType:',contentType)
			self.db['material'].update_one({'_id':id}
					,{'$set':{'material_crawl':'Fail'}})
			return

		#print(record)
		# self.db['material'].update_one({'_id':id}
		# 	,{'$set':{'material_crawl':'Done','resource':record}})
		item={}
		item["id"]=id
		item["name"]=name
		item["contentType"]=contentType
		item["chapter_name"]=chapter_name
		item["course_name"]=str(self.course_id)+"_"+course_name
		item['position']=position
		item['my_type']='resource'
		item['resource']=record
		yield item

		
		


