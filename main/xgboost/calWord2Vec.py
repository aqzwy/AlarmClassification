from __future__ import division
from collections import Counter
from collections import OrderedDict
import numpy as np
import pandas as pd
import math
import gensim
import pickle

class calWord2Vec():
    def __init__(self, save_url, training_data, label_dict, config):
        self.training_data = training_data
        self.save_url = save_url
        self.label_dict = label_dict
        self.config = config

        self.training_vector = []
        self.word_vector = {}
        self.training_label = []
        self.weight_dict = {}
        self.label_trans_dict = {}

        self.pre_train()

    def get_weight(self, data, target_label_list):
        '''
            This functions calculates weight for every word in training data
            Using P(w|t)/(1 - P(w|t))
        '''
        count_dict = {}
        content = data['报警内容'].values
        label = data['案件类别'].values
        label_count = Counter(label)

        for i in range(len(target_label_list)):
            if i not in label_count.keys():
                label_count[i] = 0

        label_count = OrderedDict(sorted(label_count.items(), key = lambda x: x[0]))
        label_count = list(label_count.values())

        for i in range(len(content)):
            word_set = set()
            index = label[i]
            content[i] = list(set(content[i]))
            for word in content[i]:
                if word not in count_dict.keys():
                    count_dict[word] = np.array([0] * len(target_label_list))
                if word not in word_set:
                    count_dict[word][index] += 1
                word_set.add(word)

        for word, count in count_dict.items():
            tmp_weight_list = np.zeros(len(count))
            for i in range(len(count)):
                if count[i] == 0 and label_count[i] == 0:
                    tmp_weight_list[i] = 0
                    continue
                else:
                    n_wl = count[i] + 1
                    n_l = label_count[i] + 1
                    tmp_weight_list[i] = math.log((n_wl / n_l) / (1 - n_wl / n_l))
            self.weight_dict[word] = tmp_weight_list

        self.weight_dict = list(
            zip(self.weight_dict.keys(), list(map(lambda x: np.max(x) - np.min(x), self.weight_dict.values()))))
        return dict(self.weight_dict)

    def cal_vector(self, sentences, size):
        '''
            This function smoothies the weight and turn a sentence into a vector
        '''
        vector = []
        for s in sentences:
            final_vector = np.array([0.0] * size)
            dis_dict = {}
            for i in range(len(s)):
                if s[i] not in self.weight_dict.keys():
                    continue
                dis_dict[s[i]] = self.weight_dict[s[i]]
            for word in s:
                if word in dis_dict.keys():
                    final_vector += self.word_vector[word] * dis_dict[word]
            vector.append(final_vector)
        return vector

    def get_train_vector(self, training, min_count, size):
        '''
            This function turns training data into vector
        '''
        sentences = training['报警内容'].values.tolist()
        model = gensim.models.Word2Vec(sentences, sg=1, min_count=min_count, size=size)
        self.word_vector = dict(zip(model.wv.index2word, model.wv.syn0))

        self.training_vector = self.cal_vector(sentences, size)
        self.training_label = training['案件类别'].values.copy()

        return self.training_vector, self.training_label, self.word_vector

    def pre_train(self):
        """
            Calculate word vector, word weight and utilize them to calculate text vector.
            Save all intermediate result, which will be used in prediction stage, into disk.
        """
        level = self.config[0]
        label = self.config[1]
        min_count = self.config[2]
        size = self.config[3]

        training = self.training_data.copy()

        if level <= 2:
            self.label_trans_dict = {0: 0, 1: 1}
            if level == 2:
                training = training.loc[training['案件类别'] != (self.label_dict['道路交通事故'])]
            for i in range(len(label)):
                training.loc[training['案件类别'] == label[i], '案件类别'] = 0
            training.loc[training['案件类别'] != 0, '案件类别'] = 1
            self.training_label = training['案件类别'].values
            label = [0, 1]
        else:
            training = pd.DataFrame()
            self.label_trans_dict = {}
            for i in range(len(label)):
                self.label_trans_dict[label[i]] = i
                t = self.training_data.loc[self.training_data['案件类别'] == label[i]]
                t['案件类别'] = i
                training = pd.concat([training, t])
            self.label_trans_dict = {value: key for key, value in self.label_trans_dict.items()}

        self.weight_dict = self.get_weight(training, range(len(label)))
        self.training_vector, self.training_label, self.word_vector = self.get_train_vector(training, min_count, size)

        with open(self.save_url + '\weight_dict.pickle', 'wb') as f:
            f.truncate()
            pickle.dump(self.weight_dict, f)
        with open(self.save_url+ '\word_vector.pickle', 'wb') as f:
            f.truncate()
            pickle.dump(self.word_vector, f)
        with open(self.save_url+ '\label_trans_dict.pickle', 'wb') as f:
            f.truncate()
            pickle.dump(self.label_trans_dict, f)