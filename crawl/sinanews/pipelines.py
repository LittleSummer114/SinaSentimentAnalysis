# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import UrlsInfoItem, NewsInfoItem, CommmentInfoItem
import MySQLdb

class SinanewsPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.conn.select_db('topicdemo')

    def process_item(self, item, spider):
        if isinstance(item, UrlsInfoItem):
            self.cursor.execute("insert into crawl_url values(null,%s,%s)", (item['response_url'],item['topic_id']))
            self.conn.commit()

        if isinstance(item, NewsInfoItem):
            self.cursor.execute("insert into crawl_news values(null,%s,%s,%s,%s,%s,%s,%s)", (item['news_comment_id'],item['news_comment_channel'],item['news_time'],item['news_title'],item['mainbody'],item['response_url'],item['topic_id']))
            self.conn.commit()

        if isinstance(item, CommmentInfoItem):
            self.cursor.execute("insert into crawl_comment values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (item['news_comment_id'],item['time'],item['uid'], \
                                                                       item['wb_verified_type'], item['nick'], item['area'], item['against'],item['vote'],item['comment_body'],item['topic_id']))
            self.conn.commit()

        return item
