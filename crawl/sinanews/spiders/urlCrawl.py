#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'hdp'

import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib2
import MySQLdb

import time
from sinanews.items import UrlsInfoItem, NewsInfoItem, CommmentInfoItem



class DmozSpider(scrapy.spider.Spider):
    print 'test'
    name = "sinanewsurl"    #唯一标识，启动spider时即指定该名称
    allowed_domains = ["sina.com.cn"]
    # start_urls = [
    #      # "http://search.sina.com.cn/?c=news&q=%CE%BA%D4%F2%CE%F7&range=title&num=20&col=1_7&source=&from=&country=&size=&time=&a=&page=1&pf=2131425466&ps=2134309112&dpc=1"
    #     "http://search.sina.com.cn/?q=%CE%BA%D4%F2%CE%F7+%C6%CE%CC%EF&range=title&c=news&sort=time"
    # ]

    def __init__(self, topicinfo=None, *args, **kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        topicinfo_list = topicinfo.split(',')
        self.topic_urlcode = topicinfo_list[0]
        self.topic_id = int(topicinfo_list[1])

        print self.topic_urlcode
        print self.topic_id

        # self.start_urls = ['http://search.sina.com.cn/?c=news&q=%s&range=title&num=20&col=1_7&source=&from=&country=&size=&time=&a=&page=1&pf=2131425466&ps=2134309112&dpc=1' % category]
        self.start_urls = ['http://search.sina.com.cn/?q=%s&range=all&c=news&sort=time&num=20&col=&source=&from=&country=&size=&time=&a=&page=1&ps=2134309112&dpc=1' % self.topic_urlcode]
        # self.start_urls = ['http://search.sina.com.cn/?q=%s&range=title&c=news&sort=time&num=20&col=&source=&from=&country=&size=&time=&a=&page=1&ps=2134309112&dpc=1' % self.topic_urlcode]

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.conn.select_db('topicdemo')

        self.output_f = open(ur'problem.txt', 'w')

    def parse(self, response):
        page = 1
        sel = HtmlXPathSelector(response)

        news_info = sel.xpath('//*[@id="result"]/div[1]/text()').extract()[0]
        news_total_num = filter(lambda x:x.isdigit(),news_info)
        news_total_page = int(news_total_num)/20 + 1
        # print self.start_urls
        print news_total_num, news_total_page

        # page = 21
        # news_total_page = 30
        while page <= news_total_page:
            url= 'http://search.sina.com.cn/?q=%s&range=all&c=news&sort=time&num=20&col=&source=&from=&country=&size=&time=&a=&page=%d&ps=2134309112&dpc=1' % (self.topic_urlcode, page)
            print "page:",page
            # time.sleep(0.2)
            yield scrapy.http.Request(url,callback=self.parse_url)
            page += 1

    # 爬取每一页的url
    def parse_url(self, response):
        sel = HtmlXPathSelector(response)
        for i in range(20):
            try:
                url_xpath = '//*[@id="result"]/div[%d]/div/h2/a/@href' % (i + 4)
                news_url = sel.xpath(url_xpath).extract()[0].decode('UTF-8')
            except:
                try:
                    url_xpath = '//*[@id="result"]/div[%d]/h2/a/@href' % (i + 4)
                    news_url = sel.xpath(url_xpath).extract()[0].decode('UTF-8')
                except:
                    try:
                        url_xpath = '//*[@id="result"]/div[%d]/h2/a' % (i + 4)
                        news_url = sel.xpath(url_xpath).extract()[0].decode('UTF-8')
                    except:
                        news_url = ''
            # print i,news_url
            # print type(news_url)

            # 爬取正文和评论
            if news_url != '':
                url_info = {'response_url':news_url, 'topic_id':self.topic_id}
                # yield UrlsInfoItem(url_info)
                self.cursor.execute("insert into crawl_url values(null,%s,%s)", (news_url,self.topic_id))

                yield scrapy.http.Request(news_url, callback=self.parse_news)
                # break
        self.conn.commit()

    # 爬取正文和评论
    def parse_news(self, response):
        response_str = '%s' % response
        response_url = response_str.split(' ')[-1][:-1]

        sel = HtmlXPathSelector(response)

        # title
        title_xpath_list = ['//*[@id="artibodyTitle"]/text()', '//*[@id="main_title"]/text()', '//*[@id="content_body"]/div[1]/div[1]/text()']
        news_title = ''
        for i in range(0, len(title_xpath_list)):
            try:
                news_title = sel.xpath(title_xpath_list[i]).extract()[0]
                break
            except:
                continue
        # if news_title == '':
            # print 'news_title', response
            # self.output_f.write('news_title:%s\n' % response)
        # print news_title

        time_xpath_list = ['//*[@id="wrapOuter"]/div/div[4]/span/text()','//*[@id="page-tools"]/span/span[1]/text()','//*[@id="content_body"]/div[1]/span[1]/text()','//*[@id="navtimeSource"]/text()','//*[@id="pub_date"]/text()']
        news_time = ''
        for i in range(0, len(time_xpath_list)):
            try:
                news_time = sel.xpath(time_xpath_list[i]).extract()[0].strip()
                if i == 0:
                    news_time = news_time.split('\n')[0].strip()
                break
            except:
                continue
        # if news_time == '':
            # print 'news_time', response
            # self.output_f.write('news_time:%s\n' % response)
        # print news_time


        # mainbody
        mainbody_full_xpath_list = ['//*[@id="artibody"]/p/text()','//*[@id="content_body"]/div[2]/div[1]/p/text()']
        mainbody_full = ''
        for i in range(0, len(mainbody_full_xpath_list)):
            try:
                mainbody_full = sel.xpath(mainbody_full_xpath_list[i]).extract()
                break
            except:
                continue
        mainbody = ''
        for p in mainbody_full:
            mainbody = mainbody + '\n' + p.strip()
        # print mainbody

        # comment
        news_comment_url = ''
        for i in [0, 1, -1, -2, -3, 2, -4, 3, -5, 4, 5, 6, 7, -6]:
            comment_xpath_n = '/html/head/meta[%d]/@name' % (i + 15)
            try:
                if sel.xpath(comment_xpath_n).extract()[0] == 'comment':
                    comment_xpath_c = '/html/head/meta[%d]/@content' % (i + 15)
                    news_comment_url = sel.xpath(comment_xpath_c).extract()[0].decode('UTF-8')
                    break
                else:
                    continue
            except:
                continue

        news_comment_id = ''
        news_comment_channel = ''
        if news_comment_url != '':
            news_comment_id = news_comment_url[3:]
            news_comment_channel = news_comment_url[:2]
        else:
            # print 'comment_url', response
            if response_str.find('/pl/') != -1:
                news_comment_channel = 'pl'
            elif response_str.find('/zl/') != -1:
                news_comment_channel = 'kj'
            elif response_str.find('/sf/') != -1:
                news_comment_channel = 'sf'
            elif response_str.find('video.') != -1:
                news_comment_channel = 'video'
            elif response_str.find('slide.') != -1:
                news_comment_channel = 'slide'

            if news_comment_channel != 'slide' and news_comment_channel != 'video':
            # if news_comment_channel == 'pl' and news_comment_channel != 'sf':
                news_comment_id = (response_str.split('/')[-1]).split('.')[0]
            # print news_comment_channel, news_comment_id

            self.output_f.write('comment_url:%s,%s,%s\n' % (response,news_comment_channel, news_comment_id))

        if news_comment_id != '' and news_title != '':
            # news_info = {
            #     'news_comment_id':news_comment_id,
            #     'news_comment_channel':news_comment_channel,
            #     'news_time':news_time.encode('utf-8'),
            #     'news_title':news_title.encode('utf-8'),
            #     'mainbody':mainbody.encode('utf-8'),
            #     'response_url':response_url,
            #     'topic_id':self.topic_id
            # }
            # yield NewsInfoItem(news_info)
            self.cursor.execute("insert into crawl_news values(null,%s,%s,%s,%s,%s,%s,%s)", (news_comment_id,news_comment_channel,news_time.encode('utf-8'),news_title.encode('utf-8'),mainbody.encode('utf-8'),response_url,self.topic_id))
            self.conn.commit()
        else:
            self.output_f.write('%s\t%s\t%s\t%s\n' % (response,news_title,news_time,news_comment_id))


        # 获取评论
        cmntlist=[]
        page = 1
        while((page==1) or (cmntlist != [])):
            # get url
            url="http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel="+news_comment_channel+"&newsid="+news_comment_id+"&group=&compress=0&ie=gbk&oe=gbk&page="+str(page)+"&page_size=100"
            # print url

            url_contain=urllib2.urlopen(url, timeout = 10).read()
            b='={'
            after = url_contain[url_contain.index(b)+len(b)-1:]
            # change
            after=after.replace('null','None')
            text=eval(after)

            if 'cmntlist' in text['result']:
                cmntlist=text['result']['cmntlist']
            else:
                cmntlist=[]


            if cmntlist != []:
                content=''
                for status_dic in cmntlist:
                    if status_dic['uid']!='0':
                        # verified_type
                        wb_verified_type = '0'
                        config = status_dic['config']
                        is_verified = config.find('wb_verified_type')
                        if is_verified != -1:
                            try:
                                wb_verified_type = config[is_verified + 17]
                            except:
                                wb_verified_type = '0'

                        # comment
                        comment_body = status_dic['content'].decode('unicode-escape').encode('utf-8')
                        area = status_dic['area'].decode('unicode-escape').encode('utf-8')
                        nick = status_dic['nick'].decode('unicode-escape').encode('utf-8')
                        # content = content + news_comment_id + '\t' + response_url + '\t' + status_dic['time'] + '\t' + status_dic['uid'] + '\t' + wb_verified_type + \
                        #           '\t'+ nick +'\t'+ area +'\t' + status_dic['against']+ '\t' +status_dic['vote']+'\t'\
                        #           + '' + '\n'

                        # comment_info = {
                        #     'news_comment_id':news_comment_id,
                        #     'time':status_dic['time'].encode('utf-8'),
                        #     'uid':status_dic['uid'].encode('utf-8'),
                        #     'wb_verified_type':wb_verified_type.encode('utf-8'),
                        #     'nick':nick,
                        #     'area':area,
                        #     'against':status_dic['against'],
                        #     'vote':status_dic['vote'].encode('utf-8'),
                        #     'comment_body':comment_body,
                        #     'topic_id':self.topic_id
                        # }
                        # yield CommmentInfoItem(comment_info)
                        self.cursor.execute("insert into crawl_comment values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (news_comment_id.encode('utf-8'),status_dic['time'].encode('utf-8'),status_dic['uid'].encode('utf-8'), \
                                                                       wb_verified_type.encode('utf-8'), nick, area, status_dic['against'].encode('utf-8'),status_dic['vote'].encode('utf-8'),comment_body,self.topic_id))

            page=page+1

        self.conn.commit()
