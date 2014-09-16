#!/usr/bin/env python
def getProxyList():
    import urllib2
    from lxml import etree
    url="http://www.site-digger.com/html/articles/20110516/proxieslist.html"
    page=urllib2.urlopen(url).read()
    root=etree.HTML(page)
    table=root.xpath('//table[@id="proxies_table"]/tbody/tr')
    proxy_list=[]
    for tr in table:
        if tr[1].text.startswith('Anony') and int(tr[3].text)<2:
            proxy_list.append(tr[0].text)


    return proxy_list

if __name__=="__main__":
    print getProxyList()

