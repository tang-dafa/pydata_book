"""
    插

"""

import pandas as pd


infomation = pd.read_excel('D:\\data_py\\pydata_book\\_names_member\\info_data\\广西调研员报名表.xlsx')

# In[4]: infomation['学院'].value_counts()
# Out[4]:
# 旅地学院         177
# 经济与管理学院       50
# 旅游与地理科学学院     34
# 史政学院          32
# 哲政学院          25
# 历史与行政学院       24
# 哲学与政法学院       22
# 经管学院          21
# 教育学部          12
# 物理与电子信息学院     10
# 物电学院           7
# 体育学院           6
# 信息学院           5
# 外国语学院          5
# 传媒学院           5
# 文学院            4
# 教管学院           4
# 汉藏语研究院         3
# 美术学院           2
# 化学化工学院         2
# 马克思主义学院        2
# 音舞学院           2
# 国际汉语教育学院       1
# \n汉藏语研究院       1
# 旅游与地理科学        1
# 经济管理学院         1
# 历史与行政          1
# 数学学院           1
# 泛亚商学院          1
# 经济与管理学院学院      1
# 旅地学校           1
# 生命科学学院         1
# 化工学院           1
# 旅游与地理学学院       1
# Name: 学院, dtype: int64

list = infomation['学院']

file = infomation.reindex(list)

edu_name = infomation[infomation['academy'] == '教育学部']
edu_names = infomation[infomation['academy'] == '教管学院']

edu_mem = edu_name.append(edu_names)

edu_mem.to_excel('D:\\data_py\\pydata_book\\_names_member\\edu_mem.xlsx')










