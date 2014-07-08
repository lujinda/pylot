# Scrapy settings for qq project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'qq'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['qq.spiders']
NEWSPIDER_MODULE = 'qq.spiders'
DEFAULT_ITEM_CLASS = 'qq.items.QqItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

