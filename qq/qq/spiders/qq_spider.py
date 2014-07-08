from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import re

from qq.items import QqItem
class QqSpider(BaseSpider):
    name="qq"
    allowed_domains=[]
    start_urls=[
            "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html",
            ]
    count=0
    items=[]
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//div[@class=\"list-box \"]/div[@class=\"list-item clearfix\"]')
        
        for site in sites:
            item=QqItem()
            try:
                item['name']=site.select("div//h3/a/text()").extract()[0]
                item['price']=site.select("div//b[@class=\"price-type\"]/text()").extract()[0]
            except:
                break
            print item['name'],item['price']
            self.items.append(item)

        try:
            nexturl=sites.select("//div[@class=\"page-box\"]//a[@class=\"next\"]/@href")[0].extract()
        except:
            return self.items
        nexturl='http://detail.zol.com.cn'+nexturl
        return Request(url=nexturl,callback=self.parse,errback=self.call_erro)
        
    def call_erro(self,_):
        print "callback error"
        return None
        

