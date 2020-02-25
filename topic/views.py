#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

from algorithm.EventEvolution import EventEvolution

# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from topic.models import TopicInfo
import MySQLdb
import json



# 话题页面
def topicIndex(request):
    # 传输字典
    context_dict = {}

    # tid
    tid = int(request.GET.get('tid', 0))
    context_dict['tid'] = tid

    # open database
    conn = MySQLdb.connect(host='116.56.143.18', user='cike', passwd='123456')
    cursor = conn.cursor()
    conn.select_db('topicdemo')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    sql_str = "select * from topic_list where id = %s " % tid
    cursor.execute(sql_str)
    res = cursor.fetchone()
    context_dict['tname'] = res[1]
    context_dict['keyword'] = res[2]
    TopicTypeNameList = ['财经', '社会', '民生', '军事', '政治']

    context_dict['type'] = TopicTypeNameList[int(res[3])]
    context_dict['date'] = res[4]
    context_dict['status'] = res[6]
    context_dict['influence'] = res[7]

    sql_str = "select * from result_topic where topic_id = %s " % tid
    cursor.execute(sql_str)
    results = cursor.fetchone()
    #print 'results: ',results[0]

    myTopicInfo, created = TopicInfo.objects.get_or_create(topic_id = tid)
    myTopicInfo.date_info = results[1].encode('utf-8')
    myTopicInfo.date_count = results[2].encode('utf-8')
    myTopicInfo.event_info = results[4].encode('utf-8')
    myTopicInfo.event_edge = results[5].encode('utf-8')
    myTopicInfo.event_node = results[6].encode('utf-8')
    myTopicInfo.enetiy_name = results[7].encode('utf-8')
    myTopicInfo.entity_event = results[8].encode('utf-8')
    myTopicInfo.entity_profile = results[9].encode('utf-8')
    myTopicInfo.heatmap_data = results[10].encode('utf-8')
    myTopicInfo.feature_frequent = results[11].encode('utf-8')
    myTopicInfo.feature_positive = results[12].encode('utf-8')
    myTopicInfo.feature_negative = results[13].encode('utf-8')
    myTopicInfo.sentiment_stream = results[14].encode('utf-8')
    myTopicInfo.sentiment_piechart = results[15].encode('utf-8')
    myTopicInfo.news_top = results[16].encode('utf-8')
    myTopicInfo.comment_best = results[17].encode('utf-8')
    myTopicInfo.comment_top = results[18].encode('utf-8')
    # myTopicInfo.comment_famous = results[19].encode('utf-8')
    # myTopicInfo.comment_question = results[20].encode('utf-8')
    myTopicInfo.area_data = results[21].encode('utf-8')
    myTopicInfo.save()

    return render(request, 'topic/topic.html',  context_dict)

# 读取事件信息
def getEventListData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    event_list = []
    tempsen = topic_data.event_info.split('\n')
    for i in range(0, len(tempsen)):
        event_list.append([])
        temp = tempsen[i].split('^')
        event_list[i].append(temp[0])
        event_list[i].append(temp[1])
        event_list[i].append(temp[2])
        event_list[i].append(temp[3])
        event_list[i].append(temp[4])
        event_list[i].append(temp[5])
    result = json.dumps(event_list)

    return HttpResponse(result)

# 读取地址信息
def getAreaData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    area_list = []
    tempsen = topic_data.area_data.split('\n')
    for i in range(0, len(tempsen)):
        area_list.append([])
        temp = tempsen[i].split(',')
        area_list[i].append(temp[0])
        area_list[i].append(temp[1])
        area_list[i].append(temp[2])
        area_list[i].append(temp[3])
    result = json.dumps(area_list)

    return HttpResponse(result)

# 高频特征词-字云图
def getFrequentFeatures(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    frequent_feature_list = []
    tempsen = topic_data.feature_frequent.split('\n')
    for i in range(0, len(tempsen)):
        frequent_feature_list.append([])
        temp = tempsen[i].split(',')
        frequent_feature_list[i].append(temp[0])
        frequent_feature_list[i].append(temp[1])

    result = json.dumps(frequent_feature_list)
    return HttpResponse(result)

# 高频特征词-正面
def getPositiveFeatures(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    frequent_feature_list = []
    tempsen = topic_data.feature_positive.split('\n')
    for i in range(0, len(tempsen)):
        frequent_feature_list.append([])
        temp = tempsen[i].split(',')
        frequent_feature_list[i].append(temp[0])
        frequent_feature_list[i].append(temp[1])

    result = json.dumps(frequent_feature_list)
    return HttpResponse(result)

# 高频特征词-负面
def getNegativeFeatures(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    frequent_feature_list = []
    tempsen = topic_data.feature_negative.split('\n')
    for i in range(0, len(tempsen)):
        frequent_feature_list.append([])
        temp = tempsen[i].split(',')
        frequent_feature_list[i].append(temp[0])
        frequent_feature_list[i].append(temp[1])

    result = json.dumps(frequent_feature_list)
    return HttpResponse(result)

# 获取实体热度图
def getHeatmapData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    enetiy_name_list = topic_data.enetiy_name.split('\n')
    date_info = topic_data.date_info.split('\n')
    heatmap_data_list = []
    tempsen = topic_data.heatmap_data.split('\n')
    for i in range(0, len(tempsen)):
        heatmap_data_list.append([])
        temp = tempsen[i].split(',')
        heatmap_data_list[i].append(temp[0])
        heatmap_data_list[i].append(temp[1])
        heatmap_data_list[i].append(temp[2])

    entity_profile_list = []
    tempsen = topic_data.entity_profile.split('\t')
    for i in range(0, len(tempsen)):
        entity_profile_list.append([])
        temp = tempsen[i].split(',')
        entity_profile_list[i].append(temp[0])
        entity_profile_list[i].append(temp[1])

    result_list = [enetiy_name_list,date_info,heatmap_data_list,entity_profile_list]
    result = json.dumps(result_list)
    return HttpResponse(result)

# 获得事件演变图
def getEventEvolutionData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    print 'getEventEvolutionData'

    enetiy_name_list = topic_data.enetiy_name.split('\n')

    node_list = []
    tempsen = topic_data.event_node.split('\n')
    for i in range(0, len(tempsen)):
        node_list.append([])
        print tempsen[i]
        temp = tempsen[i].split(',')
        node_list[i].append(temp[0])
        node_list[i].append(temp[1])
        node_list[i].append(temp[2])
        node_list[i].append(temp[3])
        node_list[i].append(temp[4])

    edge_list = []
    tempsen = topic_data.event_edge.split('\n')
    for i in range(0, len(tempsen)):
        edge_list.append([])
        temp = tempsen[i].split(',')
        edge_list[i].append(temp[0])
        edge_list[i].append(temp[1])
        edge_list[i].append(temp[2])

    entity_event_list = []
    tempsen = topic_data.entity_event.split('\n')
    for i in range(0, len(tempsen)):
        entity_event_list.append([])
        temp = tempsen[i].split(',')
        entity_event_list[i].append(temp[0])
        entity_event_list[i].append(temp[1])

    date_count_list = []
    tempsen = topic_data.date_count.split('\n')
    for i in range(0, len(tempsen)):
        date_count_list.append([])
        temp = tempsen[i].split(',')
        date_count_list[i].append(temp[0])
        date_count_list[i].append(temp[1])
        date_count_list[i].append(temp[2])


    result_list = [enetiy_name_list, node_list, edge_list, entity_event_list, date_count_list]
    result = json.dumps(result_list)
    return HttpResponse(result)

# 获取评论
# 获得最佳评论子集
def getBestCommentSet(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    best_comment_list = []
    tempsen = topic_data.comment_best.split('\n')
    for i in range(0, len(tempsen)):
        best_comment_list.append([])
        temp = tempsen[i].split(',')
        best_comment_list[i].append(temp[0])
        best_comment_list[i].append(temp[1])
        best_comment_list[i].append(temp[2])
        best_comment_list[i].append(temp[3])
        best_comment_list[i].append(temp[4])
        best_comment_list[i].append(temp[5])

    result = json.dumps(best_comment_list)
    return HttpResponse(result)

# 获得热门评论集
def getTopCommentSet(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    top_comment_list = []
    tempsen = topic_data.comment_top.split('\n')
    for i in range(0, len(tempsen)):
        top_comment_list.append([])
        temp = tempsen[i].split(',')
        top_comment_list[i].append(temp[0])
        top_comment_list[i].append(temp[1])
        top_comment_list[i].append(temp[2])
        top_comment_list[i].append(temp[3])
        top_comment_list[i].append(temp[4])
        top_comment_list[i].append(temp[5])

    result = json.dumps(top_comment_list)
    return HttpResponse(result)

# 获得微博名人评论集
def getFamousCommentSet(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    famous_comment_list = []
    tempsen = topic_data.comment_famous.split('\n')
    for i in range(0, len(tempsen)):
        famous_comment_list.append([])
        temp = tempsen[i].split(',')
        famous_comment_list[i].append(temp[0])
        famous_comment_list[i].append(temp[1])
        famous_comment_list[i].append(temp[2])

    result = json.dumps(famous_comment_list)
    return HttpResponse(result)

# 获得疑问集
def getQuestionCommentSet(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    question_comment_list = []
    tempsen = topic_data.comment_question.split('\n')
    for i in range(0, len(tempsen)):
        question_comment_list.append([])
        temp = tempsen[i].split(',')
        question_comment_list[i].append(temp[0])
        question_comment_list[i].append(temp[1])
        question_comment_list[i].append(temp[2])

    result = json.dumps(question_comment_list)
    return HttpResponse(result)

# 获取新闻
# 获得最佳评论子集
def getTopNewsSet(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    top_news_list = []
    tempsen = topic_data.news_top.split('\n')
    for i in range(0, len(tempsen)):
        top_news_list.append([])
        temp = tempsen[i].split(',', 5)
        top_news_list[i].append(temp[0])
        top_news_list[i].append(temp[1])
        top_news_list[i].append(temp[2])
        top_news_list[i].append(temp[3])
        top_news_list[i].append(temp[4])
        top_news_list[i].append(temp[5])

    result = json.dumps(top_news_list)
    return HttpResponse(result)

# 获取最新的报道
def getRecentNewsSet(request):
    recent_news_list = '测试'
    result = json.dumps(recent_news_list)
    return HttpResponse(result)

# 获取最佳社评
def getBestNewsSet(request):
    best_news_list = '测试'
    result = json.dumps(best_news_list)
    return HttpResponse(result)

# 获得情感流图
def getSentimentData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    sentiment_name = ['乐','好','怒','哀','惧','恶','惊']
    sentiment_piechart_list = []
    tempsen = topic_data.sentiment_piechart.split('\n')
    for i in range(0, len(tempsen)):
        sentiment_piechart_list.append([])
        sentiment_piechart_list[i].append(sentiment_name[i])
        sentiment_piechart_list[i].append(tempsen[i])

    sentiment_stream_list = []
    tempsen = topic_data.sentiment_stream.split('\n')
    for i in range(0, len(tempsen)):
        sentiment_stream_list.append([])
        temp = tempsen[i].split(',')
        for j in range(0, len(temp)):
            sentiment_stream_list[i].append(temp[j])
    result_list = [sentiment_piechart_list, sentiment_stream_list]
    result = json.dumps(result_list)

    return HttpResponse(result)

# 获得情感扇形图
def getPieChartData(request):
    tid = int(request.GET.get('tid', 0))
    topic_data = TopicInfo.objects.get(topic_id = tid)

    sentiment_name = ['乐','好','怒','哀','惧','恶','惊']
    sentiment_piechart_list = []
    tempsen = topic_data.sentiment_piechart.split('\n')
    for i in range(0, len(tempsen)):
        sentiment_piechart_list.append([])
        sentiment_piechart_list[i].append(sentiment_name[i])
        sentiment_piechart_list[i].append(tempsen[i])
    result = json.dumps(sentiment_piechart_list)
    return HttpResponse(result)

# 转到评论页面
def turnToCommentPage(request, cid):
    comment_id = int(cid)
    return HttpResponseRedirect(reverse('comment:commentPage')+"?cid="+json.dumps(comment_id))




