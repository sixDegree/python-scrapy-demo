# -*- coding: utf-8 -*-
import scrapy
import json
from yeko_demo.items import CourseItem,UnitItem,LessonItem

# 'courses':{
# 	'uri':'/business/Teachers/detail/id/3313'
# 	,'return':'html'
# 	,'target':'select[name="cid"] > option'
# 	,'mapping':{'value':'_id','text':'name'}	# {srcKey:destKey}
# }
# ,'units':{
# 	'uri': '/business/Students/getMtCatsByCsId/cs_id/{course_id}'
# 	,'return':'json'
# 	,'mapping':{'id':'_id','cname':'title'}
# }
# ,'lessons':{
# 	'uri':'/business/Students/getMtsByMtCat/mt_cat/{unit_id}'
# 	,'return':'json'
# 	,'mapping':{'id':'_id','mt_name':'title','pdf':'doc'}
# }
		
class LessonSpider(scrapy.Spider):
	name = 'lesson'
	allowed_domains = ['class.121talk.cn']
	start_urls=['https://class.121talk.cn/business/Index']
	login_url='https://class.121talk.cn/business/Index/login'
	course_url='https://class.121talk.cn/business/Teachers/detail/id/3313'
	unit_url='http://class.121talk.cn/business/Students/getMtCatsByCsId/cs_id/'
	lession_url='https://class.121talk.cn/business/Students/getMtsByMtCat/mt_cat/'
    
	unit_cnt=0
	lesson_cnt=0
	course_limit=2

	# cmd: scrapy crawl lesson -a username=xxx -a password=xxxx
	def __init__(self,username=None,password=None,*args, **kwargs):
		super(LessonSpider, self).__init__(*args, **kwargs)
		if username is None or password is None:
			raise Exception('No username or password to login')
		self.username=username
		self.password=password

	# login - method1:
	def start_requests(self):
		print('start_request')
		yield scrapy.FormRequest(self.login_url
			,formdata={'username':self.username,'password':self.password}
			,callback=self.after_login)
    
    # login - method2:
	# def parse(self, response):
	# 	yield scrapy.FormRequest.from_response(response
	# 		,url=self.login_url
	# 		,formdata={'username':self.username,'password':self.password}
	# 		#,meta={'cookiejar':1}
	# 		,callback=self.after_login)

	def after_login(self,response):
		print('after_login')
		print('login:',response)
		print('login headers:',response.headers)
		print('login cookie:',response.request.headers.getlist('Cookie'))
		print('login Set-Cookie:',response.headers.getlist('Set-Cookie'))

		result=json.loads(response.body)
		print("login result:",result)
		if result.get('status'):
			yield scrapy.Request(self.course_url
			#,meta={'cookiejar':response.meta['cookiejar']}
			,callback=self.parse_course)
            
	def parse_course(self, response):
		#print('course headers:',response.headers)
		print('course cookie:',response.request.headers.getlist('Cookie'))
		records=response.xpath("//select[@name='cid']/option")
		print(len(records),self.course_limit)
		for i,record in enumerate(records):
			if i>=self.course_limit:
				print('course get to limit cnt!')
				break
			item=CourseItem()
			item['id']=record.xpath('./@value').extract_first()
			item['name']=record.xpath('./text()').extract_first()
			item['type']='course'
			yield item
			yield scrapy.Request(self.unit_url+item['id']
				,meta={'parent_id':item['id'],'path':item['name']
				#,'cookiejar':1
				}
				,callback=self.parse_unit)
            
	def parse_unit(self,response):
		#print('unit headers:',response.headers)
		print('unit cookie:',response.request.headers.getlist('Cookie'))
		parent_id=response.meta['parent_id']
		path=response.meta['path']
		result=json.loads(response.body)

		self.unit_cnt+=len(result)
		print("unit:",len(result),'total:',self.unit_cnt,'parent_id:',parent_id)

		for r in result:
			item=UnitItem()
			item['id']=r.get('id')
			item['name']=r.get('cname')
			item['type']='unit'
			item['parent_id']=parent_id
			yield item
			yield scrapy.Request(self.lession_url+item['id']
				,meta={'parent_id':item['id'],'path':path+"/"+item['name']
				#,'cookiejar':1
				}
				,callback=self.parse_lesson)
                     
	def parse_lesson(self,response):
		#print('lession headers:',response.headers)
		#print('lesson cookie:',response.request.headers.getlist('Cookie'))
		parent_id=response.meta['parent_id']
		path=response.meta['path']
		result=json.loads(response.body)

		self.lesson_cnt+=len(result)
		print("lesson:",len(result),'total:',self.lesson_cnt)

		for r in result:
			item=LessonItem()
			item['id']=r.get('id')
			item['name']=r.get('mt_name')
			item['doc']=r.get('pdf')
			item['type']='lesson'
			item['parent_id']=parent_id
			item['path']=path
			yield item

