# Scrapy settings for sinanews project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sinanews'

SPIDER_MODULES = ['sinanews.spiders']
NEWSPIDER_MODULE = 'sinanews.spiders'

# DOWNLOAD_TIMEOUT = 30

ITEM_PIPELINES = {'sinanews.pipelines.SinanewsPipeline': 100}

# ITEM_PIPELINES = {
#     'myproject.pipelines.PricePipeline': 300,
#     'myproject.pipelines.JsonWriterPipeline': 800,
# }

LOG_LEVEL = 'WARNING'

DOWNLOAD_DELAY = 0.25

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sinanews (+http://www.yourdomain.com)'
