from __future__ import division

import os

import numpy as np
import xgboost as xgb
import jieba.posseg as pseg
import pickle
import time
import re

from main.models.Singleton import Singleton


def participial(data, stop_words):
    '''
        This function filters non-Chinese, stop words, numbers, punctuation and space
    '''
    data = re.sub(r'[^\u4e00-\u9fa5]', '', data)
    number = re.compile(u'([0-9]|[0-9]+[,]*[0-9]+.[0-9]+|[A-z])')
    pattern = re.compile(number)
    all = pattern.findall(data)
    for i in all:
        data = data.replace(i, "")
    words = pseg.cut(data, HMM=True)
    fenci_list = []
    words_list = []
    filter_flag = ['ns', 'nt', 'nz', 'nr', 'l', 's', 'f', 't']
    for w in words:
        if w.word not in stop_words and w.flag not in filter_flag:
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


def load_model(param_path):
    weight_list = []
    word_list = []
    model_list = []
    label_trans_list = []

    for i in range(1, 5):
        with open(param_path + '\param' + str(i) + r'\weight_dict.pickle', 'rb') as f:
            weight_list.append(pickle.load(f))
        with open(param_path + '\param' + str(i) + r'\word_vector.pickle', 'rb') as f:
            word_list.append(pickle.load(f))
        with open(param_path + '\param' + str(i) + r'\label_trans_dict.pickle', 'rb') as f:
            label_trans_list.append(pickle.load(f))
        # model_file cannot contains Chinese characters!
        model_list.append(xgb.Booster(model_file=param_path + r'\xgb' + str(i) + '.model'))
    with open(param_path + r'\label_dict.pickle', 'rb') as f:
        label_dict = pickle.load(f)

    return weight_list, word_list, model_list, label_trans_list, label_dict


def get_vector(weight_dict, word_vector, sentences, size):
    vector = np.array([0.0] * size)
    try:
        for word in sentences:
            if word not in weight_dict.keys():
                continue
            else:
                vector += word_vector[word] * weight_dict[word]
    except:
        print("All zeros!")
    return vector


def cal_duration(start):
    duration = time.time() - start
    print("It takes " + str(duration) + " seconds to finish predicting.")

# singleton para
class alarm_prediction_para_model(Singleton):
    print('Info:init singlton class alarm_prediction_para_model...')
    pwd = os.getcwd()
    project_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    param_path = project_path + '\AlarmClassification\main\param'
    stop_word_path = project_path + '\AlarmClassification\main\data\stopwords.txt'
    f = open(stop_word_path, encoding='gbk')
    stop_words = [line.strip() for line in f]
    weight_list, word_list, model_list, label_trans_list, label_dict = load_model(param_path)

    def stop_word(self):
        return self.stop_words

    def para(self):
        return self.weight_list, self.word_list, self.model_list, self.label_trans_list, self.label_dict



def get_individual_prediction(test_data):
    para = alarm_prediction_para_model()

    stop_words = para.stop_word()

    threshold_1 = 0.8
    threshold_2 = 0.8

    weight_list, word_list, model_list, label_trans_list, label_dict = para.para()

    test_case = participial(test_data, stop_words)

    test_vector_1 = get_vector(weight_list[0], word_list[0], test_case, 200)
    res_1 = model_list[0].predict(xgb.DMatrix(test_vector_1.reshape(1, -1)))[0]
    p1 = max(1 - res_1, res_1)
    if p1 <= threshold_1:
        res = "No results!"
        return res
    if res_1 < 0.5:
        res = "道路交通事故"
        return res

    test_vector_2 = get_vector(weight_list[1], word_list[1], test_case, 200)
    res_2 = model_list[1].predict(xgb.DMatrix(test_vector_2.reshape(1, -1)))[0]
    p2 = max(1 - res_2, res_2)
    if p2 <= threshold_1:
        res = "No results!"
        return res
    if res_2 < 0.5:
        test_vector_31 = get_vector(weight_list[2], word_list[2], test_case, 200)
        res_31 = model_list[2].predict(xgb.DMatrix(test_vector_31.reshape(1, -1)))[0]
        p31 = max(res_31)
        if p31 <= threshold_2:
            res = "No results!"
            return res
        res = str(label_dict[label_trans_list[2][res_31.tolist().index(max(res_31))]])
        return res
    else:
        test_vector_32 = get_vector(weight_list[3], word_list[3], test_case, 200)
        res_32 = model_list[3].predict(xgb.DMatrix(test_vector_32.reshape(1, -1)))[0]
        p32 = max(res_32)
        if p32 <= threshold_2:
            res = "No results!"
            return res
        res = str(label_dict[label_trans_list[3][res_32.tolist().index(max(res_32))]])
        return res


def predictionCase(caseContent):
    # param_path = r'../param'
    # stop_word_path =  r'../data/stopwords.txt'

    print("start prediction...")
    # start = time.time()
    result = "Exception"
    try:
        result = get_individual_prediction(caseContent)
    except Exception as ex:
        print(ex)
    # cal_duration(start)

    print("Output is " + result)
    return result


if __name__ == '__main__':
    predictionCase("我的钱包被偷了，请求帮助")
