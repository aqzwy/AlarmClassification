class modelParams():
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.size = 200
        self.min_count = 0
        self.early_stopping = 150


        self.model_1_params = {
            'pre_train': [1, self.l1, self.min_count, self.size],
            'xgb': {'max_depth': 4,
                    'learning_rate': 0.2,
                    'n_estimators': 100,
                    'objective': 'binary:logistic'},
            'xgb_cv': [3, 'auc', self.early_stopping]
        }

        self.model_2_params = {
            'pre_train': [2, self.l2, self.min_count, self.size],
            'xgb': {'max_depth': 4,
                    'learning_rate': 0.2,
                    'n_estimators': 100,
                    'objective': 'binary:logistic'},
            'xgb_cv': [3, 'auc', self.early_stopping]
        }

        self.model_31_params = {
            'pre_train': [3, self.l2, self.min_count, self.size],
            'xgb': {'max_depth': 4,
                    'learning_rate': 0.1,
                    'n_estimators': 100,
                    'objective': 'multi:softmax'},
            'xgb_cv': [3, 'mlogloss', self.early_stopping]
        }

        self.model_32_params = {
            'pre_train': [4, self.l3, self.min_count, self.size],
            'xgb': {'max_depth': 4,
                    'learning_rate': 0.2,
                    'n_estimators': 100,
                    'objective': 'multi:softmax'},
            'xgb_cv': [3, 'mlogloss', self.early_stopping]
        }