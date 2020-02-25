#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AddTopicForm
from algorithm.topic import TopicAnalysis
import MySQLdb
import json
import urllib2
import os

# Create your views here.


def categoryIndex(request):
    if request.method == 'POST':# 当提交表单时
        form = AddTopicForm(request.POST)
        if form.is_valid():
            # results = 'You just sent %s' % form
            search_name_info = form.cleaned_data['add_name_info']
            search_keywords_info = form.cleaned_data['add_keywords_info']
            search_startdate_info = form.cleaned_data['add_stratdate_info']
            search_enddate_info = form.cleaned_data['add_enddate_info']
            topic_date = search_startdate_info.replace('.', '-') + ' - ' + search_enddate_info.replace('.', '-')

            # print search_name_info, search_keywords_info
            # print urllib2.quote(search_name_info.encode('utf-8'))

            search_keywords_list = search_keywords_info.split(' ')
            search_keywords_str = ''
            search_keywords_urlcode = ''
            for i in range(0, len(search_keywords_list)):
                search_keywords_str += ('%s,' % search_keywords_list[i])
                search_keywords_urlcode += (ur'%s+' % urllib2.quote(search_keywords_list[i].encode('gb2312')))
                # print search_keywords_list[i]
                # print urllib2.quote(searcrh_keywords_list[i].encode('utf-8'))
            search_keywords_str = search_keywords_str[:-1]
            search_keywords_urlcode = search_keywords_urlcode[:-1]


            # 将话题名写入数据库
            conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
            cursor = conn.cursor()
            conn.select_db('topicdemo')
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            # 获取id号
            sql_count_str = "select count(*) from topic_list"
            cursor.execute(sql_count_str)
            result = cursor.fetchone()
            topic_id = result[0]
            print 'topic_id:',topic_id

            topic_type = int(form.cleaned_data['add_topic_type'])
            sql_str = "insert into topic_list values(%d,'%s','%s',%d,'%s',null,null,0)" % (topic_id, search_name_info.encode('utf-8'), search_keywords_str.encode('utf-8'), topic_type, topic_date)
            cursor.execute(sql_str)
            conn.commit()

            # topic_id = 0
            # 利用关键词运行爬虫
            search_name_urlcode = ur'%s' % urllib2.quote(search_name_info.encode('gb2312'))
            print search_keywords_urlcode
            topicinfo = '%s,%d,%s,%s' % (search_keywords_urlcode, topic_id, search_startdate_info, search_enddate_info)
            cmd_str = 'cd crawl &  \
                    scrapy crawl sinanewsurl -a topicinfo=%s' % (topicinfo)
            print cmd_str
            cmd_value = os.system(cmd_str)
            print 'cmd_value:',cmd_value

            # 分析数据
            # topic_id -= 1
            # test = TopicAnalysis(topic_id)

            # output_f = open(ur'crawl\crawl.bat', 'w')
            # # output_f.write('cd ..\crawl')
            # search_name_urlcode = ur'%s' % urllib2.quote(search_name_info.encode('gb2312'))
            # search_name_urlcode.replace('%','\\%')
            # print search_name_urlcode
            # output_f.write('scrapy crawl sinanewsurl -a category=%s\n'% search_name_urlcode)
            # output_f.write('pause\n')
            # output_f.close()
            #
            # os.system('crawl\\crawl.bat')

    return render(request, 'category\\category.html')


def getTopicList(request):
    # open database
    conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
    cursor = conn.cursor()
    conn.select_db('topicdemo')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    sql_str = "select * from topic_list"
    cursor.execute(sql_str)
    sql_results = cursor.fetchall()
    result_list = []
    for i in range(0, len(sql_results)):
        result_list.append([])
        result_list[i].append(sql_results[i][0])
        result_list[i].append(sql_results[i][1])
        result_list[i].append(sql_results[i][2])
        result_list[i].append(sql_results[i][3])
        result_list[i].append(sql_results[i][4])
        result_list[i].append(sql_results[i][5])
        result_list[i].append(sql_results[i][6])
        result_list[i].append(sql_results[i][7])

    result = json.dumps(result_list)
    return HttpResponse(result)