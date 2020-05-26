"""
    作者：大发
    时间：2019/12/20
    功能：统计画图，p382
"""

import pandas as pd
import numpy as np
import patsy
from io import StringIO
from lxml import objectify
import requests
import sqlite3
import sqlalchemy as sqla
from io import StringIO
import json
from numpy import nan as NA
import re
import matplotlib.pyplot as plt
from numpy.random import randn
from datetime import datetime
from io import BytesIO
import seaborn as sns
import statsmodels.api as sm
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour,Minute
from pandas.tseries.offsets import Day,MonthEnd
from scipy.stats import percentileofscore

path = 'D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\_bitly_usagov\example.txt'
# open(path).readline()
# Out[11]: '{ "a": "Mozilla\\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\\/535.11 (KHTML, like Gecko) Chrome\\/17.0.963.78 Safari\\/535.11", "c": "US", "nk": 1, "tz": "America\\/New_York", "gr": "MA", "g": "A6qOVH", "h": "wfLQtf", "l": "orofrog", "al": "en-US,en;q=0.8", "hh": "1.usa.gov", "r": "http:\\/\\/www.facebook.com\\/l\\/7AQEFzjSi\\/1.usa.gov\\/wfLQtf", "u": "http:\\/\\/www.ncbi.nlm.nih.gov\\/pubmed\\/22415991", "t": 1331923247, "hc": 1331822918, "cy": "Danvers", "ll": [ 42.576698, -70.954903 ] }\n'
# 上边拿到的是JSON数据，python中有内置库将JSON字符串转换成Python字典对象。
# 接下来使用JSON模块，及其loads函数逐行加载已经下载好的数据文件：

# records = [json.loads(line) for line in open(path)]
# records[0]
# Out[17]:
# {'a': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.78 Safari/535.11',
#  'c': 'US',
#  'nk': 1,
#  'tz': 'America/New_York',
#  'gr': 'MA',
#  'g': 'A6qOVH',
#  'h': 'wfLQtf',
#  'l': 'orofrog',
#  'al': 'en-US,en;q=0.8',
#  'hh': '1.usa.gov',
#  'r': 'http://www.facebook.com/l/7AQEFzjSi/1.usa.gov/wfLQtf',
#  'u': 'http://www.ncbi.nlm.nih.gov/pubmed/22415991',
#  't': 1331923247,
#  'hc': 1331822918,
#  'cy': 'Danvers',
#  'll': [42.576698, -70.954903]}

### 14.1.1 用纯Python代码对时区进行计数

## 假设我们想要知道该数据集中最常出现的是哪个时区（即tz字段），
## 得到答案的办法有很多。首先，我们用列表推导式取出一组时区：

# time_zones = [rec['tz'] for rec in records]

# Traceback (most recent call last):
#   File "C:\ProgramData\Anaconda3\lib\site-packages\IPython\core\interactiveshell.py", line 3325, in run_code
#     exec(code_obj, self.user_global_ns, self.user_ns)
#   File "<ipython-input-18-f3fbbc37f129>", line 1, in <module>
#     time_zones = [rec['tz'] for rec in records]
#   File "<ipython-input-18-f3fbbc37f129>", line 1, in <listcomp>
#     time_zones = [rec['tz'] for rec in records]
# KeyError: 'tz'
# 以上的这个错误表明，不是所有记录都有时区字段，需要在列表推导式末尾加上 if 'tz' in rec

# time_zones = [rec['tz'] for rec in records if 'tz' in rec]
# time_zones[:10]
# Out[20]:
# ['America/New_York',
#  'America/Denver',
#  'America/New_York',
#  'America/Sao_Paulo',
#  'America/New_York',
#  'America/New_York',
#  'Europe/Warsaw',
#  '',
#  '',
#  '']

## 只看这前十个时区，会发现有些是未知的，空的。可以过滤掉，但先留着。
## 接下来对时区进行计数，一种方法只使用Python库，一种方法用pandas
## 计数的办法之一是在遍历时区的过程中将计数值保存在字典中：

# # 方法1
# def get_counts(sequence):
#     counts = {}
#     for x in sequence:
#         if x in counts:
#             counts[x] += 1
#         else :
#             counts[x] = 1
#     return counts
#
# ## 方法2
# from collections import defaultdict
#
# def get_counts2(sequence) :
#     counts = defaultdict(int) # 值将会初始化为0
#     for x in sequence:
#         counts[x] += 1           # 塑造了一个字典，给字典的key加值
#     return counts
#
# counts = get_counts(time_zones)
# counts['America/New_York']
# Out[26]: 1251

# len(time_zones)
# Out[27]: 3440

## 如果想要得到前十位的时区及其计数值，需要用到一些有关字典的处理技巧：

# def top_counts(count_dict , n=10):
#     value_key_pairs = [(count , tz) for tz , count in count_dict.items()]
#     value_key_pairs.sort()     # .sort()正序，从小到大
#     return  value_key_pairs[-n:]
# top_counts(counts)
# Out[29]:
# [(33, 'America/Sao_Paulo'),
#  (35, 'Europe/Madrid'),
#  (36, 'Pacific/Honolulu'),
#  (37, 'Asia/Tokyo'),
#  (74, 'Europe/London'),
#  (191, 'America/Denver'),
#  (382, 'America/Los_Angeles'),
#  (400, 'America/Chicago'),
#  (521, ''),
#  (1251, 'America/New_York')]

## 这项工作用collections.Counter类，更简单：

# from collections import Counter
#
# counts = Counter(time_zones)
# counts.most_common(10)            ## .most_common()取最前10
# Out[32]:
# [('America/New_York', 1251),
#  ('', 521),
#  ('America/Chicago', 400),
#  ('America/Los_Angeles', 382),
#  ('America/Denver', 191),
#  ('Europe/London', 74),
#  ('Asia/Tokyo', 37),
#  ('Pacific/Honolulu', 36),
#  ('Europe/Madrid', 35),
#  ('America/Sao_Paulo', 33)]

##### 14.1.2 使用pandas进行时区计数
## 从原始记录的集合创建DateFrame，与将记录列表传递到pandas.DataFrame一样简单：

# frame = pd.DataFrame(records)     # 直接把records导成了DataFrame数据
# frame.info()         # .info()  是information的意思，显示frame的具体信息。
#
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3560 entries, 0 to 3559
# Data columns (total 18 columns):
# _heartbeat_    120 non-null float64
# a              3440 non-null object
# al             3094 non-null object
# c              2919 non-null object
# cy             2919 non-null object
# g              3440 non-null object
# gr             2919 non-null object
# h              3440 non-null object
# hc             3440 non-null float64
# hh             3440 non-null object
# kw             93 non-null object
# l              3440 non-null object
# ll             2919 non-null object
# nk             3440 non-null float64
# r              3440 non-null object
# t              3440 non-null float64
# tz             3440 non-null object
# u              3440 non-null object
# dtypes: float64(4), object(14)
# memory usage: 500.7+ KB

# frame['tz'][:10]
# Out[34]:
# 0     America/New_York
# 1       America/Denver
# 2     America/New_York
# 3    America/Sao_Paulo
# 4     America/New_York
# 5     America/New_York
# 6        Europe/Warsaw
# 7
# 8
# 9
# Name: tz, dtype: object

## 这里fframe的输出形式是摘要视图，主要用于较大的DataFrame对象。
## 对Series使用value_counts方法：

# tz_counts = frame['tz'].value_counts()   # .value)counts()用来分类计数，pandas简洁方便
# tz_counts[:10]
# Out[36]:
# America/New_York       1251
#                         521
# America/Chicago         400
# America/Los_Angeles     382
# America/Denver          191
# Europe/London            74
# Asia/Tokyo               37
# Pacific/Honolulu         36
# Europe/Madrid            35
# America/Sao_Paulo        33
# Name: tz, dtype: int64

## 以上这个数据可以用matplotllib可视化这个数据。
## 先要给记录中未知或缺失的时区填上一个替代值。
## fillna可以替换缺失值（NA），未知值（空字符串）则可以通过布尔型数组索引加以替换：

# clean_tz = frame['tz'].fillna('Missing')     # 清洗tz中的NA，替换成Missing
# clean_tz[clean_tz  == ''] = 'Unknow'      # 把空值换成Unknown
# tz_counts = clean_tz.value_counts()
# tz_counts[:10]
# Out[38]:
# America/New_York       1251
# Unknow                  521           # 原数据的空值
# America/Chicago         400
# America/Los_Angeles     382
# America/Denver          191
# Missing                 120            # 原数据中的NA
# Europe/London            74
# Asia/Tokyo               37
# Pacific/Honolulu         36
# Europe/Madrid            35
# Name: tz, dtype: int64

## 可以用seaborn包创建水平柱状图

# subset = tz_counts[:10]
# sns.barplot(y=subset.index , x=subset.values)    # 画图，y轴为分类名，x轴做数值轴
# Out[41]: <matplotlib.axes._subplots.AxesSubplot at 0x288bb0d1358>

# a字段含有执行URL短缩操作的浏览器、设备、应用程序的相关信息：
# frame['a'][1]
# Out[43]: 'GoogleMaps/RochesterNY'
# frame['a'][50]
# Out[44]: 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'
# frame['a'][51][:50]
# Out[45]: 'Mozilla/5.0 (Linux; U; Android 2.2.2; en-us; LG-P9'

# 将这些"agent"字符串中的所有信息都解析出来是一件挺郁闷的工作。
# 一种策略是将这种字符串的第一节（与浏览器大致对应）分离出来并得到另外一份用户行为摘要：

# results = pd.Series([x.split()[0] for x in frame.a.dropna()])
# # .split 是切片， .dropna()是删除空缺值
# In[47]: results[:5]
# Out[47]:
# 0               Mozilla/5.0
# 1    GoogleMaps/RochesterNY
# 2               Mozilla/4.0
# 3               Mozilla/5.0
# 4               Mozilla/5.0
# dtype: object

# In[48]: results.value_counts()[:8]
# Out[48]:
# Mozilla/5.0                 2594
# Mozilla/4.0                  601
# GoogleMaps/RochesterNY       121
# Opera/9.80                    34
# TEST_INTERNET_AGENT           24
# GoogleProducer                21
# Mozilla/6.0                    5
# BlackBerry8520/5.0.0.681       4
# dtype: int64

# 假设你想按Windows和非Windows用户对时区统计信息进行分解。
# 为了简单起见，我们假定只要agent字符串中含有"Windows"就认为该用户为
# Windows用户。由于有的agent缺失，所以首先将它们从数据中移除：

# frame.a.notnull()是一个布尔值判断是否为空值，不是空值返回True
# cframe = frame [frame.a.notnull()]        # 只取不为空值的数据
#
# #  np.where(condition, x, y)  返回一个n维数组，可以广播的
# #  .str.contains一个筛选的方法
# cframe['os'] = np.where(cframe['a'].str.contains('Windows'),'Windows' , 'Not Windows')
# # 试图在DataFrame的切片副本上设置一个值。
# # 尝试改用.loc [row_indexer，col_indexer] = value
#
# cframe['os'][:5]
# Out[66]:
# 0        Windows
# 1    Not Windows
# 2        Windows
# 3    Not Windows
# 4        Windows
# Name: os, dtype: object

## 接下来就可以根据时区和新得到的操作系统列表对数据进行分组了：
# by_tz_os = cframe.groupby(['tz' , 'os'])            # 取出两列
# 分组计数，类似于value_counts函数，可以用size来计算。
# 并利用unstack对计数结果进行重塑：
# 在用pandas进行数据重排，stack的意思是堆叠，堆积，unstack即“不要堆叠”
# 'Series' object has no attribute 'stack'
# agg_counts = by_tz_os.size().unstack().fillna(0)
# agg_counts[:10]
# Out[71]:
# os                              Not Windows  Windows
# tz
#                                       245.0    276.0
# Africa/Cairo                            0.0      3.0
# Africa/Casablanca                       0.0      1.0
# Africa/Ceuta                            0.0      2.0
# Africa/Johannesburg                     0.0      1.0
# Africa/Lusaka                           0.0      1.0
# America/Anchorage                       4.0      1.0
# America/Argentina/Buenos_Aires          1.0      0.0
# America/Argentina/Cordoba               0.0      1.0
# America/Argentina/Mendoza               0.0      1.0

## 选取最常出现的时区。为了达到这个目的，
# 我根据agg_counts中的行数构造了一个间接索引数组：

# 用于按升序排序
# argsort()函数是将x中的元素从小到大排列，提取其对应的index(索引)，然后输出到y
# indexer = agg_counts.sum(1).argsort()        # sum(1)表示列相加，sum()是行相加
# indexer[:10]
# Out[80]:
# tz
#                                   24
# Africa/Cairo                      20
# Africa/Casablanca                 21
# Africa/Ceuta                      92
# Africa/Johannesburg               87
# Africa/Lusaka                     53
# America/Anchorage                 54
# America/Argentina/Buenos_Aires    57
# America/Argentina/Cordoba         26
# America/Argentina/Mendoza         55
# dtype: int64
# 通过take按照这个顺序截取了最后10行最大值：

# count_subset = agg_counts.take(indexer[-10:])
# count_subset
# Out[82]:
# os                   Not Windows  Windows
# tz
# America/Sao_Paulo           13.0     20.0
# Europe/Madrid               16.0     19.0
# Pacific/Honolulu             0.0     36.0
# Asia/Tokyo                   2.0     35.0
# Europe/London               43.0     31.0
# America/Denver             132.0     59.0
# America/Los_Angeles        130.0    252.0
# America/Chicago            115.0    285.0
#                            245.0    276.0
# America/New_York           339.0    912.0

# pandas有一个简便方法nlargest，可以做同样的工作：
# agg_counts.sum(1).nlargest(10)
#
# agg_counts.sum(1).nlargest(10)
# Out[83]:
# tz
# America/New_York       1251.0
#                         521.0
# America/Chicago         400.0
# America/Los_Angeles     382.0
# America/Denver          191.0
# Europe/London            74.0
# Asia/Tokyo               37.0
# Pacific/Honolulu         36.0
# Europe/Madrid            35.0
# America/Sao_Paulo        33.0
# dtype: float64

## 对绘图数据重排列
# count_subset = count_subset.stack()
# count_subset.name = 'total'
# count_subset = count_subset.reset_index()
# count_subset[:10]
# Out[84]:
#                   tz           os  total
# 0  America/Sao_Paulo  Not Windows   13.0
# 1  America/Sao_Paulo      Windows   20.0
# 2      Europe/Madrid  Not Windows   16.0
# 3      Europe/Madrid      Windows   19.0
# 4   Pacific/Honolulu  Not Windows    0.0
# 5   Pacific/Honolulu      Windows   36.0
# 6         Asia/Tokyo  Not Windows    2.0
# 7         Asia/Tokyo      Windows   35.0
# 8      Europe/London  Not Windows   43.0
# 9      Europe/London      Windows   31.0
## hue=
# sns.barplot(x='total' , y='tz' , hue='os' , data=count_subset)

# 这张图不容易看出Windows用户在小分组中的相对比例，因此标准化分组百分比之和为1：

# def norm_total(group):
#     group['normed_total'] = group.total / group.total.sum()
#     return group
#
# results = count_subset.groupby('tz').apply(norm_total)
# sns.barplot(x='normed_total' , y='tz' , hue='os' , data=results)
# 还可以用groupby的transform方法，更高效的计算标准化的和：
# g = count_subset.groupby('tz')
# results2 = count_subset.total / g.total.transform('sum')