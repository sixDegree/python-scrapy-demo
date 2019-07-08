# -*- coding: utf-8 -*-
import scrapy
import re
import json
from douban_demo.items import MovieItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    #start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0']
    
    base_url='https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend'
    page_limit=20
    page_start=0

    def start_requests(self):
    	start_url=self.base_url+"&page_limit="+str(self.page_limit)+"&page_start="+str(self.page_start)
    	return [scrapy.Request(start_url,callback=self.parse)]

    def parse(self, response):
    	print(response.url)
    
    	result=json.loads(response.body)
    	subjects=result.get('subjects')
    	if len(subjects)>0:
    		for subject in subjects:
    			# print(subject)
    			yield MovieItem(subject)
    		# get page_start
    		match=re.search(r'page_start=\d+',response.url)
    		page_start=int(match.group(0).split('=')[-1])+self.page_limit
    		next_url=self.base_url+"&page_limit="+str(self.page_limit)+"&page_start="+str(page_start)
    		yield scrapy.Request(next_url,callback=self.parse)


        
