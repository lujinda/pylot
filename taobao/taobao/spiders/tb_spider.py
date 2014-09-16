#coding:utf8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import urllib

keyWord=urllib.quote("丝袜 裤袜 防勾丝".decode('utf8').encode("gbk"))
price=urllib.quote('[28,30]')
userName="".decode("utf8")
baseUrl="http://s.taobao.com/search?spm=a230r.1.16.6.wQi07i&q=%s&tab=all&style=list&filter=reserve_price%s&fs=0&promote=0&bcoffset=4&s="%(keyWord,price)

class tbSpider(BaseSpider):
    nowpage=0
    name="taobao"
    allowed_domains=['taobao.com']
    start_urls=[
            baseUrl+'0',
            ]

    def parse(self,response):
        site=HtmlXPathSelector(response)
        size=str(site.select('//div[@class="pagination"]/@bx-config').re('size:(\d+)')[0])
        self.nowpage+=int(size)
        content=site.select('//div[@class="tb-content"]/div/div')
        for item in content:
            title=item.select('div[@class="col title"]')
            user=title.select('div[@class="seller"]/a/text()').extract()[0].strip()
            if user!=userName:
                continue
            name=title.select('h3/a/@title').extract()[0].strip()
            url=title.select('h3/a/@href').extract()[0]

            print user,name

        yield Request(baseUrl+str(self.nowpage),callback=self.parse)
        

