from collections import Counter

from django.test import TestCase
import jieba

# Create your tests here.
from scipy import linalg, mat

from main.models import alarm
from main.unsupervised.jieba_cluster import kMeans, gen_sim, randCent
from main.utils.sql_helper import select_alarm

# 停用词表
# 创建停用词list
from main.utils.list_to_txt import list_to_txt

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

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

keyword_top150 = Counter(keyword_array).most_common(150)
keyword_list = []
for item in keyword_top150:
    keyword_list.append(str(item).split('\'')[1])

height = len(keyword_list)
width = len(content_list)

# 构建二维数组
keyword_matrix = [[0 for col in range(width + 1)] for row in range(height + 1)]

keyword_matrix[0][0] = "alarm_id"

# 第一行放入关键词
i = 1
for item in keyword_list:
    if len(item) > 1:
        keyword_matrix[i][0] = item
        i += 1

# 第一列填写news id
i = 1
for item in alarm_list:
    keyword_matrix[0][i] = item
    i += 1

# 构建矩阵
for i in range(height):
    if i == 0:
        continue
    key = keyword_matrix[i][0]
    for n in range(width):
        if n == 0 or keyword_matrix[0][n] == 0:
            continue
        print(keyword_matrix[0][n], n)
        count = keyword_matrix[0][n].content.count(key)
        keyword_matrix[i][n] = count

# 写入到txt文件
list_to_txt(keyword_matrix,'keywords')
print("build keyword_matrix successful")

# 去除第一行和第一列
result = [[0 for col in range(width)] for row in range(height)]
for i in range(height-1):
    if i == 0:
        continue
    for n in range(width-1):
        if n == 0:
            continue
        result[i-1][n-1] = keyword_matrix[i][n]

myCentroids, clustAssing = kMeans(result, 3, gen_sim, randCent)
print("kMeans successful,clustAssing length:", len(clustAssing))
for label, name in zip(clustAssing[:, 0], "2"):
    print(label, name)

# 奇异值分解
u, sigma, vt = linalg.svd(result)

print(sigma)

# 简化矩阵
sig3 = mat([[sigma[0], 0, 0],
            [0, sigma[1], 0],
            [0, 0, sigma[2]]])

u3 = u[:, :3]

# 保存文件
#list_to_txt(sigma,'sigma')
list_to_txt(u,'u')
list_to_txt(vt,'vt')
list_to_txt(u3,'u3')

print("build svd successful")