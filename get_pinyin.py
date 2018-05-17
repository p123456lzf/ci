# -*- coding:utf-8 -*-
import os.path
from yunjiao import result1,result2

class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file

    # 加载
    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]

    # 获取对应字符串的音调（1,2,3,4,5）
    def hanzi2yindiao(self, string=""):
        result = []
        for char in string:
            key = '%X' % ord(char)
            the_result = []
            for i in self.word_dict.get(key, char).split():
                the_result.append(i[-1:].lower())
            result.append(the_result)
        return result

    # 获取某汉字的韵脚
    def hanzi2yunjiao(self, string=""):
        result = []
        for char in string:
            key = '%X' % ord(char)
            the_result = []
            for i in self.word_dict.get(key, char).split():
                the_result.append(i[-1:].lower())
            result.append(the_result)
        return result

    # 获取完整的拼音
    def hanzi2pinyin(self, string=""):
        result = []
        for char in string:
            key = '%X' % ord(char)
            the_result = []
            for i in self.word_dict.get(key, char).split():
                the_result.append(i.lower())
            result.append(the_result)
        return result

if __name__ == "__main__":
    test = PinYin()
    test.load_word()
    string = "大江东去，浪淘尽的"
    print("in: %s" % string)
    print("out: %s" % str(test.hanzi2pinyin(string=string)))
    print("out: %s" % str(test.hanzi2yindiao(string=string)))
    print("out: %s" % str(test.hanzi2yunjiao(string=string)))
    #print("out: %s" % test.hanzi2pinyin_split(string=string, split="-"))