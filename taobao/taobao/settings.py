# Scrapy settings for taobao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'taobao'
BOT_VERSION = '1.1'

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'
DEFAULT_ITEM_CLASS = 'taobao.items.TaobaoItem'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
DOWNLOADER_MIDDLEWARES={
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':110,
        'taobao.middlewares.ProxyMiddleware':100,
        }
