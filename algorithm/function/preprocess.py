#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
import jieba
import jieba.posseg as pseg
import re
import json
import os
import chardet
from define import ReadConf

from ltp import Transformer

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

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

class repTool():
    def __init__(self):
        #去掉句子中的\n
        self.replace_fenhang = re.compile(ur'\n', re.S)
        #去掉句子中的空格
        self.replace_kongge = re.compile(ur' ', re.S)
        #分词分隔符
        self.replace_fenge1 = re.compile(ur'^', re.S)
        self.replace_fenge2 = re.compile(ur':', re.S)

    def replace(self, content):
        content = content.decode('utf-8')
        # content = re.sub(self.replace_fenhang, u"", content)
        # content = re.sub(self.replace_kongge, u"", content)
        content = re.sub(self.replace_fenge1, u"", content)
        content = re.sub(self.replace_fenge2, u"：", content)
        return content.strip().encode('utf-8')

    def replace_postaging(self, content):
        content = content.decode('utf-8')
        content = re.sub(self.replace_fenhang, u"", content)
        content = re.sub(self.replace_kongge, u"", content)
        return content.strip().encode('utf-8')

    def replace_comment(self, content):
        content = content.decode('utf-8')
        content = re.sub(self.replace_fenhang, u"", content)
        content = re.sub(self.replace_kongge, u"", content)
        content = re.sub(self.replace_fenge1, u"", content)
        content = re.sub(self.replace_fenge2, u"：", content)
        return content.strip().encode('utf-8')

class Preprocess:
    def __init__(self, tid):
        # open database
        #hostname, hostport, username, passwdname, dbname = ReadConf()

        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="jkl;")
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.conn.select_db("topicdemo")

        self.total_chaifen_num = 0

         # 基本变量
        self.topic_id = int(tid)

        # define
        self.rep_tool = repTool()

        # 处理函数
        self.readStopword()

        #self.readNews()
        #self.newsPosTaging()

        self.readComments()
        #self.commentPosTaging()

        self.getLtpResults()
        self.updateLtpResults()

    # 读取停词表
    def readStopword(self):
        self.stopword_list = []
        input_f = open(os.path.abspath('data/dict/stopWord.txt'))
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            self.stopword_list.append(temp_sen.strip())
        input_f.close()

    # 读取新闻
    def readNews(self):
        print 'Preprocess 1: read news'
        self.news_count = 0
        self.news_index_list = []
        self.news_body_list = []

        self.cursor.execute("select id, news_body from crawl_news where topic_id=%s" % self.topic_id) # where id < 10
        results = self.cursor.fetchall()

        for com in results:
            self.news_index_list.append(com[0])
            self.news_body_list.append(self.rep_tool.replace(com[1].strip()))
            self.news_count += 1
        print "total news number : ", self.news_count

    def newsPosTaging(self):
        posTaging_list = []
        for i in range(0, self.news_count):
            temg_sen = ''
            if i % 20 == 0:
                print i
            words = pseg.cut(self.rep_tool.replace_postaging(self.news_body_list[i]))
            for w in words:
                if w.word not in self.stopword_list:
                    flag = w.flag
                    if len(flag) == 1:
                        flag += '-'
                    elif len(flag) > 2:
                        flag = flag[:2]
                    temg_sen += (w.word + ':' +flag + '^')
            temg_sen = temg_sen[:-1]
            posTaging_list.append(temg_sen)
            # print i, len(self.news_body_list[i]), len(temg_sen)


        # 插入数据库
        for i in range(0, self.news_count):
            if i % 50 == 0:
                print i
            insert_sql = "insert into preprocess_news values(%s,%d,'%s','%s')" % (self.news_index_list[i], self.topic_id, self.news_body_list[i].encode('utf-8'), posTaging_list[i].encode('utf-8'))
            # print insert_sql
            try:
                self.cursor.execute(insert_sql)
            except:
                try:
                    insert_sql = "insert into preprocess_news values(%s,%d,'%s','')" % (self.news_index_list[i], self.topic_id, self.news_body_list[i].encode('utf-8'))
                    self.cursor.execute(insert_sql)
                except:
                    print len(temg_sen)
                    print temg_sen
                    continue
        self.conn.commit()

        # self.conn.commit()
        # self.cursor.close()
        # self.conn.close()

    # 读取评论文件
    def readComments(self):
        print 'Preprocess 2: read comments'

        self.comment_count = 0
        self.comment_id_list = []
        self.comment_body_list = []

        self.cursor.execute("select id, comment_body from crawl_comment where topic_id=%s limit 100" % self.topic_id) # where id < 10
        results = self.cursor.fetchall()

        for com in results:
            self.comment_id_list.append(com[0])
            self.comment_body_list.append(self.rep_tool.replace_comment(com[1].strip()))
            self.comment_count += 1
        print "total comment number : ", self.comment_count
        
        # 拆分数据集，用于哈工大的分析
        file_index = 0
        file_length = 0
        os.system('del ..\data\chaifen\*.txt')
        #input_f = open(os.path.abspath('data\dict\stopWord.txt'))
        output_file = 'data\chaifen\%d.txt' % file_index
        output_f = open(output_file, 'w')
        self.total_chaifen_num = 1
        for i in range(0, self.comment_count):
            file_length += len(self.comment_body_list[i])
            if file_length > 15000:
                output_f.close()
                file_length = 0
                file_index += 1
                output_file = 'data\chaifen\%d.txt' % file_index
                output_f = open(output_file, 'w')
                self.total_chaifen_num += 1
            output_f.write('%s\n' % self.comment_body_list[i])
        output_f.close()

    # 评论的分词，并写入数据库
    def commentPosTaging(self):
        # self.comment_count = 100
        posTaging_list = []
        for i in range(0, self.comment_count):
            temg_sen = ''
            if i % 500 == 0:
                print i
            words = pseg.cut(self.comment_body_list[i])
            for w in words:
                # if w.word not in self.stopword_list:
                flag = w.flag
                if len(flag) == 1:
                    flag += '-'
                elif len(flag) > 2:
                    flag = flag[:2]
                temg_sen += (w.word + ':' +flag + '^')
            temg_sen = temg_sen[:-1]
            posTaging_list.append(temg_sen)

        # temp_str = "['sd','as']"
        # 插入数据库
        for i in range(0, self.comment_count):
            if i % 500 == 0:
                print i
            insert_sql = "insert into preprocess_comment values (%s,%d,'%s','%s',null,null,null,null,-1,0,null)" % (self.comment_id_list[i], self.topic_id, self.comment_body_list[i].encode('utf-8'), posTaging_list[i].encode('utf-8'))
            print insert_sql
            try:
                self.cursor.execute(insert_sql)
            except:
                try:
                    insert_sql = "insert into preprocess_comment values (%s,%d,'%s','',null,null,null,null,-1,0,null)" % (self.comment_id_list[i], self.topic_id, self.comment_body_list[i].encode('utf-8'))
                    self.cursor.execute(insert_sql)
                except:
                    print len(temg_sen)
                    print temg_sen
                    continue
        self.conn.commit()

    # 获取哈工大句法分析结果
    def getLtpResults(self):
        print 'Preprocess 3: get ltp results'
        os.system('del ..\data\chaifen_ltp\*.txt')

        transformer = Transformer()
        # 对每一篇文档使用哈工大分词, 并存入对应序号的文件(dataFolder\mydata\pre\chaifen_ltp)中
        # 每一篇文档为多条文本的集合, 一行为一条文本
        transformer.transMyTestSet(
            the_index=0,
            the_end=450,
            # the_end=self.total_chaifen_num
        )

        # 查看哈工大分词存入的文件
        count = 0
        for i in range(0, 1):
            input_file_name =  os.path.abspath('data/chaifen_ltp/0.txt')
            count += transformer.lookFile(
                input_file= input_file_name
            )
        print count

    # 读取哈工大句法分析结果
    def updateLtpResults(self):
        if self.total_chaifen_num == 0:
            self.ltp_file_num = 10000
        else:
            self.ltp_file_num = self.total_chaifen_num
        self.ltp_list = []
        for i in range(0, self.ltp_file_num):
            if i % 25 ==0:
                print i
            input_file = 'data\chaifen_ltp\%d.txt' % i
            try:
                input_f = open(input_file)
                for file_line in input_f:
                    file_line_list = json.loads(file_line.strip(), object_hook=_decode_dict)
                    for sentence in file_line_list:
                        # self.ltp_list.append('')
                        # print file_line_list
                        # temp = eval('%s' % sentence[0])
                        # # print len(temp)
                        # for i in range(0, len(temp)):
                        # #     print chardet.detect(temp[i]['cont'])
                        #     temp[i]['cont'] = temp[i]['cont'].decode('utf-8')
                        # #     print chardet.detect(temp[i]['cont']) .encode('utf-8')

                        ltp_str = "%s" % sentence[0]
                        self.ltp_list.append(ltp_str.replace('\\','\\\\'))
                input_f.close()
            except:
                break
        print len(self.ltp_list)

        for i in range(0, len(self.ltp_list)):
            update_sql = u"update preprocess_comment set syntactic = \"%s\" where id = %s" % (self.ltp_list[i], self.comment_id_list[i])
            try:
                # print update_sql
                self.cursor.execute(update_sql)
            except:
                print i
        self.conn.commit()

if __name__ == "__main__":
    test = Preprocess(3)