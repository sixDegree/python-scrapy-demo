# -*- coding: utf-8 -*-
import scrapy
import json
import os
from hashlib import md5
from mooc.items import CategoryItem

class CategorySpider(scrapy.Spider):
	name = 'category'
	allowed_domains = ['www.icourse163.org']
	#start_urls = ['http://www.icourse163.org/']
	category_url="https://www.icourse163.org/web/j/mocCourseCategoryBean.getCategByType.rpc"
	form_data={
		"type":"4"		# 1
	}

	custom_settings={
		"SPIDER_MIDDLEWARES" : {
		   'mooc.middlewares.CategorySpiderMiddleware':543
		}
		,"ITEM_PIPELINES" : {
		   'mooc.pipelines.MongoPipeline': 300,
		   #'mooc.pipelines.ItemStorePipeline': 300
		}
		#,"ITEM_STORE":"./"
	}

	def start_requests(self):
		csrfKey=md5(os.urandom(24)).hexdigest()
		self.csrfKey=csrfKey
		self.form_data['csrfKey']=csrfKey
		yield scrapy.FormRequest(
			url=self.category_url
			,formdata=self.form_data
			,cookies={"NTESSTUDYSI":csrfKey}
			#,meta={'cookiejar':1}
			,callback=self.parse
		)

	def parse(self, response):
		result=json.loads(response.body)
		code=result.get('code',-1)
		msg=result.get('message','')
		records=result.get("result",[]) or []
		print("code:%s %s,records:%s" % (code,msg,len(records)))
		if code!=0:
			return
		return self.parse_item(records,None)

	def parse_item(self,records,parent_name):
		# print("parent:%s,children:%s" % (parent_name,len(records)))
		for r in records:
			item=CategoryItem()
			item['id']=r['id']
			item['name']=r['name']
			item['parent_id']=r['parentId']
			item['link_name']=r['linkName']
			item['type']=r['type']
			item['checked']=r['checked']
			item['weight']=r['weight']
			item['parent_name']=parent_name
			yield item
			children=r['children']
			if children:
				for i in self.parse_item(children,item['name']):
					yield i

