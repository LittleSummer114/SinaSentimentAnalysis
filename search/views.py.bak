#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SearchForm
import MySQLdb
import json
import urllib2
import chardet

# Create your views here.

# 检索页面
def search_index(request):
    # return render(request, 'search\\index.html')
    if request.method == 'POST':# 当提交表单时
        form = SearchForm(request.POST)
        if form.is_valid():
            # results = 'You just sent %s' % form
            search_info = form.cleaned_data['search_info']
            print search_info

            # open database
            conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
            cursor = conn.cursor()
            conn.select_db('topicdemo')
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            sql_str = "select * from topic_list where topic_name = '%s'" % search_info.encode('utf-8')
            cursor.execute(sql_str)
            results = cursor.fetchone()
            if results:
                print urllib2.quote(search_info.encode('utf-8'))


                topic_id = results[0]
                return HttpResponseRedirect(reverse('topic:topicPage')+"?tid="+json.dumps(topic_id))
            else:
                print type(search_info)
                print urllib2.quote(search_info.encode('gb2312'))
                pass
                # 直接搜索查不到
                # 搜关键词，产生相关话题

                # 如果还是找不到，就告诉用户再等等，然后爬取数据
                    # 1.运行爬虫 2.调用algorithm
    # 传输字典
    context_dict = {}

    # open database
    conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
    cursor = conn.cursor()
    conn.select_db('topicdemo')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # sql_str = "select top 3 * from topic_list order by id desc"
    # cursor.execute(sql_str)
    # res = cursor.fetchone()

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


    return render(request, 'search/search.html')

# 检索页面
def search_result(request):
    return render(request, 'search\\classification.html')

# 话题列表页面
# def classification(request):
#     return render(request, 'search\\classification.html')

# 介绍页面
def introduction(request):
    return render(request, 'search\\introduction.html')


