#!/usr/bin/env python
# -*- coding: utf-8 -*-
from function.preprocess import Preprocess
#from function.syntactic import SyntacticAnalysis
from function.event import EventEvolution

class TopicAnalysis:
    def __init__(self, tid):
         # 基本变量
        self.topic_id = int(tid)
        print 'self.topic_id:', self.topic_id

        # 数据预处理：分词、句法分析
        #Preprocess(tid)

        # 句法分析
        #SyntacticAnalysis(tid)

        # 统计分析
        EventEvolution(tid)
        # 句法分析

if __name__ == "__main__":
    test = TopicAnalysis(3)