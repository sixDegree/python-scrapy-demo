# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import json
import scrapy
from mooc.items import CategoryItem,CourseItem,PaginationItem

class CategorySpiderMiddleware(object):
    course_url="https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc"
    form_data={
        'categoryId': "-1"
        ,'type': "30"
        ,'orderBy': "0"
        ,'pageIndex': "1"
        ,'pageSize': "20"
    }
    def process_spider_output(self, response, result, spider):
        if spider.name !='category':
            for i in result:
                yield i
                
        for i in result:
            # print("middleware:",i['id'])
            # print(type(i))
            if isinstance(i,CourseItem):
                i['my_type']='course'
                yield i
            elif isinstance(i,CategoryItem):
                i['my_type']='category'
                yield i 
                self.form_data['categoryId']=str(i['id'])
                self.form_data['pageIndex']="1"
                self.form_data['csrfKey']=spider.csrfKey
                yield scrapy.FormRequest(
                    url=self.course_url
                    ,formdata=self.form_data
                    #,cookies={"NTESSTUDYSI":csrfKey}
                    ,meta={
                        'pageIndex':1
                        ,'category_id':i['id']
                        ,'category_name':i['name']
                    }
                    ,callback=self.parse
                )
            elif isinstance(i,PaginationItem):
                #print('PaginationItem:',i)
                self.form_data['categoryId']=str(i['category_id'])
                self.form_data['pageIndex']=str(i['page_index'])
                self.form_data['csrfKey']=spider.csrfKey
                yield scrapy.FormRequest(
                    url=self.course_url
                    ,formdata=self.form_data
                    #,cookies={"NTESSTUDYSI":csrfKey}
                    ,meta={
                        'pageIndex':i['page_index']
                        ,'category_id':i['category_id']
                        ,'category_name':i['category_name']
                        ,'instance':'PaginationItem'
                    }
                    ,callback=self.parse
                )

    def parse(self,response):
        # print("url",response.url)
        # print('cookie:',response.request.headers.getlist('Cookie'))
        result=json.loads(response.body)
        code=result.get('code',-1)
        msg=result.get('message','')
        data=result.get('result',{}) or {}
        records=data.get('result',[]) or []
        pagination=data.get('pagination',{})
        pageIndex=pagination.get('pageIndex',0)
        totalPages=pagination.get('totlePageCount',0)
        print("code:%s %s\trecords:%s/%s\t\tpage:%s/%s\t\tcategory:%s" 
            % (code,msg
                ,len(records),pagination.get('totleCount',0)
                ,pageIndex,totalPages
                ,response.meta['category_name']
            )
        )
        if code==0:
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

            if response.meta.get('instance','')!='PaginationItem':
                for p in range(pageIndex+1,totalPages+1):
                #for p in range(pageIndex+1,3):
                    page=PaginationItem()
                    page['category_id']=response.meta['category_id']
                    page['category_name']=response.meta['category_name']
                    page['page_index']=p
                    yield page

            # below yield request doens't work! -- why?
            # nextPageIndex=pageIndex+1
            # if nextPageIndex<=totalPages:
            #     cur_form_data=self.form_data.copy()
            #     cur_form_data['pageIndex']=str(nextPageIndex)
            #     yield scrapy.FormRequest(
            #         url=self.course_url+"/123"
            #         ,formdata=cur_form_data
            #         #,cookies={"NTESSTUDYSI":csrfKey}
            #         ,meta={
            #             'pageIndex': nextPageIndex
            #             ,'category_id':response.meta['category_id']
            #             ,'category_name':response.meta['category_name']
            #         }
            #         ,callback=self.parse
            #     )


class MoocSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MoocDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
