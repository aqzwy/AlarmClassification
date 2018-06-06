import numpy as np
import pandas as pd
import jieba.posseg as pseg
import re
import pickle


class dataProcess():
    def __init__(self, data_url, save_url, stop_word_url, flag):
        self.data_url = data_url
        self.stop_word_url = stop_word_url
        self.save_url = save_url
        self.threshold = 0

        self.stop_word = []
        self.data = []
        self.label_dict = {}
        self.flag = flag

        self.l1 = []
        self.l2 = []
        self.l3 = []
        self.delete_list = []

        self.pre_process()

    def read_data(self):
        data = pd.read_excel(self.data_url, sheet_name = 'Sheet1', encoding = 'gbk')
        drop_col = ['案件类型', '角色编码', '流程ID', '流程名称', '分类ID', '分类名称', '有疑问']
        data = data.drop(drop_col, axis = 1)
        return data

    def read_stop_words(self):
        f = open(self.stop_word_url, encoding = 'gbk')
        self.stop_words = [line.strip() for line in f]
        f.close()
        return self.stop_words

    def get_label_dict(self, data):
        label_set = list(set(data['案件类别'].values))
        self.label_dict = dict(zip(label_set, range(1, 1 + len(label_set))))
        with open(self.save_url+ '\label_dict.pickle', 'wb') as f:
            f.truncate()
            pickle.dump(dict((v, k) for k, v in self.label_dict.items()), f)
        return self.label_dict

    def participial(self, data):
        '''
            This function filters non-Chinese, stop words, numbers, punctuation and space
        '''
        data = re.sub(r'[^\u4e00-\u9fa5]', '', data)
        number = re.compile(u'([0-9]|[0-9]+[,]*[0-9]+.[0-9]+|[A-z])')
        pattern = re.compile(number)
        all = pattern.findall(data)
        for i in all:
            data = data.replace(i, "")
        words = pseg.cut(data, HMM = True)
        fenci_list = []
        words_list = []
        filter_flag = ['ns', 'nt', 'nz', 'nr', 'l', 's', 'f', 't']
        for w in words:
            if w.word not in self.stop_word and w.flag not in filter_flag:
                fenci_list.append([w.word, w.flag])
        for i in range(len(fenci_list)):
            words_list.append(fenci_list[i][0])
            if i < len(fenci_list) - 1:
                words_list.append(fenci_list[i][0] + fenci_list[i + 1][0])

            if fenci_list[i][1] == 'v' or fenci_list[i][1] == 'vn' or fenci_list[i][1] == 'm':
                for j in range(1, 3):
                    try:
                        if fenci_list[i + j][1] == 'n':
                            words_list.append(fenci_list[i][0] + fenci_list[i + j][0])
                        if fenci_list[i][1] == 'v' and fenci_list[i + j][1] == 'r':
                            words_list.append(fenci_list[i][0] + fenci_list[i + j][0])
                    except:
                        break
            if fenci_list[i][1] == 'p':
                for j in range(1, 3):
                    try:
                        if fenci_list[i + j][1] == 'v':
                            words_list.append(fenci_list[i][0] + fenci_list[i + j][0])
                    except:
                        break
        if len(words_list) == 0:
            return np.nan
        else:
            return words_list

    def set_label_drop_na(self, data):
        data['案件类别'] = data['案件类别'].apply(lambda x: self.label_dict[x])
        data = data.dropna(axis = 0, how = 'any').reset_index().drop(['index'], axis=1)
        return data

    def filter_data(self):
        '''
            This function removes the minority classes from training data
        '''
        training = pd.DataFrame()
        for l in self.l1 + self.l2 + self.l3:
            training = pd.concat([training, self.data[self.data['案件类别'] == l]])
        self.data = training
        return self.data

    def merge_class(self, data):
        '''
            This function merges some classes
        '''
        data.loc[data['案件类别'] == self.label_dict['日常生活求助'], '案件类别'] = self.label_dict['其他群众求助']
        data.loc[data['案件类别'] == self.label_dict['其他类型'], '案件类别'] = self.label_dict['其他群众求助']
        data.loc[data['案件类别'] == self.label_dict['其他交通事故'], '案件类别'] = self.label_dict['道路交通事故']
        data.loc[data['案件类别'] == self.label_dict['非道路交通事故'], '案件类别'] = self.label_dict['道路交通事故']
        return data

    def pre_process(self):
        self.data = self.read_data()
        self.stop_word = self.read_stop_words()
        if self.flag == 'test':
            self.data = self.participial(self.data)
            return
        else:
            self.data['报警内容'] = self.data['报警内容'].apply(self.participial)
            self.label_dict = self.get_label_dict(self.data)
            self.data = self.set_label_drop_na(self.data)

            self.l1 = [self.label_dict['道路交通事故'], self.label_dict['其他交通事故'], self.label_dict['非道路交通事故']]
            self.l2 = [self.label_dict['其他群众求助'], self.label_dict['其他纠纷'], self.label_dict['盗窃'], self.label_dict['殴打他人'], \
                       self.label_dict['物品失窃'], self.label_dict['日常生活求助'], self.label_dict['其他类型']]
            self.l3 = [self.label_dict['民事纠纷'], self.label_dict['诈骗'], self.label_dict['其他火灾'], self.label_dict['举报线索'], \
                       self.label_dict['侵犯人身权利'], self.label_dict['经济纠纷'], self.label_dict['扰乱公共秩序'], self.label_dict['人员失踪'],\
                       self.label_dict['损毁公私财物'], self.label_dict['威胁恐吓'], self.label_dict['抢劫'], self.label_dict['社会救助'], \
                       self.label_dict['强制消费'], self.label_dict['卫生求助'], self.label_dict['生产劳动']]

            self.data = self.filter_data()
            self.data = self.merge_class(self.data)
