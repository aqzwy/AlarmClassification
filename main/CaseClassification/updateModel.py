from __future__ import division
from CaseClassification.dataProcess import dataProcess
from CaseClassification.calWord2Vec import calWord2Vec
from CaseClassification.train_model import train_model
from CaseClassification.modelParams import modelParams
import xgboost as xgb
import warnings
import os
warnings.filterwarnings('ignore')

def pre_process():
    # preprocess data
    dataPro = dataProcess(r'C:\Users\f30073\Desktop\caseanalysis\data.xlsx',
                          r'C:\Users\f30073\Desktop\caseanalysis\param',
                          r'C:\Users\f30073\Desktop\caseanalysis\Chinese-master\dict\stopwords.txt',
                          'train')

    dataPro.l1.remove(dataPro.label_dict['其他交通事故'])
    dataPro.l1.remove(dataPro.label_dict['非道路交通事故'])
    dataPro.l2.remove(dataPro.label_dict['日常生活求助'])
    dataPro.l2.remove(dataPro.label_dict['其他类型'])
    dataPro.delete_list = ['其他交通事故', '非道路交通事故', '日常生活求助', '其他类型']

    config = modelParams(dataPro.l1, dataPro.l2, dataPro.l3)

    return dataPro, config

def get_vector(dataPro, config, param_path):
    # get word vector and text vector
    word2Vec_1 = calWord2Vec(param_path + '\param1', dataPro.data, dataPro.label_dict, config.model_1_params['pre_train'])
    word2Vec_2 = calWord2Vec(param_path + '\param2', dataPro.data, dataPro.label_dict, config.model_2_params['pre_train'])
    word2Vec_31 = calWord2Vec(param_path + '\param3', dataPro.data, dataPro.label_dict, config.model_31_params['pre_train'])
    word2Vec_32 = calWord2Vec(param_path + '\param4', dataPro.data, dataPro.label_dict, config.model_32_params['pre_train'])

    return [word2Vec_1, word2Vec_2, word2Vec_31, word2Vec_32]

def initialize_model(config):
    # initialize 4 models
    model_1 = xgb.XGBClassifier(max_depth=config.model_1_params['xgb']['max_depth'],
                                learning_rate=config.model_1_params['xgb']['learning_rate'],
                                n_estimators=config.model_1_params['xgb']['n_estimators'],
                                objective=config.model_1_params['xgb']['objective']
                                )
    model_2 = xgb.XGBClassifier(max_depth=config.model_2_params['xgb']['max_depth'],
                                learning_rate=config.model_2_params['xgb']['learning_rate'],
                                n_estimators=config.model_2_params['xgb']['n_estimators'],
                                objective=config.model_2_params['xgb']['objective']
                                )
    model_31 = xgb.XGBClassifier(max_depth=config.model_31_params['xgb']['max_depth'],
                                 learning_rate=config.model_31_params['xgb']['learning_rate'],
                                 n_estimators=config.model_31_params['xgb']['n_estimators'],
                                 objective=config.model_31_params['xgb']['objective']
                                 )
    model_32 = xgb.XGBClassifier(max_depth=config.model_32_params['xgb']['max_depth'],
                                 learning_rate=config.model_32_params['xgb']['learning_rate'],
                                 n_estimators=config.model_32_params['xgb']['n_estimators'],
                                 objective=config.model_32_params['xgb']['objective']
                                 )

    return [model_1, model_2, model_31, model_32]

def get_model(word2Vec_list, model_list, config, param_path):
    # train xgboost and cross validation
    train_model_1 = train_model(param_path + r'\xgb1.model', word2Vec_list[0].training_vector, word2Vec_list[0].training_label, model_list[0], \
                                config.model_1_params['xgb_cv'], 'binary', 'False')
    print("Done training 1st model!")
    train_model_2 = train_model(param_path + r'\xgb2.model', word2Vec_list[1].training_vector, word2Vec_list[1].training_label, model_list[1], \
                                config.model_2_params['xgb_cv'], 'binary', 'True')
    print("Done training 2nd model!")
    train_model_31 = train_model(param_path + r'\xgb3.model', word2Vec_list[2].training_vector, word2Vec_list[2].training_label, model_list[2], \
                                 config.model_31_params['xgb_cv'], 'multi', 'False')
    print("Done training 3rd model!")
    train_model_32 = train_model(param_path + r'\xgb4.model', word2Vec_list[3].training_vector, word2Vec_list[3].training_label, model_list[3], \
                                 config.model_32_params['xgb_cv'], 'multi', 'False')
    print("Done training 4th model!")

    return train_model_1, train_model_2, train_model_31, train_model_32

def update_model(param_path):
    for i in range(1, 5):
        os.makedirs(param_path + '\param' + str(i))
    dataPro, config = pre_process()
    print("Done preprocess data!")

    word2Vec_list = get_vector(dataPro, config, param_path)
    print("Get all training vectors!")

    model_list = initialize_model(config)
    get_model(word2Vec_list, model_list, config, param_path)
    print("Done training all four models!")

if __name__ == '__main__':
    update_model(r'C:\Users\f30073\Desktop\caseanalysis\param')

