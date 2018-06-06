import jieba

from main.tests_unsu import stopwordslist
from main.utils.sql_helper import select_alarm

keyword_array = []
content_list = []
alarm_list = select_alarm("殴打他人")
stopwords = stopwordslist('./data/stop_words.txt')
for item in alarm_list:
    cut = jieba.cut(item.content)
    for word in cut:
        if word not in stopwords and len(word) > 1:
            keyword_array.append(word)
            content_list.append(item.id)

for item in keyword_array:
    print(item)