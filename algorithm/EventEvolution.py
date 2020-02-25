#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
import time
import math
import jieba
import jieba.posseg as pseg
import chardet
import random

class EventEvolution:
    def __init__(self, tid):
        # open database
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='jkl;')
        self.cursor = self.conn.cursor()
        self.conn.select_db('newsdemo')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

        # 基本变量
        self.topic_id = int(tid)
        # insert_sql = "insert into result_topic values(%d, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null)" % (self.topic_id)
        # self.cursor.execute(insert_sql)
        # self.conn.commit()

        # read data
        # self.readStopword()
        self.getNews()
        self.getComments()

        # set the count length
        self.date_length = 86400
        self.baseCount(self.date_length)
        self.dayCount()

         # 获取代表性新闻
        # self.getRepresentNews()

        # 特征分析
        # self.featuresCount()

        # 统计高频词组，用于绘制字云图
        # self.getFrequentFeatures()

        # 地域信息统计
        # self.commentAreaCount()

        # 最佳评论子集产生
        # self.generateBestCommentSet()
        # self.generateBestNewsSet()


        # 计算每一个事件评论的衰减过程
        # self.eventDecreaseRate()

        # sentiment
        # 正反情感分析
        # self.readSentimentDict()
        # self.sentimentAnalyze()

        # 多类情感分析
        # self.readMutiSentimentDict()
        # self.mutiSentimentAnalyze()

        # tfidf相关
        # self.readIDFDict()

        # 实体相关的统计
        # self.getEntities()

        # 关系分析
        # self.relationAnalyze()



        # 获取IDF值，第一次运行
        # self.getIDF()
        # self.getIDFDict(ur'..\static\data\tfidf.csv')
        # self.getNewsTFIDF()
        #
        # self.clusterKMeans()

    # 0.读取停词表
    def readStopword(self):
        self.stopword_list = []
        input_f = open(ur'..\static\data\dict\stopWord.txt')
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            self.stopword_list.append(temp_sen.strip())
        input_f.close()

    # 0.读取情感词典
    def readSentimentDict(self):
        self.positive_word_list = []
        self.negative_word_list = []
        input_f = open(ur'..\static\data\dict\sentiment_positive.txt')
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            self.positive_word_list.append(temp_sen.strip())
        input_f.close()
        input_f = open(ur'..\static\data\dict\sentiment_negative.txt')
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            self.negative_word_list.append(temp_sen.strip())
        input_f.close()

        # print len(self.positive_word_list)
        # print len(self.negative_word_list)

    # 0.读取多类情感词典
    def readMutiSentimentDict(self):
        print "read sentiment dictionary"

        self.muti_sentiment_word_list = []
        self.muti_sentiment_pos_list = []
        self.muti_sentiment_type_list = []
        self.muti_sentiment_strength_list = []
        self.muti_sentiment_polarity_list = []

        corpus_f = open(ur'..\static\data\dict\sentiment_dict.txt')
        cor_list = corpus_f.readlines()
        for cor_temp in cor_list:
            temp_sen_split_list = cor_temp.split('\t')
            self.muti_sentiment_word_list.append(temp_sen_split_list[0])
            self.muti_sentiment_pos_list.append(temp_sen_split_list[1])
            if temp_sen_split_list[2] == 'PA' or  temp_sen_split_list[2] == 'PE':
                self.muti_sentiment_type_list.append(0)
            elif temp_sen_split_list[2] == 'PD' or  temp_sen_split_list[2] == 'PH' or  temp_sen_split_list[2] == 'PG' \
                    or  temp_sen_split_list[2] == 'PB' or  temp_sen_split_list[2] == 'PK':
                self.muti_sentiment_type_list.append(1)
            elif temp_sen_split_list[2] == 'NA':
                self.muti_sentiment_type_list.append(2)
            elif temp_sen_split_list[2] == 'NB' or  temp_sen_split_list[2] == 'NJ' or  temp_sen_split_list[2] == 'NH' \
                    or  temp_sen_split_list[2] == 'PF':
                self.muti_sentiment_type_list.append(3)
            elif temp_sen_split_list[2] == 'NI' or  temp_sen_split_list[2] == 'NC' or  temp_sen_split_list[2] == 'NG':
                self.muti_sentiment_type_list.append(4)
            elif temp_sen_split_list[2] == 'NE' or  temp_sen_split_list[2] == 'ND' or  temp_sen_split_list[2] == 'NN' \
                    or  temp_sen_split_list[2] == 'NK' or  temp_sen_split_list[2] == 'NL':
                self.muti_sentiment_type_list.append(5)
            elif temp_sen_split_list[2] == 'PC':
                self.muti_sentiment_type_list.append(6)

            self.muti_sentiment_strength_list.append(int(temp_sen_split_list[3]))
            self.muti_sentiment_polarity_list.append(int(temp_sen_split_list[4]))
        corpus_f.close()

        # print self.muti_sentiment_word_list[123]
        # print self.muti_sentiment_pos_list[123]
        # print self.muti_sentiment_type_list[123]
        # print self.muti_sentiment_strength_list[123]
        # print self.muti_sentiment_polarity_list[123]

    # 1.读取新闻
    def getNews(self):
        print 'Process 1: read news'

        self.news_num = 0
        self.news_id_list = []
        self.news_times_list = []
        self.news_title_list = []
        self.news_body_list = []
        self.news_dayIndex_list = []

        self.news_url_list = []
        self.news_leader_list = []


        # open database
        self.conn.select_db('newsdemo')
        search_sql = "select * from original_news where topic_id = %d" % self.topic_id
        self.cursor.execute(search_sql) # where id < 10
        results = self.cursor.fetchall()

        for com in results:
            self.news_id_list.append(com[1])
            if com[3] != '-':
                str_time = time.strptime(com[3].split(' ')[0], "%Y年%m月%d日%H:%M")
                sec_time = int(time.mktime(str_time))
                self.news_times_list.append(sec_time)
            else:
                self.news_times_list.append(0)

            self.news_title_list.append(com[4])
            self.news_body_list.append(com[5])
            self.news_url_list.append(com[7])
            self.news_dayIndex_list.append(0)
            self.news_leader_list.append('')
            self.news_num += 1

        self.news_posTaging_list = []
        search_sql = "select * from syntactic_news where topic_id = %d" % self.topic_id
        self.cursor.execute(search_sql) # where id < 10
        results = self.cursor.fetchall()
        for com in results:
            self.news_body_list.append(com[1])
            self.news_posTaging_list.append(com[2])

        # self.cursor.close()
        # self.conn.commit()
        # self.conn.close()

        print "total news number : ", self.news_num

    # 2.读取评论
    def getComments(self):
        print 'Process 2: read comments'

        self.comment_num = 0
        self.comment_id = []
        self.comment_newsId_list = []
        self.comment_time_list = []
        self.comment_uid_list = []
        self.comment_verifiedType_list = []
        self.comment_nickId_list = []
        self.comment_area_list = []
        self.comment_against_list = []
        self.comment_vote_list = []
        self.comment_body_list = []

        # 日期下标
        self.comment_dayIndex_list = []
        #情感类型
        self.comment_sentiment_list = []

        search_sql = "select * from original_comment where topic_id = %d" % self.topic_id
        self.cursor.execute(search_sql) # where id < 10
        results = self.cursor.fetchall()

        for com in results:
            self.comment_id.append(int(com[0]))
            self.comment_newsId_list.append(com[1])
            str_time = time.strptime(com[2], "%Y-%m-%d %H:%M:%S")
            sec_time = int(time.mktime(str_time))
            self.comment_time_list.append(sec_time)
            self.comment_uid_list.append(com[3])
            self.comment_verifiedType_list.append(com[4])
            self.comment_nickId_list.append(com[5])
            self.comment_area_list.append(com[6])
            self.comment_against_list.append(int(com[7]))
            self.comment_vote_list.append(int(com[8]))
            # self.comment_body_list.append(com[9].strip())
            self.comment_dayIndex_list.append(0)
            self.comment_sentiment_list.append(0)
            self.comment_num += 1

        self.comment_posTaging_list = []
        self.comment_ltp_list = []
        self.comment_synTag_list = []

        search_sql = "select * from syntactic_comment where topic_id = %d" % self.topic_id
        self.cursor.execute(search_sql) # where id < 10
        results = self.cursor.fetchall()
        for com in results:
            self.comment_body_list.append(com[1])
            self.comment_posTaging_list.append(com[2])
            # self.comment_ltp_list.append(com[3])
            self.comment_synTag_list.append(int(com[7]))

        # self.cursor.close()
        # self.conn.commit()
        # self.conn.close()

        print "total comment number : ", self.comment_num

    # 3.基本时间统计
    def baseCount(self,data_length):
        print "Process 3: base time count"
        # get the base time
        min_time = self.news_times_list[0]
        max_time = self.news_times_list[0]
        for i in range(0, self.news_num):
            if self.news_times_list[i] > max_time:
                max_time = self.news_times_list[i]
            elif self.news_times_list[i] < min_time and self.news_times_list[i] != 0:
                min_time = self.news_times_list[i]

        # print min_time,max_time
        # print time.localtime(min_time)
        # print time.localtime(max_time)

        # caclulate total day
        self.base_time = min_time - time.localtime(min_time).tm_hour * 3600 - time.localtime(min_time).tm_min * 60 - time.localtime(min_time).tm_sec - data_length
        # print self.base_time
        self.total_day = (max_time - self.base_time)/data_length + 1

        # calulate
        print 'total day is:', self.total_day

        str_time_s = time.strftime("%Y-%m-%d",time.localtime(min_time))
        str_time_e = time.strftime("%Y-%m-%d",time.localtime(max_time))

        update_sql = "update topic_list set Date = '%s - %s'" % (str_time_s.encode('utf-8'), str_time_e.encode('utf-8'))
        self.cursor.execute(update_sql)
        self.conn.commit()

        update_sql = "update topic_list set abstract = '%s', status = '%s', influence = '%d'" % ('熔断机制摘要', '结束',98)
        self.cursor.execute(update_sql)
        self.conn.commit()

    # 4.按天统计
    def dayCount(self):
        print "Process 4: comments and news' day count"

        # day count
        self.comment_day_count = []
        self.news_day_count = []
        # 每篇新闻评论的个数
        self.news_commentNum_list = []

        for i in range(0, self.total_day):
            self.comment_day_count.append(0)
            self.news_day_count.append(0)
        # 评论的统计
        for i in range(0, self.comment_num):
            day = (self.comment_time_list[i] - self.base_time)/86400
            self.comment_day_count[day] += 1
            self.comment_dayIndex_list[i] = day
        # 新闻的统计
        for i in range(0, self.news_num):
            self.news_commentNum_list.append(self.comment_newsId_list.count(self.news_id_list[i]))
            # print i, self.news_commentNum_list[i]
            if self.news_times_list[i] != 0:
                day = (self.news_times_list[i] - self.base_time)/86400
            else:
                day = 0
            self.news_dayIndex_list[i] = day
            self.news_day_count[day] += 1

        # 输出统计
        # output_f = open(ur'..\static\data\dayCount\day_count.csv', 'w')
        # index = 0
        # output_f.write('date,news_num,comment_num\n')
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     output_f.write('%s,%s,%s\n' % (str_time, self.news_day_count[i], self.comment_day_count[i]))
        # output_f.close()

        # 写入数据库
        # date_count_str = ''
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     date_count_str += ('%s,%s,%s\n' % (str_time, self.news_day_count[i], self.comment_day_count[i]))
        # date_count_str = date_count_str[:-1]
        # update_sql = "update result_topic set date_count = '%s' where id = %d" % (date_count_str.encode('utf-8'), self.topic_id)
        # self.cursor.execute(update_sql)
        # self.conn.commit()

    # 算IDF向量
    def getIDF(self):
        # tf-idf
        self.total_word_num = 0
        self.word_dict = {}

        self.word_count_list = []
        self.word_occur_list = []
        self.word_occur_mark_list = []

        # get tf-idf
        # self.news_num = 10
        for i in range(0, self.news_num):
            if i % 50 == 0:
                print i

            if i != 0:
                for j in range(0, len(self.word_occur_mark_list)):
                    self.word_occur_mark_list[j] = 0

            words = pseg.cut(self.news_body_list[i])
            for w in words:
                if w.flag[0] == 'v' or w.flag[0] == 'n':
                    temp_index = self.word_dict.get(w.word, -1)
                    if temp_index != -1:
                        self.word_count_list[temp_index] += 1
                        if self.word_occur_mark_list[temp_index] == 0:
                            self.word_occur_list[temp_index] += 1
                            self.word_occur_mark_list[temp_index] = 1
                    else:
                        self.word_dict[w.word] = self.total_word_num
                        self.word_count_list.append(1)
                        self.word_occur_list.append(1)
                        self.word_occur_mark_list.append(1)
                        self.total_word_num += 1

        output_f = open(ur'..\static\data\idf\idf.csv', 'w')
        for word, index in self.word_dict.items():
            # print chardet.detect(word)
            # print word, index
            # print self.word_count_list[index], self.word_occur_list[index]
            idf = math.log( self.news_num * 1.0 / self.word_occur_list[index] )
            output_f.write('%s,%d,%d,%f\n' % (word, self.word_count_list[index], self.word_occur_list[index], idf))
        output_f.close()

    # 读取idf字典
    def readIDFDict(self):
        self.word_idf_dict = {}
        input_f = open(ur'..\static\data\idf\idf.csv')
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            temp_sen_split_list = temp_sen.split(',')
            self.word_idf_dict[temp_sen_split_list[0].encode('utf-8')] = float(temp_sen_split_list[3])
            # print temp_sen_split_list[0], chardet.detect(temp_sen_split_list[0]), self.word_idf_dict[temp_sen_split_list[0]]

    # 读取IDF向量
    def getIDFDict(self, idf_file):
        input_f = open(idf_file)
        sen_list = input_f.readlines()
        for temp_sen in sen_list:
            temp_sen_split_list = temp_sen.split(',')
            self.word_dict[temp_sen_split_list[0]] = math.log(float(self.news_num) / int(temp_sen_split_list[2]))

        output_f = open(ur'..\static\data\idf.csv', 'w')
        for word, index in self.word_dict.items():
            # print chardet.detect(word)
            output_f.write('%s,%f\n' % (word, index))
        output_f.close()

    # 计算每一篇新闻的tf-idf向量
    def getNewsTFIDF(self):
        # self.news_num = 100

        # 生成字典
        self.word_tfidf_dict = [dict() for i in range(0, self.news_num)]

        for i in range(0, self.news_num):
            if i % 50 == 0:
                print i

            news_word_count = 0
            words = pseg.cut(self.news_body_list[i])
            for w in words:
                if w.flag == 'v' or w.flag == 'n':
                    news_word_count += 1
                    temp_index = self.word_tfidf_dict[i].get(w.word, -1)
                    if temp_index == -1:
                        self.word_tfidf_dict[i][w.word] = 1.0
                    else:
                        self.word_tfidf_dict[i][w.word] += 1.0

            for word, value in self.word_tfidf_dict[i].items():
                # print self.word_dict.get('记者', -1)
                idf_value = self.word_dict[word.encode('utf-8')]
                self.word_tfidf_dict[i][word] = (value/news_word_count) * idf_value

            # for word, value in self.word_tfidf_dict[i].items():
            #     print word, value

    # 计算新闻到中心点的距离
    def clusterDistance(self, j, i):
        if len(self.cluster_center_dict[j]) == 0:
            return 0
        if len(self.word_tfidf_dict[i]) == 0:
            return 0

        sum_ab = 0
        sum_aa = 0
        sum_bb = 0
        for word, value in self.cluster_center_dict[j].items():
            sum_aa += value*value
            if self.word_tfidf_dict[i].has_key(word):
                sum_ab += self.word_tfidf_dict[i][word] * value

        for word, value in self.word_tfidf_dict[i].items():
            sum_bb += value*value

        return sum_ab/(math.sqrt(sum_aa) * math.sqrt(sum_bb))

    # 使用k-means聚类
    def clusterKMeans(self):
        print "clusterKMeans"

        self.cluster_num = 50
        self.cluster_center_dict = [dict() for i in range(0, self.cluster_num)]
        for j in range(0, self.cluster_num):
            self.cluster_center_dict[j] = self.word_tfidf_dict[j].copy()

        # 每一个类别新闻的个数
        self.cluster_count = []
        for i in range(0, self.cluster_num):
            self.cluster_count.append(0)

        # 每一篇新闻的标记
        self.news_cluster_index = []
        for i in range(0, self.news_num):
            self.news_cluster_index.append(-1)
            # self.news_cluster_index.append(random.randint(0,self.cluster_num-1))


        round_number = 0
        while 1:
            print 'round_number', round_number
            # for i in range(0, self.news_num):
            #     print self.news_cluster_index[i]

            # 划分新类别
            # 求每一篇新闻到类别中心点的距离
            for i in range(0, self.news_num):
                max_distance = 0
                max_cluster = -1
                for j in range(0, self.cluster_num):
                    distance = self.clusterDistance(j, i)
                    # print i,j,distance
                    if distance > max_distance:
                        max_distance = distance
                        max_cluster = j
                self.news_cluster_index[i] = max_cluster


            round_number += 1
            if round_number > 50:
                break

            # 求类别中心点
            for j in range(0, self.cluster_num):
                self.cluster_center_dict[j] = {}
                self.cluster_count[j] = 0
                for i in range(0, self.news_num):
                    if self.news_cluster_index[i] == j:
                        self.cluster_count[j] += 1
                        for word, value in self.word_tfidf_dict[i].items():
                            if self.cluster_center_dict[j].has_key(word):
                                self.cluster_center_dict[j][word] += value
                            else:
                                self.cluster_center_dict[j][word] = value

                        # if self.cluster_center_dict[j]:
                        #     for word, value in self.word_tfidf_dict[i].items():
                        #         if self.cluster_center_dict[j].has_key(word):
                        #             self.cluster_center_dict[j][word] += value
                        #         else:
                        #             self.cluster_center_dict[j][word] = value
                        # else:
                        #     self.cluster_center_dict[j] = self.word_tfidf_dict[i].copy()
                for word in self.cluster_center_dict[j]:
                    self.cluster_center_dict[j][word] /= self.cluster_count[j]

                # print 'cluster',j
                # for word, value in self.cluster_center_dict[j].items():
                #     print word,value

        output_f = open(ur'..\static\data\cluster.txt', 'w')
        for i in range(0, self.news_num):
            output_f.write('%d \t %s \t %s\n' % (self.news_cluster_index[i], self.news_times_list[i], self.news_title_list[i]))
        output_f.close()

    # 5.获取代表性新闻事件，用于关系分析
    def getRepresentNews(self):
        print "Process 5: get represent news"
        
        # 计算每一天的权重
        count = 0
        self.news_representWeight_list = []

        # 从1开始，没有日期的不选择
        for i in range(0, self.total_day):
            self.news_representWeight_list.append(0.0)
            if self.news_day_count[i] != 0 and i != 0:
                #self.news_representWeight_list[i] = (self.comment_day_count[i] + 1.0) / self.news_day_count[i]
                self.news_representWeight_list[i] =  self.news_day_count[i]
            count += self.news_representWeight_list[i]

        # 确定每一天要抽取的新闻数目，（大概数目，自动调整）
        self.represent_news_num = 50
        represent_news_daynum_list = []
        for i in range(0, self.total_day):
            self.news_representWeight_list[i] /= count
            represent_news_daynum_list.append(int(math.ceil(self.news_representWeight_list[i] * self.represent_news_num)))
            # print self.news_day_count[i], self.comment_day_count[i], self.news_representWeight_list[i], represent_news_daynum_list[i]

        # 对新闻排序
        news_comment_dayIndex_list = []
        for i in range(0, self.news_num):
            news_comment_dayIndex_list.append([i, self.news_dayIndex_list[i], self.news_commentNum_list[i]])
            # print news_comment_dayIndex_list[i]
        news_comment_dayIndex_list.sort(key=lambda l:(l[1],l[2]),reverse=True)

        # output_f = open(ur'..\static\data\representNews\test.csv', 'w')
        # for i in range(0, self.news_num):
        #     output_f.write('%s\n' % news_comment_dayIndex_list[i])
        # output_f.close()

        # 找出新闻
        self.represent_news_index = []
        for j in range(0, self.total_day):
            for i in range(0, self.news_num):
                if news_comment_dayIndex_list[i][1] == j:
                    for s in range(0, represent_news_daynum_list[j]):
                        self.represent_news_index.append(news_comment_dayIndex_list[i+s][0])
                    break

        events_info_str = ''
        for i in range(0, self.represent_news_num):
            id = self.represent_news_index[i]
            leader_index = self.news_body_list[id].find('。')
            if leader_index != -1:
                self.news_leader_list[id] = self.news_body_list[id][:leader_index+3].strip().encode('utf-8')
                # print i, self.news_leader_list[id]

            str_time = time.strftime("%Y-%m-%d",time.localtime(self.news_times_list[id]))
            events_info_str += ('%s^%s^%s^%s^%d^%s\n' % (str_time, self.news_dayIndex_list[id], self.news_title_list[id], self.news_leader_list[id], self.news_commentNum_list[id], self.news_url_list[id]))
        events_info_str = events_info_str[:-1]
        update_sql = "update result_topic set event_info = '%s' where id = %d" % (events_info_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()


        # output_f = open(ur'..\static\data\representNews\represent_news.csv', 'w')
        # index = 0
        # for i in range(0, len(self.represent_news_index)):
        #     id = self.represent_news_index[i]
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(self.news_times_list[id]))
        #     output_f.write('%s,%s,%s,%d\n' % (str_time, self.news_dayIndex_list[id], self.news_title_list[id],  self.news_commentNum_list[id]))
        # output_f.close()

        # 重新计算代表性新闻篇数
        self.represent_news_num = len(self.represent_news_index)
        print 'represent_news_num ', self.represent_news_num


    # def getNodeAndEdge(self):
    #     max_comment_num = 0
    #     max_relation_num = 0
    #     self.represent_news_weight = []
    #     for i in range(0, self.represent_news_num):
    #         id = self.represent_news_index[i]
    #         if self.news_commentNum_list[id] > max_comment_num:
    #             max_comment_num = self.news_commentNum_list[id]
    #         if self.event_relation_num[i] > max_relation_num:
    #             max_relation_num = self.event_relation_num[i]
    #     for i in range(0, self.represent_news_num):
    #         comment_weight = math.ceil((self.represent_news_comNum_list[i])*10.0/max_comment_num)+4
    #         relation_weight = math.ceil((self.event_relation_num[i])*10.0/max_relation_num)+4
    #         print i, self.represent_news_comNum_list[i], comment_weight, self.event_relation_num[i], relation_weight
    #         self.represent_news_weight.append((comment_weight+relation_weight)/2)

    # 6.特征分析
    def featuresCount(self):
        print 'Process 6: features count'

        # 特征统计
        self.represent_news_singlefeatures = {}
        self.represent_news_combinefeatures = {}

        # 获取每一篇新闻的特征值
        self.represent_news_allfeatures = {}
        self.represent_news_features = []
        self.represent_news_features_tags = []
        self.represent_news_features_count = []
        for i in range(0, self.represent_news_num):
            self.represent_news_features.append([])
            self.represent_news_features_tags.append([])
            self.represent_news_features_count.append([])
            newsId = self.represent_news_index[i]

            pre_word = ''
            pre_flag = '-'
            words = self.news_posTaging_list[i].split('^')
            if len(words) == 1:
                continue
            for w in words:
                temp = w.split(':',1)
                word = temp[0]
                flag = temp[1]
                if flag[0] == 'v' or flag[1] == 'n':
                    if word not in self.represent_news_features[i]:
                        self.represent_news_features[i].append(word)
                        self.represent_news_features_tags[i].append(flag[0])
                        self.represent_news_features_count[i].append(1)
                        if self.represent_news_allfeatures.has_key(word):
                            self.represent_news_allfeatures[word] += 1
                        else:
                            self.represent_news_allfeatures[word] = 1
                    else:
                        index = self.represent_news_features[i].index(word)
                        self.represent_news_features_count[i][index] += 1

                # 获取高频词
                if flag[0] == 'n' or flag[0] == 'v' or flag[0] == 'd' or flag[0] == 'a':
                # if (flag0] == 'n') and len(flag) >= 2:
                    temp_flag = flag
                    if len(flag) == 1:
                        temp_flag = '-' + flag
                    single_word = word + temp_flag
                    if self.represent_news_singlefeatures.has_key(single_word):
                        self.represent_news_singlefeatures[single_word] += 1
                    else:
                        self.represent_news_singlefeatures[single_word] = 1

                # 获取高频词词组
                sutiable_flag_str = ['nv','vn','nd','dn','dv','vd','na','an']
                flag_str = pre_flag[0] + flag[0]
                if (flag_str in sutiable_flag_str):
                    combine_word = pre_word + word + flag_str
                    if self.represent_news_combinefeatures.has_key(combine_word):
                        self.represent_news_combinefeatures[combine_word] += 1
                    else:
                        self.represent_news_combinefeatures[combine_word] = 1
                pre_word = word
                pre_flag = flag

    # 6.1-获取高频词词组
    def getFrequentFeatures(self):
        # 组合词特征， 综合考虑评论中出现的次数
        print 'get frequent features'
        frequent_features_list = []
        combinefeatures_list = sorted(self.represent_news_combinefeatures.iteritems(), key=lambda l:l[1],reverse=True)
        for i in range(0, 1000):
            temp_word = combinefeatures_list[i][0][:-2]
            temp_count = 0
            for j in range(0, self.comment_num):
                temp_count += self.comment_body_list[j].count(temp_word)
            temp_count *= combinefeatures_list[i][1]
            temp_count = int(math.sqrt(temp_count))
            frequent_features_list.append([combinefeatures_list[i][0],temp_count])

        # 考虑单个词
        singlefeatures_list = sorted(self.represent_news_singlefeatures.iteritems(), key=lambda l:l[1],reverse=True)
        for i in range(0, 1000):
            temp_word = singlefeatures_list[i][0][:-2]
            if len(temp_word) <= 3:
                continue
            temp_count = 0
            for j in range(0, self.comment_num):
                temp_count += self.comment_body_list[j].count(temp_word)
            temp_count *= singlefeatures_list[i][1]
            temp_count = int(math.sqrt(temp_count)/8)
            frequent_features_list.append([singlefeatures_list[i][0],temp_count])

        # 输出高频特征
        frequent_features_list.sort(key=lambda l:l[1],reverse=True)
        frequent_features_str = ''
        for i in range(0, 100):
            frequent_features_list[i][1] = math.sqrt(frequent_features_list[i][1])
            weight = int((frequent_features_list[i][1] * 100.0/ frequent_features_list[0][1]))
            frequent_features_str += ('%s,%d\n' % (frequent_features_list[i][0][:-2], weight))
        frequent_features_str = frequent_features_str[:-1]
        update_sql = "update result_topic set feature_frequent = '%s' where id = %d" % (frequent_features_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

        # output_f = open(ur'..\static\data\features\cloud_features.csv', 'w')
        # output_f.write('feature,weight\n')
        # for i in range(0, 100):
        #     frequent_features_list[i][1] = math.sqrt(frequent_features_list[i][1])
        #     weight = int((frequent_features_list[i][1] * 100.0/ frequent_features_list[0][1]))
        #     output_f.write('%s,%d\n' % (frequent_features_list[i][0][:-2], weight))
        # output_f.close()

        # 组合词特征， 综合考虑评论中出现的次数
        # for word, value in self.represent_news_combinefeatures.items():
        #     temp_word = word[:-2]
        #     temp_count = 0
        #     for j in range(0, self.comment_num):
        #         temp_count += self.comment_body_list[j].count(temp_word)
        #     self.represent_news_combinefeatures[word] *= temp_count

         # 输出组合词特征
        # combinefeatures_list = sorted(self.represent_news_combinefeatures.iteritems(), key=lambda l:l[1],reverse=True)
        # output_f = open(ur'..\static\data\features\combine_features.csv', 'w')
        # output_f.write('feature,weight\n')
        # for i in range(0, 100):
        #     output_f.write('%s,%d\n' % (combinefeatures_list[i][0][:-2], combinefeatures_list[i][1]))
        # output_f.close()

        # 输出单词特征
        # singlefeatures_list = sorted(self.represent_news_singlefeatures.iteritems(), key=lambda l:l[1],reverse=True)
        # output_f = open(ur'..\static\data\features\single_features.csv', 'w')
        # for i in range(0, 100):
        #     output_f.write('%s %d\n' % (singlefeatures_list[i][0], singlefeatures_list[i][1]))
        # output_f.close()

    # 获取实体画像特征
    def getEntityProfile(self):
        # 分析每一个实体的画像特征
        entity_profile_dict = []
        entity_profile_str = ''
        for j in range(0, self.entity_num):
            entity_profile_dict.append({})

            for i in range(0, self.represent_news_num):
                newsId = self.represent_news_index[i]
                if self.news_body_list[newsId].find(self.entities_list[j]) != -1:
                    words = self.news_posTaging_list[newsId].split('^')
                    if len(words) == 1:
                        continue
                    for w in words:
                        temp = w.split(':',1)
                        word = temp[0]
                        flag = temp[1]
                        if flag[0] == 'a' or flag[0] == 'd':
                            # temp_word = word + flag[0]
                            temp_word = word
                            if entity_profile_dict[j].has_key(temp_word):
                                entity_profile_dict[j][temp_word] += 1
                            else:
                                entity_profile_dict[j][temp_word] = 1
            temp_e_profile_list = sorted(entity_profile_dict[j].iteritems(), key=lambda l:l[1],reverse=True)

            print self.entities_list[j]
            for i in range(0, 25):
                # print i, temp_e_profile_list[i][0]
                entity_profile_str += ('%s,%d\t' % (temp_e_profile_list[i][0],temp_e_profile_list[i][1]))
            # entity_profile_str = entity_profile_str[:-1]
            # entity_profile_str += '\n'
        entity_profile_str = entity_profile_str[:-1]
        update_sql = "update result_topic set entity_profile = '%s' where id = %d" % (entity_profile_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()


    # 6.2-获取实体
    def getEntities(self):
        print 'get entities'
        # 获取实体特征
        entities_dict = {}
        for word, value in self.represent_news_combinefeatures.items():
            if word[-1] == 'n': # or word[-2] == 'n'
                entities_dict[word] = value*4
        for word, value in self.represent_news_singlefeatures.items():
            if word[-2] == 'n' and not (word[-1] == 'g' or word[-1] == 'l') and len(word[:-2]) > 3:
                entities_dict[word] = value
                # if self.word_idf_dict.has_key(temp_word):
                #     if self.word_idf_dict[temp_word] < 3:
                #         entities_dict[word] = value * self.word_idf_dict[temp_word]
                #     else:
                #         entities_dict[word] = value

        temp_entities_list = sorted(entities_dict.iteritems(), key=lambda l:l[1],reverse=True)


        # 取前k个实体进行分析,看哪个在评论出现的次数多
        self.entity_num = 100
        temp_entities_count_list = []
        for i in range(0, self.entity_num):
            temp_entities_count_list.append([i, 0])

        for i in range(0, self.comment_num):
            for j in range(0, self.entity_num):
                entity_name = temp_entities_list[j][0][:-2]

                temp_count = self.comment_body_list[i].count(entity_name)
                if temp_count != 0:
                    # print entity_name, temp_count
                    temp_entities_count_list[j][1] += temp_count

        # 综合考虑事件和评论的出现次数
        for j in range(0, self.entity_num):
            temp_entities_count_list[j][1] *= (entities_dict[temp_entities_list[j][0]]*entities_dict[temp_entities_list[j][0]])
            # print temp_entities_list[j][0], temp_entities_count_list[j][1], entities_dict[temp_entities_list[j][0]]

        # 挑选最热的15个实体
        self.entities_list = []
        self.entity_num = 15
        temp_entities_count_list.sort(key=lambda l:l[1],reverse=True)
        for j in range(0, self.entity_num):
            print temp_entities_list[temp_entities_count_list[j][0]][0][:-2]
            print temp_entities_count_list[j][0], temp_entities_list[temp_entities_count_list[j][0]][0], temp_entities_count_list[j][1]
            self.entities_list.append(temp_entities_list[temp_entities_count_list[j][0]][0][:-2])



        self.getEntityProfile()
        return


        # 统计实体出现的频率，用于画heatmap
        self.entities_day_count_list = []
        for i in range(0, self.entity_num):
            # 初始化
            self.entities_day_count_list.append([])
            for j in range(0, self.total_day):
                self.entities_day_count_list[i].append(0)
            # 按评论统计
            for j in range(0, self.comment_num):
                if self.entities_list[i] in self.comment_body_list[j]:
                    day_index = self.comment_dayIndex_list[j]
                    self.entities_day_count_list[i][day_index] += 1

        # 输出实体日关注度矩阵，用于画heatmap
        # output_f = open(ur'..\static\data\entities\entities_matrix.csv', 'w')
        # for i in range(0, self.entity_num):
        #     output_f.write('%s,' % self.entities_list[i])
        #     for j in range(15, 45):
        #         # temp_time = self.base_time + self.date_length * j
        #         # str_time = time.strftime("%Y-%m-%d",time.localtime(temp_time))
        #         # output_f.write('%s,' % str_time)
        #         output_f.write('%d,' % self.entities_day_count_list[i][j])
        #     output_f.write('\n')
        # output_f.close()

        # 统计实体在事件中出现的频率，找出与事件最相关的前k个实体
        self.entities_event_count_list = []
        for i in range(0, self.represent_news_num):
            # 初始化
            self.entities_event_count_list.append([])
            for j in range(0, self.entity_num):
                self.entities_event_count_list[i].append([j,0])

            temp_news_id = self.news_id_list[self.represent_news_index[i]]
            # 按评论统计
            for k in range(0, self.comment_num):
                if self.comment_newsId_list[k] == temp_news_id:
                    for j in range(0, self.entity_num):
                        self.entities_event_count_list[i][j][1] += self.comment_body_list[k].count(self.entities_list[j])
        # 加上事件出现次数的考虑
        for i in range(0, self.represent_news_num):
            for j in range(0, self.entity_num):
                count = self.news_body_list[self.represent_news_index[i]].count(self.entities_list[j])
                self.entities_event_count_list[i][j][1] *= count


        # 输出实体在每个事件中出现的次数
        # output_f = open(ur'..\static\data\entities\entities_event_count.csv', 'w')
        # for i in range(0, self.entity_num):
        #     output_f.write('%s,' % self.entities_list[i])
        # output_f.write('\n')
        # for i in range(0, self.represent_news_num):
        #     output_f.write('%s,' % self.represent_news_index[i])
        #     for j in range(0, self.entity_num):
        #         output_f.write('%d,' % self.entities_event_count_list[i][j][1])
        #     output_f.write('\n')
        # output_f.close()

        # 输出每个事件相关的前k个实体，用于绘图
        entities_events = []
        for i in range(0, self.represent_news_num):
            self.entities_event_count_list[i].sort(key=lambda l:l[1], reverse=True)
            for j in range(0, 5):
                if self.entities_event_count_list[i][j][1] == 0:
                    break
                # if self.entities_event_count_list[i][j][0] <= j:
                #     entities_events.append([i,self.entities_event_count_list[i][j][0]])

                entities_events.append([i,self.entities_event_count_list[i][j][0]])

        entities_events.sort(key=lambda l:l[1])



        entities_events_str = ''
        for i in range(0, len(entities_events)):
            entities_events_str += ('%d,%d\n' % (entities_events[i][1], entities_events[i][0]))
        entities_events_str = entities_events_str[:-1]
        update_sql = "update result_topic set entity_event = '%s' where id = %d" % (entities_events_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

        # output_f = open(ur'..\static\data\entities\entities_events.csv', 'w')
        # output_f.write('entity_index,news_index\n')
        # for i in range(0, len(entities_events)):
        #     output_f.write('%d,%d\n' % (entities_events[i][1], entities_events[i][0]))
        # output_f.close()



        # heatmap 绘图相关
        entity_str = ''
        date_str = ''
        entities_date_count_str = ''
        for i in range(0, self.entity_num):
            entity_str += ('%s\n' % self.entities_list[i])
        for j in range(0, self.total_day):
            temp_time = self.base_time + self.date_length * j
            str_time = time.strftime("%Y-%m-%d",time.localtime(temp_time))
            date_str += ('%s\n' % str_time)
            for i in range(0, self.entity_num):
                entities_date_count_str += ('%d,%d,%d\n' % (j, i ,self.entities_day_count_list[i][j]))
        entity_str = entity_str[:-1]
        date_str = date_str[:-1]
        entities_date_count_str = entities_date_count_str[:-1]

        update_sql = "update result_topic set entity_name = '%s', date_info = '%s', heatmap_data = '%s' where id = %d" % (entity_str.encode('utf-8'), date_str.encode('utf-8'), entities_date_count_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()


        # 以下输出用于绘图
        # 输出实体名称
        # output_f = open(ur'..\static\data\entities\entities.csv', 'w')
        # output_f.write('entity\n')
        # for i in range(0, self.entity_num):
        #     output_f.write('%s\n' % self.entities_list[i])
        # output_f.close()

        # 输出日期
        # output_f = open(ur'..\static\data\entities\date.csv', 'w')
        # output_f.write('date\n')
        # for j in range(15, 45):
        #     temp_time = self.base_time + self.date_length * j
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(temp_time))
        #     output_f.write('%s\n' % str_time)
        # output_f.close()

        # 输出实体统计
        output_f = open(ur'..\static\data\entities\entities_count.csv', 'w')
        output_f.write('date_index,entity_index,count\n')
        for j in range(15, 45):
            # temp_time = self.base_time + self.date_length * j
            # str_time = time.strftime("%Y-%m-%d",time.localtime(temp_time))
            for i in range(0, self.entity_num):
                output_f.write('%d,%d,%d\n' % (j - 15, i ,self.entities_day_count_list[i][j]))
        output_f.close()

        # 输出每一天每个实体占的比例
        temp_day_count = []
        for j in range(0, self.total_day):
            temp_day_count.append(0.0)
            for i in range(0, self.entity_num):
                temp_day_count[j] += (self.entities_day_count_list[i][j] + 1)
        output_f = open(ur'..\static\data\entities\entities_percent.csv', 'w')
        for i in range(0, self.entity_num):
            output_f.write('%s,' % self.entities_list[i])
            for j in range(15, 45):
                output_f.write('%f,' %((self.entities_day_count_list[i][j] + 1)/ temp_day_count[j]))
            output_f.write('\n')
        output_f.close()

    # 7.关系分析
    def relationAnalyze(self):
        print 'Process 7: relation analyze'
        # self.contentDependenceAnalysis()
        # self.readContentDependenceAnalysis()
        self.eventReferenceAnalysis()
        self.temporalProximityAnalysis()
        self.eventMapConstruction()

    # 7.1
    def readContentDependenceAnalysis(self):
        print 'read Content Dependence Analysis'
        self.Cd_value = []
        for i in range(0, self.represent_news_num):
            self.Cd_value.append([])
            for j in range(0, self.represent_news_num):
                self.Cd_value[i].append(0)

        input_f = open(ur'..\static\data\relation\ContentDependence.csv')
        sentences = input_f.readlines()
        for i in range(0, self.represent_news_num):
            temp = sentences[i].split(',')
            for j in range(0, self.represent_news_num):
                self.Cd_value[i][j] = float(temp[j])
        input_f.close()

    # 7.1
    def contentDependenceAnalysis(self):
        print 'Content Dependence Analysis'

        # 获取每两个特征的互信息量
        self.mutual_information = {}
        for i in range(0, self.represent_news_num):
            # print i
            for s in range(0, len(self.represent_news_features[i])):
                for t in range(s + 1, len(self.represent_news_features[i])):
                    a = self.represent_news_features[i][s]
                    b = self.represent_news_features[i][t]
                    if a == b:
                        continue
                    if self.represent_news_features[i][s] > self.represent_news_features[i][t]:
                        a = self.represent_news_features[i][t]
                        b = self.represent_news_features[i][s]

                    str = ur'%s,%s' % (a,b)
                    if self.mutual_information.has_key(str):
                        self.mutual_information[str] += 1
                    else:
                        self.mutual_information[str] = 1

        # output_f = open(ur'..\static\data\relation\mutual_information.csv', 'w')
        # for word, weight in self.mutual_information.items():
        #     output_f.write('%s,%d\n' % (word, weight))
        # output_f.close()

        # 计算每两则新闻之间的关系
        # Content Dependence Analysis
        self.Cd_value = []
        for i in range(0, self.represent_news_num):
            self.Cd_value.append([])
            for j in range(0, self.represent_news_num):
                self.Cd_value[i].append(0)
        for i in range(0, self.represent_news_num):
            print i
            for j in range(i + 1, self.represent_news_num):
                iu_value = 0
                for s in range(0, len(self.represent_news_features[i])):
                    for t in range(0, len(self.represent_news_features[j])):
                        f_a = self.represent_news_features[i][s]
                        f_b = self.represent_news_features[j][t]
                        if f_a == f_b:
                            continue
                        if f_a > f_b:
                            f_a = self.represent_news_features[j][t]
                            f_b = self.represent_news_features[i][s]
                        str = ur'%s,%s' % (f_a, f_b)
                        if self.mutual_information.has_key(str):
                            # print f_a, f_b, str
                            iu_st = self.mutual_information[str]
                            iu_s = self.represent_news_allfeatures[f_a]
                            iu_t = self.represent_news_allfeatures[f_b]
                            temp = iu_st *1.0/self.represent_news_num * math.log10((iu_st *self.represent_news_num)/(iu_s*iu_t*1.0))
                            iu_value += temp
                            # print f_a, iu_s, f_b, iu_t, iu_st, temp
                self.Cd_value[i][j] = iu_value/(len(self.represent_news_features[i]) * len(self.represent_news_features[j]))
                self.Cd_value[j][i] = self.Cd_value[i][j]

        # 归一化
        max_value = 0.0
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                if self.Cd_value[i][j] > max_value:
                    max_value = self.Cd_value[i][j]
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                self.Cd_value[i][j] /= max_value

        output_f = open(ur'..\static\data\relation\ContentDependence.csv', 'w')
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                output_f.write('%f,' % (self.Cd_value[i][j]))
            output_f.write('\n')
        output_f.close()

    # 7.2
    def eventReferenceAnalysis(self):
        print 'Event Reference Analysis'
        self.core_feature_num = 10

        # 找出关键特征词
        represent_news_featuresWeight_list = []
        self.core_features = []
        self.core_features_tag = []
        self.core_features_weight = []
        for i in range(0, self.represent_news_num):
            represent_news_featuresWeight_list.append([])
            self.core_features.append([])
            self.core_features_tag.append([])
            self.core_features_weight.append([])
            count = 0.0
            for j in range(0, len(self.represent_news_features[i])):
                count += self.represent_news_features_count[i][j]
            for j in range(0, len(self.represent_news_features[i])):
                if len(self.represent_news_features[i][j]) > 1:
                    weight_value = (self.represent_news_features_count[i][j]/count) * (1.0/self.represent_news_allfeatures[self.represent_news_features[i][j]])
                    represent_news_featuresWeight_list[i].append([j,weight_value])
                # print self.represent_news_features_count[i][j], self.represent_news_allfeatures[self.represent_news_features[i][j]], weight_value
            represent_news_featuresWeight_list[i].sort(key=lambda l:l[1],reverse=True)
            for s in range(0, self.core_feature_num):
                # print i, represent_news_featuresWeight_list[i][s][0], represent_news_featuresWeight_list[i][s][1]
                # print self.represent_news_features[i][represent_news_featuresWeight_list[i][s][0]]
                self.core_features[i].append(self.represent_news_features[i][represent_news_featuresWeight_list[i][s][0]])
                self.core_features_tag[i].append(self.represent_news_features_tags[i][represent_news_featuresWeight_list[i][s][0]])
                self.core_features_weight[i].append(represent_news_featuresWeight_list[i][s][1])

        output_f = open(ur'..\static\data\relation\core_features.csv', 'w')
        for i in range(0, self.represent_news_num):
            for s in range(0, self.core_feature_num):
                output_f.write('%s%s,' % (self.core_features[i][s], self.core_features_tag[i][s]))
            output_f.write('\n')
        output_f.close()


        # 计算 Event Reference
        self.ER_value = []
        for i in range(0, self.represent_news_num):
            self.ER_value.append([])
            for j in range(0, self.represent_news_num):
                if i == j :
                    self.ER_value[i].append(0)
                else:
                    temp_er_value = 0.0
                    for s in range(0, self.core_feature_num):
                        # print i, self.core_features[i][s], self.core_features[i][s] in self.represent_news_features[j]
                        if self.core_features[i][s] in self.represent_news_features[j]:
                            index = self.represent_news_features[j].index(self.core_features[i][s])
                            # temp_er_value += (self.represent_news_features_count[j][index] * self.core_features_weight[i][s])
                            temp_er_value += self.represent_news_features_count[j][index]
                    temp_er_value /= self.core_feature_num
                    self.ER_value[i].append(temp_er_value + 0.05)

        # 归一化
        max_value = 0.0
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                if self.ER_value[i][j] > max_value:
                    max_value = self.ER_value[i][j]
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                self.ER_value[i][j] /= max_value

        output_f = open(ur'..\static\data\relation\EventReference.csv', 'w')
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                output_f.write('%f,' % (self.ER_value[i][j]))
            output_f.write('\n')
        output_f.close()

    # 7.3
    def temporalProximityAnalysis(self):
        print 'Temporal Proximity Analysis'
        self.u_value = 0.5
        self.TP_value = []
        for i in range(0, self.represent_news_num):
            self.TP_value.append([])
            for j in range(0, self.represent_news_num):
                if i == j :
                    self.TP_value[i].append(0.0)
                else:
                    news_id_i = self.represent_news_index[i]
                    news_id_j = self.represent_news_index[j]
                    dayIndex_i = self.news_dayIndex_list[news_id_i]
                    dayIndex_j = self.news_dayIndex_list[news_id_j]
                    if dayIndex_j >= dayIndex_i:
                        temp_value = math.pow(3, self.u_value * (dayIndex_i - dayIndex_j)/self.total_day )
                        self.TP_value[i].append(temp_value)
                    else:
                        self.TP_value[i].append(0.0)

        output_f = open(ur'..\static\data\relation\TemporalProximity.csv', 'w')
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                news_id_i = self.represent_news_index[i]
                news_id_j = self.represent_news_index[j]
                dayIndex_i = self.news_dayIndex_list[news_id_i]
                dayIndex_j = self.news_dayIndex_list[news_id_j]
                output_f.write('%d:%d:%f,' % (dayIndex_i,dayIndex_j, self.TP_value[i][j]))
            output_f.write('\n')
        output_f.close()

    # 7.4 得到事件演变的结果
    def eventMapConstruction(self):
        print 'Event Map Construction'

        # construct map
        self.Tem_value = []
        for i in range(0, self.represent_news_num):
            self.Tem_value.append([])
            for j in range(0, self.represent_news_num):
                if i == j:
                    self.Tem_value[i].append(0.0)
                else:
                    self.Tem_value[i].append(self.Cd_value[i][j]*(self.ER_value[i][j])*self.TP_value[i][j])

        # 归一化
        max_value = 0.0
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                if self.Tem_value[i][j] > max_value:
                    max_value = self.Tem_value[i][j]
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                self.Tem_value[i][j] /= max_value

        output_f = open(ur'..\static\data\relation\EventMap.csv', 'w')
        # for i in range(0, self.represent_news_num):
        #     output_f.write('%d,' % i)
        for i in range(0, self.represent_news_num):
            # output_f.write('%d,' % i)
            for j in range(0, self.represent_news_num):
                output_f.write('%f,' % (self.Tem_value[i][j]))
            output_f.write('\n')
        output_f.close()

    # 8.情感分析
    def sentimentAnalyze(self):
        print '8.Sentiment Analysis'
        # self.comment_num = 20

        # 统计每种句子的个数
        # count_1 = 0
        # count_2 = 0
        # count_3 = 0
        # for i in range(0, self.comment_num):
        #     if self.comment_synTag_list[i] == 0:
        #         self.comment_sentiment_list[i] = -1
        #         count_1 += 1
        #     elif self.comment_synTag_list[i] == 1:
        #         self.comment_sentiment_list[i] = -2
        #         count_2 += 1
        #     elif self.comment_synTag_list[i] == 2:
        #         count_3 += 1
        # print count_1, count_2, count_3

        sentiment_word_list = []
        for i in range(0, self.comment_num):
            sentiment_word_list.append([])
            if i % 500 == 0:
                print i
            sentiment_value = 0
            words = self.comment_posTaging_list[i].split('^')
            if len(words) == 1:
                continue
            for w in words:
                temp = w.split(':',1)
                word = temp[0]
                flag = temp[1]
                if flag[0] == 'a' or 1:
                    if word in self.positive_word_list:
                        sentiment_word_list[i].append(word)
                        sentiment_value += 1
                    elif word in self.negative_word_list:
                        sentiment_word_list[i].append(word)
                        sentiment_value -= 1
            self.comment_sentiment_list[i] = sentiment_value
            if self.comment_synTag_list[i] == 1:
                self.comment_sentiment_list[i] *= -1

        output_f = open(ur'..\static\data\sentiment\comment.csv', 'w')
        for i in range(0, self.comment_num):
            if self.comment_sentiment_list[i] != 0:
                output_f.write('%d\t%d\t%s\n' % (self.comment_sentiment_list[i], self.comment_synTag_list[i], self.comment_body_list[i]))
                for word in sentiment_word_list[i]:
                    output_f.write('%s '% word)
                output_f.write('\n')
        output_f.close()

        # self.sentimentDayCount()
        self.getPosNegFeatures()

    # 8.1 情感的日统计
    def sentimentDayCount(self):
        print "Process : sentiment day count"

        # day count
        self.sentiment_day_count = []
        for i in range(0, self.total_day):
            self.sentiment_day_count.append([0,0,0])

        # 评论的统计
        for i in range(0, self.comment_num):
            day = (self.comment_time_list[i] - self.base_time)/86400
            if self.comment_sentiment_list[i] > 0:
                self.sentiment_day_count[day][0] += 1
            elif self.comment_sentiment_list[i] < 0:
                self.sentiment_day_count[day][1] += 1
            else:
                self.sentiment_day_count[day][2] += 1


        # 输出统计
        output_f = open(ur'..\static\data\sentiment\sentiment_day_count.csv', 'w')
        index = 0
        for i in range(0, self.total_day):
            sec_time = self.base_time + 86400*i
            str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
            output_f.write('%s\t%d\t%d\t%d\n' % (str_time, self.sentiment_day_count[i][0], self.sentiment_day_count[i][1], self.sentiment_day_count[i][2]))
        output_f.close()

    # 8.2 正负面高频特征提取
    def getPosNegFeatures(self):
        # 获取正负面特征词
        # sutiable_flag_str = ['nv','vn','nd','dn','dv','vd','na','an']
        sutiable_flag_str = ['nv','dn','dv','na','an']

        positive_sentence_count = 0
        negative_sentence_count = 0
        positive_features_dict = {}
        negative_features_dict = {}
        for i in range(0, self.comment_num):
            if self.comment_sentiment_list[i] != 0:
                words = self.comment_posTaging_list[i].split('^')

                pre_word = ''
                pre_flag = '-'
                for w in words:
                    temp = w.split(':',1)
                    word = temp[0]
                    flag = temp[1]

                    # 使用单个词
                    # if (flag[0] == 'v') and len(word) > 3:
                    #     c_word = word + flag[0]
                    #     if self.comment_sentiment_list[i] > 0:
                    #         if positive_features_dict.has_key(c_word):
                    #             positive_features_dict[c_word] += 1
                    #         else:
                    #             positive_features_dict[c_word] = 1
                    #     elif self.comment_sentiment_list[i] < 0:
                    #         if negative_features_dict.has_key(c_word):
                    #             negative_features_dict[c_word] += 1
                    #         else:
                    #             negative_features_dict[c_word] = 1

                    # 使用组合词
                    flag_str = pre_flag[0] + flag[0]
                    if (flag_str in sutiable_flag_str):
                        combine_word = pre_word + word # + flag_str
                        if self.comment_sentiment_list[i] > 0:
                            if positive_features_dict.has_key(combine_word):
                                positive_features_dict[combine_word] += 1
                            else:
                                positive_features_dict[combine_word] = 1
                        elif self.comment_sentiment_list[i] < 0:
                            if negative_features_dict.has_key(combine_word):
                                negative_features_dict[combine_word] += 1
                            else:
                                negative_features_dict[combine_word] = 1
                    pre_word = word
                    pre_flag = flag


        print positive_sentence_count
        print negative_sentence_count

        positive_features_list = sorted(positive_features_dict.iteritems(), key=lambda l:l[1],reverse=True)
        negative_features_list = sorted(negative_features_dict.iteritems(), key=lambda l:l[1],reverse=True)

        output_features_num = 50
        output_f = open(ur'..\static\data\sentiment\positive_features.csv', 'w')
        output_f.write('feature,count\n')
        for i in range(0, output_features_num):
            output_f.write('%s,%d\n' % (positive_features_list[i][0], positive_features_list[i][1]))
        output_f.close()

        output_f = open(ur'..\static\data\sentiment\negative_features.csv', 'w')
        output_f.write('feature,count\n')
        for i in range(0, output_features_num):
            output_f.write('%s,%d\n' % (negative_features_list[i][0], negative_features_list[i][1]))
        output_f.close()

        positive_features_str = ''
        negative_features_str = ''
        for i in range(0, output_features_num):
            positive_features_str += ('%s,%d\n' % (positive_features_list[i][0], positive_features_list[i][1]))
            negative_features_str += ('%s,%d\n' % (negative_features_list[i][0], negative_features_list[i][1]))
        positive_features_str = positive_features_str[:-1]
        negative_features_str = negative_features_str[:-1]
        update_sql = "update result_topic set feature_positive = '%s', feature_negative = '%s' where id = %d" % (positive_features_str.encode('utf-8'), negative_features_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

        # output_f = open(ur'..\static\data\sentiment\positive_features.csv', 'w')
        # for i in range(0, len(positive_features_list)):
        #     output_f.write('%s\t%d\n' % (positive_features_list[i][0], positive_features_list[i][1]))
        # output_f.close()
        #
        # output_f = open(ur'..\static\data\sentiment\negative_features.csv', 'w')
        # for i in range(0, len(negative_features_list)):
        #     output_f.write('%s\t%d\n' % (negative_features_list[i][0], negative_features_list[i][1]))
        # output_f.close()

    # 8.3 多类情感分析
    def mutiSentimentAnalyze(self):
        print "sentiment analysis use 7 category."

        whole_sentiment_value = []
        total_sentiment_value = [0,0,0,0,0,0,0]
        for i in range(0, self.total_day):
            whole_sentiment_value.append([0,0,0,0,0,0,0])

        for i in range(0, self.comment_num):
            if i % 500 == 0:
                print i

            sentiment_value = 0
            # print self.comment_list_body[i]
            words = self.comment_posTaging_list[i].split('^')
            if len(words) == 1:
                continue
            for w in words:
                temp = w.split(':',1)
                word = temp[0]
                flag = temp[1]
                if word in self.muti_sentiment_word_list:
                    sentiment_index = self.muti_sentiment_word_list.index(word)
                    whole_sentiment_value[self.comment_dayIndex_list[i]][self.muti_sentiment_type_list[i]] += 1
                    total_sentiment_value[self.muti_sentiment_type_list[i]] += 1

        total_sentiment_str = ''
        for i in range(0, 7):
            total_sentiment_str += ('%s\n' % total_sentiment_value[i])
        total_sentiment_str = total_sentiment_str[:-1]

        whole_sentiment_str = ''
        for i in range(0, self.total_day):
            sec_time = self.base_time + 86400*i
            str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
            whole_sentiment_str += ('%s,%d,%d,%d,%d,%d,%d,%d,%d\n' % (str_time,self.comment_day_count[i],whole_sentiment_value[i][0],whole_sentiment_value[i][1],whole_sentiment_value[i][2] \
                                                             ,whole_sentiment_value[i][3],whole_sentiment_value[i][4],whole_sentiment_value[i][5],whole_sentiment_value[i][6]))
        whole_sentiment_str = whole_sentiment_str[:-1]

        update_sql = "update result_topic set sentiment_piechart = '%s', sentiment_stream = '%s' where id = %d" % (total_sentiment_str.encode('utf-8'), whole_sentiment_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()


        # output_f = open(ur'..\static\data\sentiment\streamgraph.csv', 'w')
        # output_f.write('date,happiness,good,anger,sadness,fear,evil,surprise\n')
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     output_f.write('%s,%d,%d,%d,%d,%d,%d,%d,%d\n' % (str_time,self.comment_day_count[i],whole_sentiment_value[i][0],whole_sentiment_value[i][1],whole_sentiment_value[i][2] \
        #                                                      ,whole_sentiment_value[i][3],whole_sentiment_value[i][4],whole_sentiment_value[i][5],whole_sentiment_value[i][6]))
        # output_f.close()

        # output_f = open(ur'..\static\data\sentiment\streamgraphpercent.csv', 'w')
        # output_f.write('date,happiness,good,anger,sadness,fear,evil,surprise\n')
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     count = 0.0
        #     for j in range(0, 7):
        #         whole_sentiment_value[i][j] += 1
        #         count += whole_sentiment_value[i][j]
        #     output_f.write('%s,%f,%f,%f,%f,%f,%f,%f\n' % (str_time, whole_sentiment_value[i][0]/count,whole_sentiment_value[i][1]/count,whole_sentiment_value[i][2]/count \
        #                                                      ,whole_sentiment_value[i][3]/count,whole_sentiment_value[i][4]/count,whole_sentiment_value[i][5]/count,whole_sentiment_value[i][6]/count))
        # output_f.close()

    # 9.事件的日衰减情感, 计算每一个事件评论的衰减过程
    def eventDecreaseRate(self):
        eventDecreaseRate_matrix = []
        for i in range(0, self.represent_news_num):
            eventDecreaseRate_matrix.append([])
            for j in range(0, self.total_day):
                eventDecreaseRate_matrix[i].append(0)
            for j in range(0, self.comment_num):
                if self.comment_newsId_list[j] == self.news_id_list[i]:
                    temp_index = self.comment_dayIndex_list[j]
                    eventDecreaseRate_matrix[i][temp_index] += 1

        # 事件为横轴，单个
        output_f = open(ur'..\static\data\representNews\eventDecreaseRate_single.csv', 'w')
        output_f.write('date,comment_num\n')
        for i in range(0, self.total_day):
            sec_time = self.base_time + 86400*i
            str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
            output_f.write('%s,%d\n' % (str_time,eventDecreaseRate_matrix[42][i]))
        output_f.close()

        # 事件为横轴
        # output_f = open(ur'..\static\data\representNews\eventDecreaseRate.csv', 'w')
        # temp_str = 'date,'
        # for i in range(0, self.represent_news_num):
        #     temp_str += ('%d,' % i)
        # temp_str = temp_str[:-1]
        # output_f.write('%s\n' % temp_str)
        #
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     temp_str = ('%s,' % str_time)
        #     for j in range(0, self.represent_news_num):
        #         temp_str += ('%d,' % eventDecreaseRate_matrix[j][i])
        #     temp_str = temp_str[:-1]
        #     output_f.write('%s\n' % temp_str)
        # output_f.close()

        # 时间为横轴
        # output_f = open(ur'..\static\data\representNews\eventDecreaseRate.csv', 'w')
        # temp_str = 'event,'
        # for i in range(0, self.total_day):
        #     sec_time = self.base_time + 86400*i
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     temp_str += ('%s,' % str_time)
        # temp_str = temp_str[:-1]
        # output_f.write('%s\n' % temp_str)\
        # for i in range(0, self.represent_news_num):
        #     temp_str = ('%d,' % i)
        #     for j in range(0, self.total_day):
        #         temp_str += ('%d,' % eventDecreaseRate_matrix[i][j])
        #     temp_str = temp_str[:-1]
        #     output_f.write('%s\n' % temp_str)
        # output_f.close()

    # 11.地域信息统计
    def commentAreaCount(self):
        print 'comment area count'
        # 34个省级地区，加一个其他地区
        self.area_num = 35
        self.area_name_list = ['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆','北京','天津','上海','重庆','香港','澳门']

        self.area_comment_count = []
        for i in range(0, self.area_num):
            self.area_comment_count.append(0)

        for i in range(0, self.comment_num):
            temp_area = self.comment_area_list[i]
            isfound = 0
            for j in range(0, len(self.area_name_list)):
                if self.area_name_list[j] in temp_area:
                    self.area_comment_count[j] += 1
                    isfound = 1
                    break
            if isfound == 0:
                self.area_comment_count[34] += 1

        # 排序
        temp_sort_list = []
        for i in range(0, self.area_num):
            temp_sort_list.append([i,self.area_comment_count[i]])
        temp_sort_list.sort(key=lambda l:l[1], reverse=True)

        # output_f = open(ur'..\static\data\area\area_count.csv', 'w')
        # output_f.write('area,rank,comment_num,percent\n')
        # for i in range(0, self.area_num):
        #     if temp_sort_list[i][0] != 34:
        #         output_f.write('%s,%d,%d,%f\n' % (self.area_name_list[temp_sort_list[i][0]], i+1, temp_sort_list[i][1], temp_sort_list[i][1] * 1.0/self.comment_num))
        #     else:
        #         output_f.write('其他,%d,%d,%d\n' % (i+1,temp_sort_list[i][1], temp_sort_list[i][1] * 1.0/self.comment_num))
        # output_f.close()

        # area_str = 'area,rank,comment_num,percent\n'
        area_str = ''
        for i in range(0, self.area_num):
            if temp_sort_list[i][0] != 34:
                area_str += ('%s,%d,%d,%f\n' % (self.area_name_list[temp_sort_list[i][0]], i+1, temp_sort_list[i][1], temp_sort_list[i][1] * 1.0/self.comment_num))
            else:
                area_str += ('其他,%d,%d,%d\n' % (i+1,temp_sort_list[i][1], temp_sort_list[i][1] * 1.0/self.comment_num))
        area_str = area_str[:-1]
        update_sql = "update result_topic set area_info = '%s' where id = %d" % (area_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)

        self.conn.commit()
        # self.cursor.close()
        # self.conn.close()

    # 10.生成最佳评论子集
    def generateBestCommentSet(self):
        print 'generate best comment set'
        max_against_num = 0
        self.comment_represent_weight = []
        for i in range(0, self.comment_num):
            self.comment_represent_weight.append(self.comment_against_list[i])
            if self.comment_against_list[i] > max_against_num:
                max_against_num = self.comment_against_list[i]
            # 加v与非加v用户
            # if self.comment_verifiedType_list[i] != 0:
            #     self.comment_represent_weight.append(self.comment_against_list[i]*2)
            # else:
            #     self.comment_represent_weight.append(self.comment_against_list[i])

        # 排序
        temp_sort_list = []
        for i in range(0, self.comment_num):
            temp_sort_list.append([i, self.comment_represent_weight[i]])
        temp_sort_list.sort(key=lambda l:l[1], reverse=True)


        # output_f = open(ur'..\static\data\commentset\comments.csv', 'w')
        # # output_f.write('area,comment_num\n')
        # for i in range(0, 100):
        #     index = temp_sort_list[i][0]
        #     sec_time = self.base_time + 86400*self.comment_dayIndex_list[index]
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     output_f.write('%d,%s,%s\n' % (self.comment_against_list[index], str_time, self.comment_body_list[index]))
        # output_f.close()

        top_comment_str = ''
        for i in range(0, 100):
            index = temp_sort_list[i][0]
            sec_time = self.base_time + 86400*self.comment_dayIndex_list[index]
            str_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(sec_time))
            top_comment_str += ('%d,%d,%s,%s,%s,%s\n' % (self.comment_id[index],self.comment_against_list[index], self.comment_area_list[index], str_time, self.comment_nickId_list[index], self.comment_body_list[index]))
        top_comment_str = top_comment_str[:-1]

        # 获取评论的所有特征
        self.comment_all_featuers = {}
        temp_total = 0
        for i in range(0, self.comment_num):
            words = self.comment_posTaging_list[i].split('^')
            if len(words) == 1:
                continue
            for w in words:
                temp = w.split(':',1)
                word = temp[0]
                temp_total += 1
                if self.comment_all_featuers.has_key(word):
                    self.comment_all_featuers[word] += 1
                else:
                    self.comment_all_featuers[word] = 1

        for word, value in self.comment_all_featuers.iteritems():
            self.comment_all_featuers[word] = value * 1.0/ temp_total
            # print value, self.comment_all_featuers[word]

        # 计算评论的信息熵
        entropy_value_list = []
        feature_count_list = []
        for i in range(0, self.comment_num):
            entropy_value_list.append(0)
            feature_count_list.append(0)
            words = self.comment_posTaging_list[i].split('^')
            if len(words) == 1:
                continue
            for w in words:
                temp = w.split(':',1)
                word = temp[0]
                entropy_value_list[i] -= self.comment_all_featuers[word] * math.log10(self.comment_all_featuers[word])
                feature_count_list[i] += 1

        # 考虑推荐集合的信息熵
        self.best_comment_num = 20
        self.best_comment_index = []
        self.best_comment_weight = 0.5

        best_comment_entropy_value = 0
        best_comment_feature_count = 0
        best_comment_against_count = 0
        best_comment_h = 0
        # 获取初始推荐集合
        for i in range(0, self.best_comment_num):
            index = temp_sort_list[i][0]
            self.best_comment_index.append(index)
            best_comment_entropy_value += entropy_value_list[index]
            best_comment_feature_count += feature_count_list[index]
            best_comment_against_count += self.comment_against_list[index]
            best_comment_h = self.best_comment_weight * best_comment_entropy_value / math.log10(best_comment_feature_count) + (1 - self.best_comment_weight) * best_comment_against_count * 1.0 / (max_against_num * self.best_comment_num)
            # print best_comment_h, best_comment_entropy_value / math.log10(best_comment_feature_count), best_comment_against_count * 1.0 / (max_against_num * self.best_comment_num)

        # 循环更新集合
        for j in range(self.best_comment_num, 100):
            new_index = temp_sort_list[j][0]
            max_e_v = 0
            max_f_c = 0
            max_a_c = 0.0
            max_h = 0
            max_index = 0
            for i in range(0, self.best_comment_num):
                old_index = self.best_comment_index[i]
                temp_e_v = best_comment_entropy_value - entropy_value_list[old_index] + entropy_value_list[new_index]
                temp_f_c = best_comment_feature_count - feature_count_list[old_index] + feature_count_list[new_index]
                temp_a_c = best_comment_against_count - self.comment_against_list[old_index] + self.comment_against_list[new_index]
                temp_h =  self.best_comment_weight * temp_e_v / math.log10(temp_f_c) + (1 - self.best_comment_weight) * temp_a_c * 1.0 / (max_against_num * self.best_comment_num)
                if temp_h > max_h:
                    max_e_v = temp_e_v
                    max_f_c = temp_f_c
                    max_a_c = temp_a_c
                    max_h = temp_h
                    max_index = i
            if max_h > best_comment_h:
                self.best_comment_index[max_index] = new_index
                best_comment_entropy_value = max_e_v
                best_comment_feature_count = max_f_c
                best_comment_against_count = max_a_c
                best_comment_h = max_h

        # output_f = open(ur'..\static\data\commentset\best_comments.csv', 'w')
        # for i in range(0, self.best_comment_num):
        #     index = self.best_comment_index[i]
        #     sec_time = self.base_time + 86400*self.comment_dayIndex_list[index]
        #     str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
        #     output_f.write('%d,%s,%s\n' % (self.comment_against_list[index], str_time, self.comment_body_list[index]))
        # output_f.close()

        best_comment_str = ''
        for i in range(0, self.best_comment_num):
            index = self.best_comment_index[i]
            sec_time = self.base_time + 86400*self.comment_dayIndex_list[index]
            str_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(sec_time))
            best_comment_str += ('%d,%d,%s,%s,%s,%s\n' % (self.comment_id[index],self.comment_against_list[index], self.comment_area_list[index], str_time, self.comment_nickId_list[index], self.comment_body_list[index]))
        best_comment_str = best_comment_str[:-1]

        update_sql = "update result_topic set comment_best = '%s', comment_top = '%s' where id = %d" % (best_comment_str.encode('utf-8'), top_comment_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

    # 10.生成最佳新闻集合
    def generateBestNewsSet(self):
        print 'generate best news set'

        # 对新闻排序
        temp_news_comment_list = []
        for i in range(0, self.news_num):
            temp_news_comment_list.append([i, self.news_commentNum_list[i]])
            # print news_comment_dayIndex_list[i]
        temp_news_comment_list.sort(key=lambda l:(l[1]),reverse=True)

        # index = temp_news_comment_list[0][0]
        # for i in range(0 ,len(self.news_body_list[index])):
        #     self.news_body_list[index][i] = self.news_body_list[index][i].encode('utf-8')
        # print self.news_body_list[index]
        # return

        top_news_str = ''
        for i in range(0, 20):
            index = temp_news_comment_list[i][0]
            if index == 363:
                continue
            sec_time = self.base_time + 86400*self.news_dayIndex_list[index]
            str_time = time.strftime("%Y-%m-%d",time.localtime(sec_time))
            # self.news_title_list[index].encode('utf-8')
            # print type(self.news_body_list[index])
            temp = self.news_body_list[index].decode('utf-8')
            # print temp

            # self.news_body_list[index] = '测试'
            top_news_str += ('%d,%d,%s,%s,%s,%s\n' % (index, self.news_commentNum_list[index], self.news_title_list[index].encode('utf-8'), str_time, self.news_url_list[index], self.news_body_list[index]))
        top_news_str = top_news_str[:-1]

        print top_news_str

        update_sql = "update result_topic set news_top = '%s' where id = %d" % (top_news_str, self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

        # max_against_num = 0
        # self.news_represent_weight = []
        # for i in range(0, self.comment_num):
        #     self.comment_represent_weight.append(self.comment_against_list[i])
        #     if self.comment_against_list[i] > max_against_num:
        #         max_against_num = self.comment_against_list[i]
        #
        # # 排序
        # temp_sort_list = []
        # for i in range(0, self.comment_num):
        #     temp_sort_list.append([i, self.comment_represent_weight[i]])
        # temp_sort_list.sort(key=lambda l:l[1], reverse=True)



if __name__ == "__main__":
    test = EventEvolution(0)

    # 地域信息
    # test.commentAreaCount()

    # 特征分析
    # test.featuresCount()

    # 统计高频词组，用于绘制字云图
    # test.getFrequentFeatures()
