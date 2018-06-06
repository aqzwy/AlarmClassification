import os
from pyltp import Postagger

LTP_DATA_DIR = '.\model'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`

from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型

words = ['元芳', '今天', '在', '深圳市']
postags = ['nh', 'r', 'ns', 'ns']
netags = recognizer.recognize(words, postags)  # 命名实体识别

print('\t'.join(netags))
recognizer.release()  # 释放模型