# Scrapy settings for taobao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'taobao'
BOT_VERSION = '1.1'

SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'
DEFAULT_ITEM_CLASS = 'taobao.items.TaobaoItem'
USER_AGENT = '%s/%s' % ("linux","3.5.0-23-generic")

