from getproxy import getProxyList
import random

class ProxyMiddleware(object):
    def process_request(self,request,spider):
        pass
#        proxy_list=getProxyList()
#        request.meta['proxy']="http://"+random.choice(proxy_list)
