import scrapy
from scrapy.crawler import CrawlerProcess

from sinanews.spiders.urlCrawl import DmozSpider

class MySpider(scrapy.Spider):
    # Your spider definition
    process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(DmozSpider)
    process.start()

if __name__ == "__main__":
    MySpider()
