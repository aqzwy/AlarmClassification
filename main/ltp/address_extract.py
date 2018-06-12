import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

from main.models.Singleton import Singleton

class address_extract_model(Singleton):
    print('load ltp model start...')

    pwd = os.getcwd()
    project_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

    LTP_DATA_DIR = project_path + '\AlarmClassification\main\ltp\model'  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`

    print('path' + cws_model_path)

    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型

    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型


    def get_model(self):
        return self.segmentor, self.postagger, self.recognizer


def get_address_prediction(alarm_content):
    model = address_extract_model()
    segmentor, postagger, recognizer = model.get_model()

    words = segmentor.segment(alarm_content)  # 分词
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别

    result = ''
    for i in range(0, len(netags)):
        print(words[i] + ': ' + netags[i])
        if 's' in netags[i]:
            result += words[i] + ','
    if len(result) < 1:
        result = 'No address!'
    print(result)
    return result


def get_address(alarm_content):
    print("start get_address...")
    result = "Exception"
    try:
        result = get_address_prediction(alarm_content)
    except Exception as ex:
        print(ex)

    print("Output is " + result)
    return result

# segmentor.release()  # 释放模型
# postagger.release()
# recognizer.release()