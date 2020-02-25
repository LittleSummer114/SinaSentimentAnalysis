#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from comment.models import CommentInfo
import MySQLdb
import json

# 评论页面
def commentIndex(request):
    context_dict = {}

    # tid
    cid = int(request.GET.get('cid', 0))
    context_dict['cid'] = cid


    # open database
    conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
    cursor = conn.cursor()
    conn.select_db('topicdemo')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    sql_str = "select * from crawl_comment where id = %d " % cid
    cursor.execute(sql_str)
    results = cursor.fetchone()

    myCommentInfo, created = CommentInfo.objects.get_or_create(comment_id = cid)
    myCommentInfo.comment_newsId = results[1].encode('utf-8')
    myCommentInfo.comment_time = results[2].encode('utf-8')
    myCommentInfo.comment_verify = int(results[4])
    myCommentInfo.comment_nick = results[5].encode('utf-8')
    myCommentInfo.comment_area = results[6].encode('utf-8')
    myCommentInfo.comment_against = int(results[7])
    myCommentInfo.comment_body = results[9].encode('utf-8')

    sql_str = "select * from preprocess_comment where id = %d " % cid
    cursor.execute(sql_str)
    results = cursor.fetchone()
    myCommentInfo.preprocess = results[2].encode('utf-8')
    myCommentInfo.postagging = results[3].encode('utf-8')
    myCommentInfo.syntactic = results[4]
    myCommentInfo.pv_word = results[5]
    myCommentInfo.pv_modifierword = results[6]
    myCommentInfo.keywords = results[7]
    myCommentInfo.tag = int(results[8])
    myCommentInfo.sentiment = int(results[9])
    myCommentInfo.mutisentiment = results[10]
    myCommentInfo.topic_id = int(results[1])

    sql_str = "select title, url from crawl_news where news_id = '%s' " % myCommentInfo.comment_newsId
    print sql_str
    cursor.execute(sql_str)
    results = cursor.fetchone()
    myCommentInfo.comment_news_title = results[0].encode('utf-8')
    myCommentInfo.comment_news_url = results[1].encode('utf-8')

    sql_str = "select topic_name from topic_list where id = %d " % myCommentInfo.topic_id
    cursor.execute(sql_str)
    results = cursor.fetchone()
    myCommentInfo.comment_topic_name = results[0].encode('utf-8')


    myCommentInfo.save()
    context_dict['comment_info'] = myCommentInfo


    keyword_list = eval(myCommentInfo.keywords)
    keywordstr_list = []
    if len(keyword_list):
        for i in range(0, len(keyword_list)):
            keywordstr_list.append(keyword_list[i][1].decode('utf-8'))
    context_dict['keyword_list'] = keywordstr_list

    cursor.close()
    conn.commit()
    conn.close()

    return render(request, 'comment/comment.html', context_dict)


# 将list中所有unicode转为utf-8
def _decode_list(data):
    rv = []
    for item in data:
        print item
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

# 将dict中所有unicode转为utf-8
def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

# 读取地址信息
def getParserTreeData(request):
    cid = int(request.GET.get('cid', 0))
    comment_data = CommentInfo.objects.get(comment_id = cid)
    temp_str = '%s' % comment_data.syntactic.encode('utf-8')
    temp = eval(temp_str)
    for i in range(0, len(temp)):
        temp[0]['cont'] = temp[0]['cont'].decode('utf-8')
    result = json.dumps(temp)
    return HttpResponse(result)

def getPieChartData(request):
    cid = int(request.GET.get('cid', 0))
    comment_data = CommentInfo.objects.get(comment_id = cid)
    tempsen = comment_data.mutisentiment.split(',')

    # tempsen = [2,4,6,0,5,5,12]
    piechart_list = [['乐',float(tempsen[0])],['好',float(tempsen[1])],['怒',float(tempsen[2])],['哀',float(tempsen[3])],['惧',float(tempsen[4])],['恶',float(tempsen[5])],['惊',float(tempsen[6])]]
    result = json.dumps(piechart_list)
    return HttpResponse(result)
