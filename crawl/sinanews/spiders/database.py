#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == "__main__":
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')

    # creat database
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # cursor.execute("create database if not exists sinanews charset utf8 COLLATE utf8_general_ci")

    conn.select_db('newsdemo')

    cursor.execute("create table crawl_comment(id int auto_increment primary key, news_id varchar(25), time varchar(25), uid varchar(25), wb_verified_type int, nick varchar(100), area varchar(50), against int, vote int, comment_body varchar(2550), topic_id int)")
    cursor.execute("create table crawl_news(id int auto_increment primary key, news_id varchar(25), news_channel varchar(8), time varchar(50), title varchar(255), news_body text, url varchar(255), topic_id int)")
    cursor.execute("create table crawl_url(id int auto_increment primary key, url varchar(255), topicid int)")

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



