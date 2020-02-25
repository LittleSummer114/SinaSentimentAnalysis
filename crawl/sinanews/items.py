# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SinanewsItem(Item):
    # define the fields for your item here like:
    # name = Field()

    response_url = Field()
    topic_id = Field()

class UrlsInfoItem(Item):
    response_url = Field()
    topic_id = Field()

class NewsInfoItem(Item):
    news_comment_id = Field()
    news_comment_channel = Field()
    news_time = Field()
    news_title = Field()
    mainbody = Field()
    response_url = Field()
    topic_id = Field()

class CommmentInfoItem(Item):
    news_comment_id = Field()
    time = Field()
    uid = Field()
    wb_verified_type = Field()
    nick = Field()
    area = Field()
    against = Field()
    vote = Field()
    comment_body = Field()
    topic_id = Field()