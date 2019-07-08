# -*- coding: utf-8 -*-
import scrapy
import json
from mooc.items import CourseItem

class SearchSpider(scrapy.Spider):
	name = 'search'
	allowed_domains = ['www.icourse163.org']
	#start_urls = ['http://www.icourse163.org/']
	search_url="https://www.icourse163.org/web/j/mocSearchBean.searchMocCourse.rpc"
	query={
		"keyword":"python"
		,"pageIndex":1
		,"highlight":True
		,"orderBy":0
		,"stats":30
		,"pageSize":20
	}
	form_data={
		"csrfKey":"1"
		,"query":""
	}

	custom_settings={
		"ITEM_PIPELINES" :{
		   'mooc.pipelines.MongoPipeline': 300,
		   'mooc.pipelines.ItemStorePipeline': 310,
		}
		,"ITEM_STORE":"./"
	}

	# cmd: scrapy crawl search -a keyword=python
	def __init__(self,keyword=None,*args, **kwargs):
		super(SearchSpider, self).__init__(*args, **kwargs)
		if keyword is None:
			raise Exception('No keyword to search')
		self.keyword=keyword

	def start_requests(self):
		self.query['keyword']=self.keyword
		self.form_data['query']=json.dumps(self.query)
		#print(self.form_data)
		yield scrapy.FormRequest(
			url=self.search_url
			,formdata=self.form_data
			,cookies={"NTESSTUDYSI":self.form_data['csrfKey']}
			#,meta={'cookiejar':1}
			,callback=self.parse
		)

	def parse(self, response):
		body=json.loads(response.body)
		code=body.get('code',-1)
		msg=body.get('message','')
		result=body.get("result",{}) or {}
		pagination=result.get('pagination')
		totalHit=result.get('totalHit')
		records=result.get('result',[]) or []

		pageIndex=pagination.get('pageIndex')
		totalPage=pagination.get('totlePageCount')
		offset=pagination.get('offset')

		print("code:%s %s, records:%s(%s)/%s, page:%s/%s" % (code,msg,offset,len(records),totalHit,pageIndex,totalPage))
		if code!=0 or len(records)==0:
			return

		for record in records:
			r=record.get('mocCourseCardDto')
			item=CourseItem()

			item['my_type']='course'	# default store to spider name:search

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
			yield item

		if pageIndex<totalPage:
			self.query['pageIndex']=pageIndex+1
			self.form_data['query']=json.dumps(self.query)
			yield scrapy.FormRequest(
				url=self.search_url
				,formdata=self.form_data
				,callback=self.parse
				#,dont_filter=True
			)

