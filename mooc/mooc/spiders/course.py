# -*- coding: utf-8 -*-
import scrapy
import json
import os
from hashlib import md5
# import urllib.parse
# import requests

from mooc.items import CourseItem

class CourseSpider(scrapy.Spider):
	name = 'course'
	allowed_domains = ['www.icourse163.org']
	#start_urls = ['https://www.icourse163.org/category/all']
	course_url="https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc"
	page_data={
		# 'categoryId': -1
		# ,'type': 30
		# ,'orderBy': 0
		# ,'pageIndex': 1
		# ,'pageSize': 20
		'categoryId': "-1"		 #"1001043032"
		,'type': "30"
		,'orderBy': "0"
		,'pageIndex': "1"
		,'pageSize': "20"
	}
	no_record_cnt=0

	custom_settings={
		"ITEM_PIPELINES" :{
		   'mooc.pipelines.MongoPipeline': 300,
		   #'mooc.pipelines.ItemStorePipeline': 300,
		}
		#"ITEM_STORE":"./"
	}

	def start_requests(self):
		csrfKey=md5(os.urandom(24)).hexdigest()
		self.page_data['csrfKey']=csrfKey
		# yield scrapy.Request(
		# 	url=self.course_url
		# 	,method='POST'
		# 	,body=urllib.parse.urlencode(self.page_data)
		# 	,headers={'Content-Type':'application/x-www-form-urlencoded'}
		# 	,cookies={"NTESSTUDYSI":csrfKey}
		# 	,meta={'cookiejar':1}
		# 	,callback=self.parse
		# )
		yield scrapy.FormRequest(
			url=self.course_url
			,formdata=self.page_data
			,cookies={"NTESSTUDYSI":csrfKey}
			#,meta={'cookiejar':1}
			,callback=self.parse
		)
		# r=requests.request('POST',self.course_url,data=self.page_data,cookies={"NTESSTUDYSI":csrfKey})
		# print(r.status_code,r.reason)					# 200 OK
		# print(r.text)

	def parse(self, response):
		print("url",response.url)
		print('cookie:',response.request.headers.getlist('Cookie'))
		# print('Set-Cookie:',response.headers.getlist('Set-Cookie'))
		# print("request headers:",response.request.headers)
		# print("request body:",response.request.body)
		# print("response headers:",response.headers)
		result=json.loads(response.body)
		code=result.get('code',-1)
		print("code:%s %s" % (code,result.get("message","")))
		if code==0 : 
			#records=result["result"]["result"]
			p=result["result"]["pagination"]
			print("pageIndex:%s,pageSize:%s,totalPage:%s,totalCount:%s" 
				% (p["pageIndex"],p["pageSize"],p["totlePageCount"],p["totleCount"]))
			i=int(p["pageIndex"])
			while i<=int(p["totlePageCount"]):
			#while i<=3:
				# print(i)
				self.page_data["pageIndex"]=str(i)
				yield scrapy.FormRequest(
						url=self.course_url
						,formdata=self.page_data
						,callback=self.parse_item
						,meta={
							'pageIndex':i
							,'category_id':-1
							,'category_name':None
						}
						,dont_filter=True
					)
				i+=1

	def parse_item(self,response):
		if response.meta['pageIndex']==1:
			print("get 1 index----")
		# print("url",response.url)
		#print("parse pageIndex:",response.meta['pageIndex'])
		#print('cookie:',response.request.headers.getlist('Cookie'))
		result=json.loads(response.body)
		code=result.get('code',-1)
		#print("code:%s %s" % (code,result.get("message","")))
		if code==0 : 
			records=result["result"]["result"]
			if not records:
				self.no_record_cnt+=1
				print("no records")
				return
			print("len:",len(records),self.no_record_cnt,response.meta['pageIndex'])
			for r in records:
				item=CourseItem()
				item['id']=r['id']
				item['name']=r['name']
				item['short_name']=r['shortName']
				item['channel']=r['channel']
				item['status']=r['status']
				item['learner_count']=r['learnerCount']
				item['video_id']=r['videoId']
				item['video_url']=r['VideoUrl']

				term=r['termPanel']
				item['content']=term['jsonContent']
				item['lector']=term['lectorPanels']
				item['term']={
					'id': term['id']
					,'course_id':term['courseId']
					,'from_term_id':term['fromTermId']
					,'start_time':term['startTime']
					,'end_time':term['endTime']
					,'duration':term['duration']
					,'publish_status':term['publishStatus']
					,'enroll_count':term['enrollCount']
					,'lessons_count':term['lessonsCount']
				}
				school=r['schoolPanel']
				item['school']={
					'id':school['id']
					,'name':school['name']
					,'short_name':school['shortName']
				}
				item['tag']=r['mocTagDtos']
				item['product_type']=r['productType']
				item['course_type']=r['courseType']
				item['gmt_create']=r['gmtCreate']
				item['publish_time']=r['firstPublishTime']
				item['page_index']=response.meta['pageIndex']
				item['category_id']=response.meta['category_id']
				item['category_name']=response.meta['category_name']
				yield item
		

