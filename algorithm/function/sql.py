#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def CreateDataBase():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')

    # creat database
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # creat database
    # cursor.execute("create database if not exists topicdemo charset utf8 COLLATE utf8_general_ci")

    # create table
    conn.select_db('topicdemo')
    # cursor.execute("create table crawl_comment(id int auto_increment primary key, news_id varchar(25), time varchar(25), uid varchar(25), wb_verified_type int, nick varchar(100), area varchar(50), against int, vote int, comment_body varchar(2550), topic_id int)")
    # cursor.execute("create table crawl_news(id int auto_increment primary key, news_id varchar(25), news_channel varchar(8), time varchar(50), title varchar(255), news_body text, url varchar(255), topic_id int)")
    # cursor.execute("create table crawl_url(id int auto_increment primary key, url varchar(255), topicid int)")

    # cursor.execute("create table topic_list (id int primary key, topic_name varchar(100), keyword text, topic_type int)")
    # cursor.execute("alter table topic_list add column date varchar(100);")
    # cursor.execute("alter table topic_list add column abstract text;")
    # cursor.execute("alter table topic_list add column status varchar(10);")
    # cursor.execute("alter table topic_list add column influence int;")

    # cursor.execute("create table preprocess_news (id int primary key, topic_id int, news_body text, pos_tagging text) ")
    # cursor.execute("create table preprocess_comment (id int primary key, topic_id int, comment_body text, pos_tagging text, syntactic text, pv_word text, pv_modifier_word text, keywords text, tag_label int, sentiment_value int) ")
    # cursor.execute("alter table preprocess_comment add column mutisentiment_value text;")


    # cursor.execute("create table syntactic_train(id int auto_increment primary key, preprocessSen varchar(500), posTagging varchar(750), syntacticAnalysis text, pvWord text, pvModifierWord text, keyWords text, tagResult int)")

    cursor.execute("create table result_topic (topic_id int primary key, date_info text, date_count text, status_info text, event_info text, event_edge text, event_node text, entity_name text, entity_event text, entity_profile text,  heatmap_data text, feature_frequent text, feature_positive text, feature_negative text, sentiment_stream text, sentiment_piechart text, news_top text, comment_best text, comment_top text, comment_famous text, comment_question text, area_info text, \
    cd_value text, er_value text, tp_value text, tem_value text)")


if __name__ == "__main__":

    # 建数据库表
    CreateDataBase()