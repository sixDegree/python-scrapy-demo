# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yeko_demo.items import CommentItem
import json

# 'comments':{
#     'uri':'/business/Students/classRecords/p/{page}'
#     ,'return':'html'
#     ,'target':'table.list_table > tbody > tr'
#     ,'mapping':{'0.text':'time','1.span.a':'teacher','2.dl.dt.p':'lesson','2.dl.dd.p.a':'meterial_url','7.a':'content'}
#     ,'next_link':'div.page a.page_next'
#     ,'content_uri':'/business/Students/getMemo/id/{comment_id}'
#     ,'content_target':'table.fill_table textarea.big_textara'
# }

class CommentSpider(CrawlSpider):
    name = 'comment'
    allowed_domains = ['class.121talk.cn']
    start_urls = ['https://class.121talk.cn/business/Index']
    login_url='https://class.121talk.cn/business/Index/login'
    comment_url='https://class.121talk.cn/business/Students/classRecords'
    content_url='https://class.121talk.cn/business/Students/getMemo/id/'
    comment_cnt=0

    rules = (
        Rule(
            LinkExtractor(allow=r'/p/\d+',restrict_xpaths='//div[contains(@class,"page")]')
            , callback='parse_item', follow=True),
        # Rule(
        #     LinkExtractor(allow=r'/getMemo/id/\d+',restrict_xpaths='//table[@class="list_table"]/tbody/tr')
        #     ,callback='parse_content',follow=False),
    )

    # cmd: scrapy crawl comment -a username=xxx -a password=xxxx
    def __init__(self,username=None,password=None,*args, **kwargs):
        super(CommentSpider, self).__init__(*args, **kwargs)
        if username is None or password is None:
            raise Exception('No username or password to login')
        self.username=username
        self.password=password

    # don't use this:
    # def parse_start_url(self,response):
    #     print("do_login:",response.url)
    #     yield scrapy.FormRequest.from_response(response
    #         ,url=self.login_url
    #         ,formdata={'username':self.username,'password':self.password}
    #         #,meta={'cookiejar':1}
    #         ,callback=self.after_login)

    def start_requests(self):
        print('start_request')
        yield scrapy.FormRequest(self.login_url
            ,formdata={'username':self.username,'password':self.password}
            ,callback=self.after_login)
    
    def after_login(self,response):
        print('after_login')
        print('login:',response)
        print('login headers:',response.headers)
        print('login cookie:',response.request.headers.getlist('Cookie'))
        print('login Set-Cookie:',response.headers.getlist('Set-Cookie'))

        result=json.loads(response.body)
        print("login result:",result)
        if result.get('status'):
            yield scrapy.Request(self.comment_url
                #,meta={'cookiejar':response.meta['cookiejar']}
                )

    def parse_item(self, response):
        print("item:",response.url)
        records=response.xpath('//table[@class="list_table"]/tbody/tr')
        for r in records:
            item=CommentItem()
            content_link=r.xpath('./td[last()]//a/@href').get()
            if not content_link:
                continue
            item['id']=content_link.split('/')[-1]
            item['course']=r.xpath('./td[3]//dt//p[1]/text()').get()
            item['unit']=r.xpath('./td[3]//dt//p[2]/text()').get()
            item['lesson']=r.xpath('./td[3]//dt/p[3]/text()').get()
            item['doc']=r.xpath('./td[3]//dd//a/@href').get().split('/')[-1]
            item['teacher']=r.xpath('./td[2]//a/text()').get()
            item['teacher_id']=r.xpath('./td[2]//a/@href').get().split('/')[-1]
            item['time']=r.xpath('./td[1]/text()').get()
            # yield item
            yield scrapy.Request(self.content_url+item['id'],meta={'item':item},callback=self.parse_content)

    def parse_content(self,response):
        self.comment_cnt+=1
        print(self.comment_cnt,"content:",response.url)
        item=response.meta['item']
        #id=response.url.split('/')[-1]
        text=response.xpath('//table[contains(@class,"fill_table")]//textarea[@class="big_textara"]/text()').get()
        item['content']=text.strip()
        yield item


