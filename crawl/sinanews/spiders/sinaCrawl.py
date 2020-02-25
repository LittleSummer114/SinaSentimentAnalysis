#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'hdp'

import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib2
import MySQLdb
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

projectpath='C:\\Users\\DongpingHuang\\Desktop\\sinanews\\data\\'

class DmozSpider(scrapy.spider.Spider):
    name = "sinanews"    #唯一标识，启动spider时即指定该名称
    allowed_domains = ["sina.com.cn"]
    start_urls = [
         "http://finance.sina.com.cn/stock/y/2016-01-07/doc-ifxnkkux0922639.shtml"
    ]

    def __init__(self, topicinfo=None, *args, **kwargs):

        topicinfo_list = topicinfo.split(',')
        self.topic_urlcode = topicinfo_list[0]
        self.topic_id = int(topicinfo_list[1])

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.conn.select_db('newsdemo')

        self.output_f = open(ur'problem.txt', 'w')

    def parse(self, response):
        self.cursor.execute("select * from crawl_url")
        results = self.cursor.fetchall()
        count = 0
        for url in results:
            # print url[1]
            print count
            count += 1
            yield scrapy.http.Request(url[1], callback=self.parse_news)

        # 爬取正文和评论
    def parse_news(self, response):
        response_str = '%s' % response
        response_url = response_str.split(' ')[-1][:-1]

        # news_info = {'response_url':response_url,'topic_id':self.topic_id}
        # yield SinanewsItem(news_info)
        #
        # # self.cursor.execute("insert into crawl_news values(null,null,null,null,null,null,%s,%s)", (response_url,self.topic_id))
        # # self.conn.commit()
        #
        # return


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
                            wb_verified_type = config[is_verified + 17]

                        # comment
                        comment_body = status_dic['content'].decode('unicode-escape').encode('utf-8')
                        area = status_dic['area'].decode('unicode-escape').encode('utf-8')
                        nick = status_dic['nick'].decode('unicode-escape').encode('utf-8')
                        # content = content + news_comment_id + '\t' + response_url + '\t' + status_dic['time'] + '\t' + status_dic['uid'] + '\t' + wb_verified_type + \
                        #           '\t'+ nick +'\t'+ area +'\t' + status_dic['against']+ '\t' +status_dic['vote']+'\t'\
                        #           + '' + '\n'

                        self.cursor.execute("insert into crawl_comment values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (news_comment_id.encode('utf-8'),status_dic['time'].encode('utf-8'),status_dic['uid'].encode('utf-8'), \
                                                                       wb_verified_type.encode('utf-8'), nick, area, status_dic['against'].encode('utf-8'),status_dic['vote'].encode('utf-8'),comment_body,self.topic_id))
            page=page+1

        self.conn.commit()

