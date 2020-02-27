#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def CreateDataBase():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456')

    # creat database
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # creat database
    # cursor.execute("create database if not exists topicdemo charset utf8 COLLATE utf8_general_ci")

    # select database
    conn.select_db('topicdemo')
    # cursor.execute("create table preprocess_news (id int primary key, topic_id int, news_body text, pos_tagging text) ")
    # cursor.execute("create table preprocess_comment (id int primary key, topic_id int, comment_body text, pos_tagging text, syntactic text, pv_word text, pv_modifier_word text, keywords text, tag_label int, sentiment_value int) ")
    # cursor.execute("create table result_topic (topic_id int primary key, date_info text, date_count text, status_info text, event_info text, event_edge text, event_node text, entity_name text, entity_event text, entity_profile text,  heatmap_data text, feature_frequent text, feature_positive text, feature_negative text, sentiment_stream text, sentiment_piechart text, news_top text, comment_best text, comment_top text, comment_famous text, comment_question text, area_info text)")
    # cursor.execute("alter table result_topic add column status_info text;")
    # cursor.execute("alter table topicdemo.result_topic change column enetiy_name entity_name text;")
    cursor.execute("alter table result_topic add column cd_value text;")
    cursor.execute("alter table result_topic add column er_value text;")
    cursor.execute("alter table result_topic add column tp_value text;")
    cursor.execute("alter table result_topic add column tem_value text;")

    # cursor.execute("alter table crawl_news change column id id int auto_increment primary key;")
    # cursor.execute("alter table crawl_comment change column id id int auto_increment primary key;")

    # cursor.execute("create table temp_url select * from crawl_url")
    # cursor.execute("create table temp_news select * from crawl_news")
    # cursor.execute("create table temp_comment select * from crawl_comment")


    # cursor.execute("create table crawl_comment(id int auto_increment primary key, news_id varchar(25), time varchar(25), uid varchar(25), wb_verified_type int, nick varchar(100), area varchar(50), against int, vote int, comment_body varchar(2550), topic_id int)")
    # cursor.execute("create table crawl_news(id int auto_increment primary key, news_id varchar(25), news_channel varchar(8), time varchar(50), title varchar(255), news_body text, url varchar(255), topic_id int)")
    # cursor.execute("create table crawl_url(id int auto_increment primary key, url varchar(255), topicid int)")
    # cursor.execute("alter table preprocess_comment add column mutisentiment_value text;")


    # cursor.execute("create table crawl_url select * from newsdemo.crawl_url")
    # cursor.execute("create table crawl_news select * from newsdemo.crawl_news")
    # cursor.execute("create table crawl_comment select * from newsdemo.crawl_comment")
    # cursor.execute("create table syntactic_train select * from sinanews.train")
    # cursor.execute("create table topic_list select * from newsdemo.topic_list")


    # cursor.execute("alter table topic_list add column date varchar(100);")
    # cursor.execute("alter table topic_list add column abstract text;")
    # cursor.execute("alter table topic_list add column status varchar(10);")
    # cursor.execute("alter table topic_list add column influence int;")

    # cursor.execute("alter table result_topic add column entity_profile text not null;")
    # cursor.execute("create table syntactic_train select * from sinanews.train")
    # cursor.execute("create table original_comment select * from sinanews.comment")
    # cursor.execute("create table original_news select * from sinanews.news")
    # cursor.execute("create table original_url select * from sinanews.urlinfo")
    # cursor.execute("alter table original_comment add column topic_id int not null;")
    # cursor.execute("alter table original_news add column topic_id int not null;")
    # cursor.execute("alter table original_url add column topic_id int not null;")
    # cursor.execute("create table syntactic_news select * from sinanews.newssyn")
    # cursor.execute("create table syntactic_comment select * from sinanews.commentsyn")
    # cursor.execute("alter table syntactic_news add column topic_id int not null;")
    # cursor.execute("alter table syntactic_comment add column topic_id int not null;")

    #cursor.execute("create table topic_list (id int primary key, topic_name varchar(100), keyword text, topic_type int)")
    #cursor.execute("insert into topic_list values(3, %s,%s,%s)", ('抗击肺炎', '疫情,肺炎', 0))

    # search_info = u'熔断机制'
    # sql_str = "select * from original_url"
    # cursor.execute(sql_str)
    # results = cursor.fetchall()
    # for com in results:
    #     update_sql = "update original_news set url = '%s' where id = %s" % (com[1].encode('utf-8'), com[0])
    #     cursor.execute(update_sql)
        # self.conn.commit()

    # cursor.execute("create table result_topic (id int primary key, event_info text, date_count text, event_edge text, event_node text, enetiy_name text, entity_event text, date_info text, heatmap_data text, feature_frequent text, feature_positive text, feature_negative text, sentiment_stream text, sentiment_piechart text, news_top text, comment_best text, comment_top text, comment_famous text, comment_question text, area_info text)")


    # creat table
    # cursor.execute("create table commentSyn (id int primary key, preprocessSen text, posTagging text, syntacticAnalysis text, pvWord text, pvModifierWord text, keyWords text, tagResult int, sentimentValue int)")
    #
    # cursor.execute("create table newsSyn (id int primary key, preprocessSen text, posTagging text, entity varchar(500)) ")

    # cursor.execute("create table comment(id int auto_increment primary key, userID varchar(50), userName varchar(50), userType varchar(50), time varchar(50), forwardNum int, commentNum int, likeNum int, content varchar(500), topicId int)")
    # cursor.execute("create table comment(id int auto_increment primary key, userID varchar(50), userName varchar(50), userType varchar(50), time varchar(50), forwardNum int, commentNum int, likeNum int, content varchar(500))")
    # cursor.execute("create table train(id int auto_increment primary key, preprocessSen varchar(500), posTagging varchar(750), syntacticAnalysis text, pvWord text, pvModifierWord text, keyWords text, tagResult int)")
    # cursor.execute("create table syntactic_result(id int primary key, preprocessSen varchar(500), posTagging varchar(750), syntacticAnalysis text, pvWord text, pvModifierWord text, keyWords text, tagResult int)")
    # cursor.execute("create table update_result (id int auto_increment primary key, result_id int, realTagResult int)")



    # value = [[5,'1'],[25,'0'],[342,'1'],[514,'2'],[1235,'1']]
    # for i in range(0, len(value)):
    #     cursor.execute("insert into update_result values(null,%s,%s)",value[i])

    # insert
    # value = [1,"inserted"]
    # cursor.execute("insert into test values(%s,%s)",value)

    # select
    # cursor = conn.cursor()
    # conn.select_db('sinanews')
    # cursor.execute("select * from news where id < 100")
    # results = cursor.fetchall()
    #
    # for d in results:
    #     # print chardet.detect(d[4])
    #     # print type(d[4])
    #     print d[4]

    cursor.close()
    conn.commit()
    conn.close()

def copydata_1():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')

    # creat database
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # select database
    conn.select_db('topicdemo')

    search_sql = "select * from temp_comment where topic_id = %d" % 1

    cursor.execute(search_sql) # where id < 10
    results = cursor.fetchall()

    for com in results:
        insert_sql = "insert into crawl_comment values(null,'%s','%s','%s',%s,'%s','%s',%s,%s,'%s',%s)" % (com[1],com[2],com[3],com[4],com[5].replace("'",'"'),com[6].replace("'",'"'),com[7],com[8],com[9].replace("'",'"'),com[10])
        try:
            cursor.execute(insert_sql)
        except:
            print insert_sql
    conn.commit()

def copydata():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')

    # creat database
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # select database
    conn.select_db('newsdemo')

    search_sql = "select * from syntactic_comment where topic_id = %d" % 0

    cursor.execute(search_sql) # where id < 10
    results = cursor.fetchall()

    conn.select_db('topicdemo')
    # index = 22072
    # for com in results:
    #     insert_sql = "insert into preprocess_comment values(%d,%d,'%s','%s',null,null,null,null,%s,%s)" % (index,0,com[1].replace("'",'"'),com[2],com[7],com[8])
    #     try:
    #         cursor.execute(insert_sql)
    #     except:
    #         print insert_sql
    #         cursor.execute(insert_sql)
    #         break
    #     index += 1
    # conn.commit()

    # index = 22072
    # for com in results:
    #     update_sql = u"update preprocess_comment set syntactic = \"%s\" where id = %s" % (com[3].replace('\\','\\\\'), index)
    #     try:
    #         cursor.execute(update_sql)
    #     except:
    #         print update_sql
    #     index += 1
    # conn.commit()

    # index = 22072
    # for com in results:
    #     update_sql = u"update preprocess_comment set keywords = \"%s\" where id = %s" % (com[6].replace('\\','\\\\'), index)
    #     try:
    #         cursor.execute(update_sql)
    #     except:
    #         print update_sql
    #     index += 1
    # conn.commit()

if __name__ == "__main__":

    # 建数据库表
    CreateDataBase()
    # copydata()

    # str_time = time.strptime('2016年5月10日00:00', "%Y年%m月%d日%H:%M")
    # sec_time = int(time.mktime(str_time))
    # print sec_time