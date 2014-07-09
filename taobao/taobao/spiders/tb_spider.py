from scrapy.spider import BaseSpider

class tbSpider(BaseSpider):
    name="taobao"
    allowed_domains=['localhost']
    start_urls=[
            'http://localhost',
            ]

    def parse(self,response):
        print response
