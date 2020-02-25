#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import urllib
import urllib2

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

# 哈工大语言云的爬虫, 用于对文本进行句法分析
class Ltp:
    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.url_base = "http://api.ltp-cloud.com/analysis/"
        self.pattern = 'all'
        self.format = 'json'

    # text: utf-8
    def getCon(self, api_key='M5w2V1B4mHGXyUGxrKiDayGKOxaxYoECIDvOhihp', text=''):
        the_data = {
           "api_key": api_key,
           "text": text,
           "format": self.format,
           "pattern": self.pattern
        }
        tar_data = self.postData(the_data)
        content = 'error'
        if True:
            req = urllib2.Request(self.url_base, data=tar_data)
            res = self.opener.open(req)
            if res.getcode() == 403:
                print '该月流量已用完'
            else:
                content = res.read().strip()
            res.close()
        return content

    def postData(self, the_data):
        return urllib.urlencode(the_data)

# 使用哈工大语言云时不能对一些特殊字符或某些字符的组合解析,
# 且这些字符对文本分析没有影响, 因此将其除去
def replaceSpecial(content):
    replace1 = re.compile(ur'%\d+', re.S)
    content = content.decode('utf-8')
    content = re.sub(replace1, u"%", content)
    return content.strip().encode('utf-8')

# 使用哈工大进行句法分析
class Transformer:
    def __init__(self):
        self.ltp_tool = Ltp()
        self.wrong_list = []

    # 对每一篇文档使用哈工大分词, 并存入对应序号的文件中
    # 每一篇文档为多条文本的集合, 一行为一条文本
    def transMyTestSet(self, the_index=0, the_end=10000):
        continue_flag = True
        while continue_flag:
            if the_index == the_end:
                continue_flag = False
            print '正在处理第%d篇文档' % the_index

            input_file = ur'..\data\chaifen\%d.txt' % the_index
            try:
                input_f = open(input_file)
            except:
                return
            the_content = ''
            for line in input_f:
                # 处理掉影响哈工大分词的字符
                sen = replaceSpecial(line.strip()).decode('utf-8')
                # 若文本为空, 则须加上'。', 因为哈工大会忽略为空的一行
                if sen:
                    if sen[-1] != u'?' and sen[-1] != u'？' and sen[-1] != u'.' and sen[-1] != u'！' and sen[-1] != u'。':
                        sen += u'。'
                else:
                    sen += u'。'
                sen += u'\n'
                the_content += sen.encode('utf-8')
            input_f.close()
            trans_content = ''

            try:
                the_content2 = self.ltp_tool.getCon(
                    text=the_content
                )
                for content_line in the_content2:
                    trans_content += content_line.strip()

                print '哈工大句法分析完毕, 现在写入'
                output_file = ur'..\data\chaifen_ltp\%d.txt' % the_index
                output_f = open(output_file, 'w')
                output_f.write('%s' % trans_content)
                output_f.close()
            except:
                self.wrong_list.append(the_index)
                self.transMyTestSet_worng(the_index)

            the_index += 1

    def transMyTestSet_worng(self, index):
        chaifen_number = 15

        print '正在处理第%d篇文档-异常' % index
        input_file = ur'..\data\chaifen\%d.txt' % index
        input_f = open(input_file)
        sentences= input_f.readlines()

        the_contents = []
        for i in range(0, chaifen_number):
            the_contents.append('')

        index_change = chaifen_number*1.0/len(sentences)
        for i in range(0, len(sentences)):
            # 处理掉影响哈工大分词的字符
            sen = replaceSpecial(sentences[i].strip()).decode('utf-8')
            # 若文本为空, 则须加上'。', 因为哈工大会忽略为空的一行
            if sen:
                if sen[-1] != u'?' and sen[-1] != u'？' and sen[-1] != u'.'and sen[-1] != u'！' and sen[-1] != u'。':
                    sen += u'。'
            else:
                sen += u'。'
            sen += u'\n'
            the_contents[int(i*index_change)] += sen.encode('utf-8')
        input_f.close()

        trans_content = ''
        for i in range(0, chaifen_number):
            print '正在处理第%d个子文档' % i
            try:
                the_content3 = self.ltp_tool.getCon(
                    text=the_contents[i]
                )
                trans_content += (the_content3.replace(' ','').replace('\n','')[1:-1] + ',')
            except:
                sens = the_contents[i].split('\n')
                print len(sens)
                for j in range(0, len(sens)-1):
                    try:
                        the_content4 = self.ltp_tool.getCon(
                            text=(sens[j] + u'\n')
                        )
                        # print (the_content4.replace(' ','').replace('\n','')[1:-1] + ',')
                        trans_content += (the_content4.replace(' ','').replace('\n','')[1:-1] + ',')
                    except:
                        print sens[j]
                        trans_content += '[[]],'

        trans_content = u'[' + trans_content[:-1] + u']'
        print trans_content
        print '哈工大句法分析完毕, 现在写入'
        output_file = ur'..\data\chaifen_ltp\%d.txt' % index
        output_f = open(output_file, 'w')
        output_f.write('%s' % trans_content)
        output_f.close()

    def transMyTestSet_s(self, the_index=0, the_end=56):
        continue_flag = True
        while continue_flag:
            if the_index == the_end + 1:
                continue_flag = False
            print '正在处理第%d篇文档' % the_index

            input_file = ur'..\data\chaifen\%d.txt' % the_index
            input_f = open(input_file)
            the_content = ''
            trans_content = ''
            index = 0
            for line in input_f:
                # 处理掉影响哈工大分词的字符
                sen = replaceSpecial(line.strip()).decode('utf-8')
                # 若文本为空, 则须加上'。', 因为哈工大会忽略为空的一行
                if sen:
                    if sen[-1] != u'?' and sen[-1] != u'？' and sen[-1] != u'.':
                        sen += u'。'
                else:
                    sen += u'。'
                sen += u'\n'
                the_content += sen.encode('utf-8')
                the_content2 = ''
                try:
                    the_content2 =self.ltp_tool.getCon(
                        text=sen.encode('utf-8')
                    )
                    for content_line in the_content2:
                        trans_content += content_line.strip()
                except:
                    print sen.encode('utf-8')
                print index
                index += 1

            input_f.close()

            print '哈工大句法分析完毕, 现在写入'

            output_file = ur'..\data\chaifen_ltp\%d.txt' % the_index
            output_f = open(output_file, 'w')
            output_f.write('%s' % trans_content)
            output_f.close()

            the_index += 1

    # 查看哈工大分词存入的文件
    def lookFile(self, input_file):
        input_f = open(input_file)
        for line in input_f:
            count = 0
            line_json = json.loads(line.strip(), object_hook=_decode_dict)
            # print line_json
            for i in line_json:
                count += 1
                # for j in i[0]:
                #     print count, j['cont']
            print 'count:%d' % count
        input_f.close()
        return  count
