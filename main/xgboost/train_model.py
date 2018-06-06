from __future__ import division
import numpy as np
import xgboost as xgb
import random
from sklearn.neighbors import NearestNeighbors
from collections import Counter

class train_model():
    def __init__(self, model_url, training_vector, training_label, model, params, task, over_sample):
        self.training_vector = training_vector
        self.training_label = training_label
        self.model = model
        self.model_url = model_url
        self.params = params
        self.task = task
        self.over_sample = over_sample

        self.cross_validation()
        self.train_model()

    def over_sampling(self, data, data_label, minority_label, N, k):
        synthetic = data
        data_label = list(data_label)
        neighbors = NearestNeighbors(n_neighbors = k).fit(data)

        for i in range(len(data)):
            if data_label[i] == minority_label:
                index = neighbors.kneighbors(np.array(data[i]).reshape(1, -1), return_distance = False)[0]
                count = 0
                for j in index:
                    if data_label[j] == minority_label:
                        count += 1
                if count < k / 2 and count > 0:
                    synthetic, data_label = self.populate(synthetic, data, data_label, minority_label, N, i, k, index)
        return synthetic, data_label

    # data[i] has k nearest neighbors, their index are stored in index. We need to sample N data from these neighbors
    def populate(self, synthetic, data, data_label, minority_label, N, i, k, index):
        for j in range(N):
            nn = random.randint(0, k - 1)
            dif = data[index[nn]] - data[i]
            gap = random.random()
            synthetic.append(data[i] + gap * dif)
            data_label.append(minority_label)
        return synthetic, data_label

    def cross_validation(self):
        xgb_param = self.model.get_xgb_params()
        if self.task == 'multi':
            xgb_param['num_class'] = len(Counter(self.training_label))
        xgtrain = xgb.DMatrix(self.training_vector, self.training_label)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round = self.model.get_params()['n_estimators'],
                            nfold = self.params[0], metrics = self.params[1], early_stopping_rounds = self.params[2])
        self.model.set_params(n_estimators = cvresult.shape[0])

        return self.model

    def train_model(self):
        if self.over_sample == 'True':
            self.training_vector, self.training_label = self.over_sampling(self.training_vector, self.training_label, 1, 1, 10)

        self.model.fit(np.array(self.training_vector), self.training_label)
        self.model.get_booster().save_model(self.model_url)
        return self.model