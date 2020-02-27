#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class EventEvolutionAnalysis():
    def __init__(self):
        # open database
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
        self.cursor = self.conn.cursor()
        self.conn.select_db('newsdemo')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

        self.topic_id = 0
        self.total_day = 75
        self.readRepresentNews()
        self.readCoreFeatures()
        self.readEventTable()

        self.getEventRelations()
        self.getEventPostion()

    def readRepresentNews(self):
        self.represent_news_list = []
        self.represent_news_time_list = []
        self.represent_news_day_list = []
        self.represent_news_comNum_list = []

        input_f = open(ur'..\static\data\representNews\represent_news.csv')
        sentences = input_f.readlines()
        for sen in sentences:
            temp = sen.split(',')
            self.represent_news_time_list.append(temp[0].strip())
            self.represent_news_day_list.append(temp[1].strip())
            self.represent_news_list.append(temp[2].strip())
            self.represent_news_comNum_list.append(int(temp[3].strip()))
        self.represent_news_num = len(self.represent_news_list)
        input_f.close()
        # print self.represent_news_num

    def readCoreFeatures(self):
        self.represent_news_coreFeatures_list = []

        input_f = open(ur'..\static\data\relation\core_features.csv')
        sentences = input_f.readlines()
        for sen in sentences:
            self.represent_news_coreFeatures_list.append(sen.strip())
        input_f.close()

    def readEventTable(self):
        self.Tem_value = []
        for i in range(0, self.represent_news_num):
            self.Tem_value.append([])
            for j in range(0, self.represent_news_num):
                self.Tem_value[i].append(0)

        input_f = open(ur'..\static\data\relation\EventMap.csv')
        sentences = input_f.readlines()
        # print len(sentences)
        for i in range(0, self.represent_news_num):
            temp = sentences[i].split(',')
            for j in range(0, self.represent_news_num):
                self.Tem_value[i][j] = float(temp[j])
            #     print self.Tem_value[i][j]
            # print '\n'
        input_f.close()

    def getEventPostion(self):
        max_comment_num = 0
        max_relation_num = 0
        self.represent_news_weight = []
        for i in range(0, self.represent_news_num):
            if self.represent_news_comNum_list[i] > max_comment_num:
                max_comment_num = self.represent_news_comNum_list[i]
            if self.event_relation_num[i] > max_relation_num:
                max_relation_num = self.event_relation_num[i]
        for i in range(0, self.represent_news_num):
            comment_weight = math.ceil((self.represent_news_comNum_list[i])*10.0/max_comment_num)+4
            relation_weight = math.ceil((self.event_relation_num[i])*10.0/max_relation_num)+4
            print i, self.represent_news_comNum_list[i], comment_weight, self.event_relation_num[i], relation_weight
            self.represent_news_weight.append((comment_weight+relation_weight)/2)

        self.news_postion_list = []
        for i in range(0, self.represent_news_num):
            self.news_postion_list.append([])
            # p_x = int(self.represent_news_day_list[i]) + random.randint(0,9)*0.1 - 0.5
            p_x = int(self.represent_news_day_list[i])
            p_y = random.randint(0, 100)/10.0
            self.news_postion_list[i].append(p_x)
            self.news_postion_list[i].append(p_y)

            # print self.represent_news_day_list[i], p_x

        event_node_str = ''
        for i in range(0, self.represent_news_num):
            event_node_str += ('%s,%d,%f,%d,%s\n' % (self.represent_news_time_list[i], self.news_postion_list[i][0], self.news_postion_list[i][1], self.represent_news_weight[i],self.represent_news_list[i]))
        event_node_str = event_node_str[:-1]
        update_sql = "update result_topic set event_node = '%s' where id = %d" % (event_node_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()


        # output_f = open(ur'dataFolder\results\node.csv', 'w')
        # output_f.write('date,position_x,position_y,weight,name\n')
        # for i in range(0, self.represent_news_num):
        # # for i in range(0, 15):
        #     output_f.write('%s,%d,%f,%d,%s\n'% (self.represent_news_time_list[i], self.news_postion_list[i][0], self.news_postion_list[i][1], self.represent_news_weight[i],self.represent_news_list[i]))
        # output_f.close()

    def getEventRelations(self):
        self.event_relation_num = []

        EEG_postion_list = []

        EEG_day_list = []
        for i in range(0, self.total_day):
            EEG_day_list.append([])

        sort_tem_list = []

        max_value = 0.0
        min_value = 1.0
        avg_value = 0.0
        for i in range(0, self.represent_news_num):
            for j in range(0, self.represent_news_num):
                sort_tem_list.append([i,j,self.Tem_value[i][j]])
                avg_value += self.Tem_value[i][j]
                if self.Tem_value[i][j] > max_value:
                    max_value = self.Tem_value[i][j]
                elif self.Tem_value[i][j] < min_value:
                    min_value = self.Tem_value[i][j]
        sort_tem_list.sort(key=lambda x:x[2], reverse = True)
        index = int(len(sort_tem_list) * 0.01)
        threshold_value = sort_tem_list[index][2]
        weak_threshold_value = sort_tem_list[ int(len(sort_tem_list) * 0.05)][2]

        print threshold_value, weak_threshold_value

        temp_Tem_value = []
        for i in range(0, self.represent_news_num):
            self.event_relation_num.append(0)

            temp_Tem_value.append([])
            for j in range(0, self.represent_news_num):
                temp_Tem_value[i].append([j,self.Tem_value[i][j]])
            temp_Tem_value[i].sort(key=lambda x:x[1], reverse = True)

            # 产生关系边
            for j in range(0, self.represent_news_num):
                if temp_Tem_value[i][j][1] > threshold_value:
                    self.event_relation_num[i] += 1
                    EEG_postion_list.append([i,temp_Tem_value[i][j][0],2])
                    # if edge_count > int(self.represent_news_num * 0.15):
                    #     break
                if j == 0:
                    if temp_Tem_value[i][j][1] < threshold_value and temp_Tem_value[i][j][1] > weak_threshold_value and i < temp_Tem_value[i][j][0]:
                        self.event_relation_num[i] += 1
                        EEG_postion_list.append([i,temp_Tem_value[i][j][0],1])


        # output_f = open(ur'dataFolder\results\EventMap_name.csv', 'w')
        # for i in range(0, self.represent_news_num):
        #     output_f.write('%f\n' % self.Tem_value[i][j])
        #     output_f.write('%s,%s,%s,%s\n' % (self.represent_news_list[i], self.represent_news_day_list[i], self.represent_news_comNum_list[i], self.represent_news_coreFeatures_list[i]))
        #     is_have = 0
        #     for j in range(0, self.represent_news_num):
        #         if self.Tem_value[i][j] > threshold_value:
        #             is_have = 1
        #             temp_str = '%d->%d' % (i,j)
        #             EEG_day_list[int(self.represent_news_day_list[i])].append(temp_str)
        #
        #             EEG_postion_list.extend([i,j])
        #             # print i, j
        #             output_f.write('%s,%s,%s,%s\n' % (self.represent_news_list[j], self.represent_news_day_list[j], self.represent_news_comNum_list[j], self.represent_news_coreFeatures_list[j]))
        #     if is_have == 0:
        #         EEG_day_list[int(self.represent_news_day_list[i])].append(str(i))
        #         # EEG_postion_list.extend([self.news_postion_list[i][0], self.news_postion_list[i][1], self.news_postion_list[i][0] ,self.news_postion_list[i][1]])
        # output_f.close()


        # output_f = open(ur'dataFolder\results\day.csv', 'w')
        # for i in range(0, self.total_day):
        #     output_f.write('%d\t'% i)
        #     for j in range(0, len(EEG_day_list[i])):
        #         output_f.write('%s '% EEG_day_list[i][j] )
        #     output_f.write('\n')
        # output_f.close()

        event_edge_str = ''
        for i in range(0, self.represent_news_num):
            event_edge_str += ('%d,%d,%d\n'% (EEG_postion_list[i][0], EEG_postion_list[i][1], EEG_postion_list[i][2]))
        event_edge_str = event_edge_str[:-1]
        update_sql = "update result_topic set event_edge = '%s' where id = %d" % (event_edge_str.encode('utf-8'), self.topic_id)
        self.cursor.execute(update_sql)
        self.conn.commit()

        # output_f = open(ur'dataFolder\results\edge.csv', 'w')
        # output_f.write('position_1,position_2,weight\n')
        # for i in range(0, len(EEG_postion_list)):
        #     output_f.write('%d,%d,%d\n'% (EEG_postion_list[i][0], EEG_postion_list[i][1], EEG_postion_list[i][2]))
        # output_f.close()

if __name__ == "__main__":
    test = EventEvolutionAnalysis()