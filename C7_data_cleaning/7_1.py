"""

    作者：大发
    日期：2019/11/13
    内容：利用python进行数据分析 7.1 p188 笔记

"""

import pandas as pd
import numpy as np
from io import StringIO
from lxml import objectify
import requests
import sqlite3
import sqlalchemy as sqla
from io import StringIO
import json
from numpy import nan as NA

import re

# 7.1 处理缺失值

# string_data  = pd.Series(['aardvark' , 'artichoke' , np.nan , 'avocado'])
# string_data
# Out[50]:
# 0     aardvark
# 1    artichoke
# 2          NaN
# 3      avocado
# dtype: object
# string_data.isnull()
# Out[51]:
# 0    False
# 1    False
# 2     True
# 3    False
# dtype: bool
# string_data[0] = None
# string_data.isnull()
# Out[53]:
# 0     True
# 1    False
# 2     True
# 3    False
# dtype: bool
##  data.drona 用于过滤缺失值，返回所有非空数据和其索引
# data = pd.Series([1, NA , 3.5 , NA , 7])
# data.dropna()
# Out[56]:
# 0    1.0
# 2    3.5
# 4    7.0
# dtype: float64

# data[data.notnull()]   # 相同作用，过滤缺失值
# Out[57]:
# 0    1.0
# 2    3.5
# 4    7.0
# dtype: float64

##
# data = pd.DataFrame([[1. , 6.5 , 3.] , [1. , NA , NA] , [NA , NA , NA] , [NA , 6.5 , 3.]])
# cleaned = data.dropna()       # dropna 默认会删除包含缺失值的行
# data
# Out[60]:
#      0    1    2
# 0  1.0  6.5  3.0
# 1  1.0  NaN  NaN
# 2  NaN  NaN  NaN
# 3  NaN  6.5  3.0
# cleaned
# Out[61]:
#      0    1    2
# 0  1.0  6.5  3.0


# data.dropna(how = 'all')  # 这一行可以删除所有制均为NA的行
# Out[62]:
#      0    1    2
# 0  1.0  6.5  3.0
# 1  1.0  NaN  NaN
# 3  NaN  6.5  3.0

# data[4] = NA
# data
# Out[64]:
#      0    1    2   4
# 0  1.0  6.5  3.0 NaN
# 1  1.0  NaN  NaN NaN
# 2  NaN  NaN  NaN NaN
# 3  NaN  6.5  3.0 NaN
# data.dropna(axis = 1 , how = 'all')   # 传入参数axis=1 , 可以删除列中所有值为NA的
# Out[65]:
#      0    1    2
# 0  1.0  6.5  3.0
# 1  1.0  NaN  NaN
# 2  NaN  NaN  NaN
# 3  NaN  6.5  3.0


# df = pd.DataFrame(np.random.randn(7,3))
# df.iloc[:4 , 1] = NA
# df.iloc[:2 , 2] = NA
# df
# Out[69]:
#           0         1         2
# 0  1.226591       NaN       NaN
# 1  0.780342       NaN       NaN
# 2  0.485982       NaN -0.193329
# 3 -0.104485       NaN -0.963074
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688     # 生成一个矩阵
# df.dropna()                         # 删除所有有NA的行
# Out[70]:
#           0         1         2
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688
# df.dropna(thresh = 2)              # 每行的观察数量有2的保留，其他的删掉
# Out[71]:
#           0         1         2
# 2  0.485982       NaN -0.193329
# 3 -0.104485       NaN -0.963074
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688


# 7.1.2 补全缺失值 ， 用fillna补全

# df.fillna(0)                 # 使用常数0 补全缺失值
# Out[72]:
#           0         1         2
# 0  1.226591  0.000000  0.000000
# 1  0.780342  0.000000  0.000000
# 2  0.485982  0.000000 -0.193329
# 3 -0.104485  0.000000 -0.963074
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688
# df.fillna({1:0.5 , 2: 0 })      # 不同的列设置不同的填充值
# Out[73]:
#           0         1         2
# 0  1.226591  0.500000  0.000000
# 1  0.780342  0.500000  0.000000
# 2  0.485982  0.500000 -0.193329
# 3 -0.104485  0.500000 -0.963074
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688
# _ = df.fillna(0 , inplace = True)       # 修改已存在的对象
# df
# Out[75]:
#           0         1         2
# 0  1.226591  0.000000  0.000000
# 1  0.780342  0.000000  0.000000
# 2  0.485982  0.000000 -0.193329
# 3 -0.104485  0.000000 -0.963074
# 4  1.527058  0.117366  1.910239
# 5 -0.278958  0.553990  0.230248
# 6  2.297880  1.876769 -0.018688


# df = pd.DataFrame(np.random.randn(6,3))
# df.iloc[2: , 1] = NA
# df.iloc[4: , 2] = NA
# df
# Out[80]:
#           0         1         2
# 0 -0.454925 -0.912961 -0.541046
# 1  0.262247 -1.352699 -0.122755
# 2  1.388706       NaN -0.870880
# 3 -1.426940       NaN  1.461163
# 4 -0.579179       NaN       NaN
# 5 -0.618648       NaN       NaN


# df.fillna(method = 'ffill')            # 插值方法，默认ffill
# Out[81]:
#           0         1         2
# 0 -0.454925 -0.912961 -0.541046
# 1  0.262247 -1.352699 -0.122755
# 2  1.388706 -1.352699 -0.870880
# 3 -1.426940 -1.352699  1.461163
# 4 -0.579179 -1.352699  1.461163
# 5 -0.618648 -1.352699  1.461163
# df.fillna(method = 'ffill' , limit = 2)     # 用于向前或向后填充时最大的填充范围 ，这里是向下填充2个
# Out[82]:
#           0         1         2
# 0 -0.454925 -0.912961 -0.541046
# 1  0.262247 -1.352699 -0.122755
# 2  1.388706 -1.352699 -0.870880
# 3 -1.426940 -1.352699  1.461163
# 4 -0.579179       NaN  1.461163
# 5 -0.618648       NaN  1.461163
# data = pd.Series([1. , NA , 3.5 , NA , 7])
# data.fillna(data.mean())                        # 用平均值填充
# Out[84]:
# 0    1.000000
# 1    3.833333
# 2    3.500000
# 3    3.833333
# 4    7.000000
# dtype: float64

# fillna 的函数参数
# value：标量值或字典型对象用于填充缺失值
# method：查值方法
# axis：需要填充的轴 默认axis=0
# inplace：修改被调用的对象，而不是生成一个备份
# limit：用于向前或向后填充时最大的填充范围


## 7.2 数据转换


# 7.2.1 删除U重复值

# data = pd.DataFrame({'k1': ['one' , 'two']*3 + ['two'],'k2':[1,1,2,3,3,4,4]})
# data
# Out[89]:
#     k1  k2
# 0  one   1
# 1  two   1
# 2  one   2
# 3  two   3
# 4  one   3
# 5  two   4
# 6  two   4
# data.duplicated()  # 判断布尔值，反应每一行是否和前边的重复
# Out[90]:
# 0    False
# 1    False
# 2    False
# 3    False
# 4    False
# 5    False
# 6     True
# dtype: bool
# data.drop_duplicates()  # 返回一个dataframe,删除重复
# Out[91]:
#     k1  k2
# 0  one   1
# 1  two   1
# 2  one   2
# 3  two   3
# 4  one   3
# 5  two   4
# data['v1'] = range(7)
# data.drop_duplicates(['k1'])      # 基于k1列去除重复值
# Out[93]:
#     k1  k2  v1
# 0  one   1   0
# 1  two   1   1
# data.drop_duplicates(['k1', 'k2'] , keep = 'last')     # 使用keep = 'last'参数，会返回最后一个重复值
# Out[94]:
#     k1  k2  v1
# 0  one   1   0
# 1  two   1   1
# 2  one   2   2
# 3  two   3   3
# 4  one   3   4
# 6  two   4   6


# 7.2.2 使用函数或映射进行数据转换

# data = pd.DataFrame({'food':['bacon' , 'pulled pork' , 'bacon' ,
#                              'Pastrami' , 'corned beef' , 'Bacon' ,
#                              'pastrame' , 'honey ham' , 'nova lox'],
#                      'ounces':[4,3,12,6,7.5,8,3,5,6]})
#
# data
# Out[98]:
#           food  ounces
# 0        bacon     4.0
# 1  pulled pork     3.0
# 2        bacon    12.0
# 3     Pastrami     6.0
# 4  corned beef     7.5
# 5        Bacon     8.0
# 6     pastrame     3.0
# 7    honey ham     5.0
# 8     nova lox     6.0
#
# meat_to_animai = {                # 写出一个映射
#     'bacon': 'pig' ,
#     'pulled pork': 'pig' ,
#     'pastrami' : 'cow' ,
#     'corned beef' : 'cow' ,
#     'honey ham' : 'pig' ,
#     'nova lox' : 'salmo'
# }
#
# lowercased = data['food'].str.lower()     # 统一成小写，使用str.lower()
# lowercased
# Out[101]:
# 0          bacon
# 1    pulled pork
# 2          bacon
# 3       pastrami
# 4    corned beef
# 5          bacon
# 6       pastrame
# 7      honey ham
# 8       nova lox
# Name: food, dtype: object

# data['animal'] = lowercased.map(meat_to_animai)
# data
# Out[104]:
#           food  ounces animal
# 0        bacon     4.0    pig
# 1  pulled pork     3.0    pig
# 2        bacon    12.0    pig
# 3     Pastrami     6.0    cow
# 4  corned beef     7.5    cow
# 5        Bacon     8.0    pig
# 6     pastrame     3.0    NaN
# 7    honey ham     5.0    pig
# 8     nova lox     6.0  salmo
#
# data['food'].map(lambda x: meat_to_animai[x.lower()])  # 这个函数等同于上边的


# 7.2.3 替代值

# data = pd.Series([1. , -999. , 2. , -999. , -1000. , 3.])
# data
# Out[109]:
# 0       1.0
# 1    -999.0
# 2       2.0
# 3    -999.0
# 4   -1000.0
# 5       3.0
# dtype: float64
# data.replace(-999 , np.nan)        # 一次替代一个值
# Out[110]:
# 0       1.0
# 1       NaN
# 2       2.0
# 3       NaN
# 4   -1000.0
# 5       3.0
# dtype: float64
# data.replace([-999 , -1000] , np.nan)    # 使用列表，一次替代多个值
# Out[111]:
# 0    1.0
# 1    NaN
# 2    2.0
# 3    NaN
# 4    NaN
# 5    3.0
# dtype: float64

#
# data.replace([-999 , -1000] , [np.nan , 0])   # 特定值替换
# Out[112]:
# 0    1.0
# 1    NaN
# 2    2.0
# 3    NaN
# 4    0.0
# 5    3.0
# dtype: float64

# data.replace({-999:np.nan , -1000:0})  # 使用字典替换
# Out[113]:
# 0    1.0
# 1    NaN
# 2    2.0
# 3    NaN
# 4    0.0
# 5    3.0
# dtype: float64


# 7.2.4 重命名轴索引


# data = pd.DataFrame(np.arange(12).reshape((3,4)),
#                     index=['Ohio' , 'Colorado' , 'New York'] ,
#                     columns=['one' , 'two' , 'three' , 'four'])
#
# transform = lambda x:x[:4].upper()
# data.index.map(transform)
# Out[116]: Index(['OHIO', 'COLO', 'NEW '], dtype='object')
#
# data.index = data.index.map(transform)
# data
# Out[118]:
#       one  two  three  four
# OHIO    0    1      2     3
# COLO    4    5      6     7
# NEW     8    9     10    11
#
#
# data.rename(index = str.title , columns=str.upper)
# Out[119]:
#       ONE  TWO  THREE  FOUR
# Ohio    0    1      2     3
# Colo    4    5      6     7
# New     8    9     10    11
#
#
# data.rename(index = {'OHIO': 'INDIANA'} ,
#             columns = {'three': 'peekaboo'})      # 替换
#
# Out[6]:
#          one  two  peekaboo  four
# INDIANA    0    1         2     3
# COLO       4    5         6     7
# NEW        8    9        10    11

## 离散化和分箱
#
# ages = [20 , 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
# bins = [18, 25, 35, 60, 100]               # 分组
# cats = pd.cut(ages, bins)                  # 把年龄按bins分组，返回的是每个年龄所对应的箱子
# cats
# Out[10]:
# [(18, 25], (18, 25], (18, 25], (25, 35], (18, 25], ..., (25, 35], (60, 100], (35, 60], (35, 60], (25, 35]]
# Length: 12
# Categories (4, interval[int64]): [(18, 25] < (25, 35] < (35, 60] < (60, 100]]
# cats.codes                  # 返回的是该年龄对应的箱的序列
# Out[11]: array([0, 0, 0, 1, 0, 0, 2, 1, 3, 2, 2, 1], dtype=int8)
# cats.categories
# Out[12]:
# IntervalIndex([(18, 25], (25, 35], (35, 60], (60, 100]],
#               closed='right',
#               dtype='interval[int64]')
# pd.value_counts(cats)               # 计算每一个c箱中有几个内容
# Out[13]:
# (18, 25]     5
# (35, 60]     3
# (25, 35]     3
# (60, 100]    1
# dtype: int64

# pd.cut(ages , [18, 26, 36, 61, 100] , right = False)    # 传入right = False来改变范围那边是封闭的
# Out[14]:
# [[18, 26), [18, 26), [18, 26), [26, 36), [18, 26), ..., [26, 36), [61, 100), [36, 61), [36, 61), [26, 36)]
# Length: 12
# Categories (4, interval[int64]): [[18, 26) < [26, 36) < [36, 61) < [61, 100)]

# group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']    # 给每个箱子命名
# pd.cut(ages, bins, labels=group_names)
# Out[16]:
# [Youth, Youth, Youth, YoungAdult, Youth, ..., YoungAdult, Senior, MiddleAged, MiddleAged, YoungAdult]
# Length: 12
# Categories (4, object): [Youth < YoungAdult < MiddleAged < Senior]

# data = np.random.rand(20)           #
# pd.cut(data, 4, precision=2)      #  4是均匀切成4分，precision=2 把十进制的精度限制在两位
# Out[18]:
# [(0.0094, 0.26], (0.0094, 0.26], (0.5, 0.75], (0.26, 0.5], (0.26, 0.5], ..., (0.0094, 0.26], (0.5, 0.75], (0.0094, 0.26], (0.0094, 0.26], (0.26, 0.5]]
# Length: 20
# Categories (4, interval[float64]): [(0.0094, 0.26] < (0.26, 0.5] < (0.5, 0.75] < (0.75, 0.99]]

# data = np.random.randn(1000)           # 正态分布
# cats = pd.qcut(data , 4)              # 切成4分 ， qcut基于样本分位数进行分箱 ， 获得等长的箱
# cats
# Out[21]:
# [(-3.461, -0.677], (-0.677, -0.0644], (-3.461, -0.677], (0.603, 2.967], (0.603, 2.967], ..., (-0.0644, 0.603], (-3.461, -0.677], (0.603, 2.967], (-0.677, -0.0644], (-0.677, -0.0644]]
# Length: 1000
# Categories (4, interval[float64]): [(-3.461, -0.677] < (-0.677, -0.0644] < (-0.0644, 0.603] <
#                                     (0.603, 2.967]]
# pd.value_counts(cats)
# Out[22]:
# (0.603, 2.967]       250
# (-0.0644, 0.603]     250
# (-0.677, -0.0644]    250
# (-3.461, -0.677]     250              # 箱等长
# dtype: int64


# pd.qcut(data , [0 , 0.1 , 0.5 , 0.9 , 1.])    # 自定义分位数
# Out[23]:
# [(-1.271, -0.0644], (-1.271, -0.0644], (-1.271, -0.0644], (1.178, 2.967], (1.178, 2.967], ..., (-0.0644, 1.178], (-1.271, -0.0644], (-0.0644, 1.178], (-1.271, -0.0644], (-1.271, -0.0644]]
# Length: 1000
# Categories (4, interval[float64]): [(-3.461, -1.271] < (-1.271, -0.0644] < (-0.0644, 1.178] <
#                                     (1.178, 2.967]]


# 7.2.6 检测和过滤异常值

# data = pd.DataFrame(np.random.randn(1000 , 4))    # 正态分布
# data.describe()      # 返回描述统计结果
# Out[25]:
#                  0            1            2            3
# count  1000.000000  1000.000000  1000.000000  1000.000000
# mean      0.041107    -0.000505     0.003680    -0.020282
# std       0.987768     1.008360     1.024961     0.987928
# min      -3.243074    -3.535812    -2.836718    -2.940010
# 25%      -0.609088    -0.652666    -0.694720    -0.712108
# 50%       0.044689    -0.035631     0.003289    -0.068262
# 75%       0.733067     0.677481     0.674784     0.672709
# max       3.177820     3.267438     3.723802     3.692419
# col = data[2]
# col[np.abs(col)>3]
# Out[27]:
# 328    3.723802
# Name: 2, dtype: float64
#
# data[(np.abs(data) > 3).any(1)]     # 选出所有值大于3或小于-3的行， 使用any方法
# Out[28]:
#             0         1         2         3
# 14   3.112003  0.265680 -1.021908  1.291247
# 182 -3.067911 -0.837200 -0.213498 -1.354600
# 328 -1.384057  1.217438  3.723802  0.568977
# 411 -3.243074  0.822246 -0.355773  0.752823
# 480  3.174715  0.351713 -0.660785 -0.499990
# 761  3.177820  0.306630 -1.520944 -1.279747
# 764  0.906007 -0.048642 -0.138435  3.692419
# 836 -0.213079 -3.535812 -0.787509 -0.959970
# 928  0.222027  3.267438 -1.098359  0.267384
# 933  0.556279  1.290485  2.328871  3.012376


# data[np.abs(data) > 3] = np.sign(data) * 3     # 限制-3到3之间的数值，np.sign(data)根据数据中的正负值分别生成1和-1的数值
# data.describe()
# Out[30]:
#                  0            1            2            3
# count  1000.000000  1000.000000  1000.000000  1000.000000
# mean      0.040953    -0.000237     0.002956    -0.020986
# std       0.985343     1.005786     1.022584     0.985525
# min      -3.000000    -3.000000    -2.836718    -2.940010
# 25%      -0.609088    -0.652666    -0.694720    -0.712108
# 50%       0.044689    -0.035631     0.003289    -0.068262
# 75%       0.733067     0.677481     0.674784     0.672709
# max       3.000000     3.000000     3.000000     3.000000

# np.sign(data).head()
# Out[31]:
#      0    1    2    3
# 0 -1.0  1.0 -1.0 -1.0
# 1  1.0  1.0  1.0  1.0
# 2  1.0 -1.0 -1.0  1.0
# 3 -1.0  1.0 -1.0  1.0
# 4  1.0 -1.0 -1.0 -1.0


## 7.2.7 置换和随机抽样

#
# df = pd.DataFrame(np.arange(5 * 4).reshape((5,4)))
# sampler = np.random.permutation(5)             # 用np.random.permutation 对数据置换或者随机重排，5是自定义的轴长度
# sampler
# Out[34]: array([1, 4, 0, 2, 3])

# df
# Out[35]:
#     0   1   2   3
# 0   0   1   2   3
# 1   4   5   6   7
# 2   8   9  10  11
# 3  12  13  14  15
# 4  16  17  18  19
# df.take(sampler)          # 把上边的整数数组用于行索引
# Out[36]:
#     0   1   2   3
# 1   4   5   6   7
# 4  16  17  18  19
# 0   0   1   2   3
# 2   8   9  10  11
# 3  12  13  14  15

# df.sample(n=3)        # 选出不含有替代值（不允许重复选择）的随机子集
# Out[37]:
#     0   1   2   3
# 0   0   1   2   3
# 3  12  13  14  15
# 1   4   5   6   7

# choices = pd.Series([5, 7, -1, 6, 4])
# draws = choices.sample(n=10 , replace = True)      # 传入replace = True，就可以重复选择，n=10重复选10次
# draws
# Out[40]:
# 3    6
# 4    4
# 4    4
# 0    5
# 3    6
# 4    4
# 3    6
# 0    5
# 4    4
# 3    6
# dtype: int64



#  7.2.8 计算指标/虚拟变量


# df = pd.DataFrame({'key':['b', 'b', 'a', 'c', 'a', 'b'],'data1':range(6)})
# pd.get_dummies(df['key'])
# Out[42]:
#    a  b  c
# 0  0  1  0
# 1  0  1  0
# 2  1  0  0
# 3  0  0  1
# 4  1  0  0
# 5  0  1  0

# dummies = pd.get_dummies(df['key'] , prefix = 'key')     # 列上加上前缀，与其他数据合并
# df_with_dummy = df[['data1']].join(dummies)
# df_with_dummy
# Out[45]:
#    data1  key_a  key_b  key_c
# 0      0      0      1      0
# 1      1      0      1      0
# 2      2      1      0      0
# 3      3      0      0      1
# 4      4      1      0      0
# 5      5      0      1      0

# mnames = ['movie_id', 'title', 'genres']
# movies = pd.read_table('D:\data_py\pydata-book-2nd-edition\datasets\movielens\movies.dat' , sep = '::' ,
#                        header = None , names = mnames)
#
# movies[:10]
# Out[50]:
#    movie_id                               title                        genres
# 0         1                    Toy Story (1995)   Animation|Children's|Comedy
# 1         2                      Jumanji (1995)  Adventure|Children's|Fantasy
# 2         3             Grumpier Old Men (1995)                Comedy|Romance
# 3         4            Waiting to Exhale (1995)                  Comedy|Drama
# 4         5  Father of the Bride Part II (1995)                        Comedy
# 5         6                         Heat (1995)         Action|Crime|Thriller
# 6         7                      Sabrina (1995)                Comedy|Romance
# 7         8                 Tom and Huck (1995)          Adventure|Children's
# 8         9                 Sudden Death (1995)                        Action
# 9        10                    GoldenEye (1995)     Action|Adventure|Thriller


# all_genres = []
# for x in movies.genres:
#     all_genres.extend(x.split('|'))             # .split拆分字符串
# genres = pd.unique(all_genres)                  # 只取不重复的
# genres
# Out[53]:
# array(['Animation', "Children's", 'Comedy', 'Adventure', 'Fantasy',
#        'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror',
#        'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir',
#        'Western'], dtype=object)


# zero_matrix = np.zeros((len(movies) , len(genres)))
# dummies = pd.DataFrame(zero_matrix , columns = genres)
# gen = movies.genres[0]
# gen.split('|')
# Out[58]: ['Animation', "Children's", 'Comedy']
# dummies.columns.get_indexer(gen.split('|'))             # 使用.columns 计算列指标
# Out[59]: array([0, 1, 2], dtype=int64)

# .loc根据这些指标来设置值

# for i , gen in enumerate(movies.genres):
#     indices = dummies.columns.get_indexer(gen.split('|'))
#     dummies.iloc[i , indices] = 1
#
# movies_windic = movies.join(dummies.add_prefix('Genre_'))
# movies_windic.iloc[0]
# Out[62]:
# movie_id                                       1
# title                           Toy Story (1995)
# genres               Animation|Children's|Comedy
# Genre_Animation                                1
# Genre_Children's                               1
# Genre_Comedy                                   1
# Genre_Adventure                                0
# Genre_Fantasy                                  0
# Genre_Romance                                  0
# Genre_Drama                                    0
# Genre_Action                                   0
# Genre_Crime                                    0
# Genre_Thriller                                 0
# Genre_Horror                                   0
# Genre_Sci-Fi                                   0
# Genre_Documentary                              0
# Genre_War                                      0
# Genre_Musical                                  0
# Genre_Mystery                                  0
# Genre_Film-Noir                                0
# Genre_Western                                  0
# Name: 0, dtype: object


# np.random.seed(12345)               # 设置随机种子
# values = np.random.rand(10)
# values
# Out[65]:
# array([0.92961609, 0.31637555, 0.18391881, 0.20456028, 0.56772503,
#        0.5955447 , 0.96451452, 0.6531771 , 0.74890664, 0.65356987])
# bins = [0 , 0.2 , 0.4 , 0.6 , 0.8 , 1]
# pd.get_dummies(pd.cut(values , bins))
# Out[67]:
#    (0.0, 0.2]  (0.2, 0.4]  (0.4, 0.6]  (0.6, 0.8]  (0.8, 1.0]
# 0           0           0           0           0           1
# 1           0           1           0           0           0
# 2           1           0           0           0           0
# 3           0           1           0           0           0
# 4           0           0           1           0           0
# 5           0           0           1           0           0
# 6           0           0           0           0           1
# 7           0           0           0           1           0
# 8           0           0           0           1           0
# 9           0           0           0           1           0


# 7.3字符串操作


# val = 'a,b, guido'
# val.split(',')                 # 使用，把val分割
# Out[4]: ['a', 'b', ' guido']

# pieces = [x.strip() for x in val.split(',')]          # strip和split一起用，用来清除空格
# pieces
# Out[6]: ['a', 'b', 'guido']

# first , second , third = pieces
# first + '::' + second + '::' + third          # 把这些子字符串用符号连在一起
# Out[8]: 'a::b::guido'

# '::'.join(pieces)                              # 更简洁的方法
# Out[9]: 'a::b::guido'

## 检测子字符串的方法
# 'guido' in val
# Out[10]: True
# val.index(',')            # index 和find 的区别是，如果index在字符串中没找到的话，会显示异常，find则会抛出一个-1
# Out[11]: 1
# val.find(':')
# Out[12]: -1

# val.count(',')       # 返回的是计数
# Out[13]: 2

# val.replace(',' , '::')   # 用后边的字符替代前边的字符
# Out[14]: 'a::b:: guido'
# val.replace(',' , '')
# Out[15]: 'ab guido'


# 7.3.2正则表达式

# re模块： 模式匹配、替代、拆分

# text = " foo            bar\t  baz \tqux"
# re.split('\s+' , text)                              # 以空格（\s+）,+表示重复，就是多个空格
# Out[21]: ['', 'foo', 'bar', 'baz', 'qux']
# text = "  foo            bar\t  baz \tqux"
# re.split('\s+' , text)
# Out[23]: ['', 'foo', 'bar', 'baz', 'qux']
# text = "foo            bar\t  baz \tqux"
# re.split('\s+' , text)
# Out[27]: ['foo', 'bar', 'baz', 'qux']

# regex = re.compile('\s+')                  # 使用.compile 定义一个正则表达式，之后调用
# regex.split(text)
# Out[29]: ['foo', 'bar', 'baz', 'qux']

# regex.findall(text)
# #.findall 可以获得一个所有匹配正则表达式的模式的列表
## .search仅返回第一个匹配项
# Out[30]: ['            ', '\t  ', ' \t']

# text = """Dave dave@google.com
# Steve steve@gmail.com
# Rob rob@gmail.com
# Ryan ryan@yahoo.com
# """
#
# pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
# # 正则表达式的一些规则
# # [A-Z]：匹配任何大写字母
# # [a-z]:匹配任何小写字母
# # [0-9]:匹配任何数字
# # [Pp]ython : 匹配Python或python
# # [aeiou]:匹配任何一个小写元音
# # [a-zA-Z0-9] :匹配上述任何一个
# # [^aeiou] : ^ 这个符号是取反
# regex = re.compile(pattern, flags=re.IGNORECASE)    # re.IGNORECASE  使正则表达式不分大小写
# regex.findall(text)
# Out[36]: ['dave@google.com', 'steve@gmail.com', 'rob@gmail.com', 'ryan@yahoo.com']

# m = regex.search(text)
# m
# Out[38]: <re.Match object; span=(5, 20), match='dave@google.com'>
# text[m.start():m.end()]
# Out[39]: 'dave@google.com'

# print(regex.match(text))   # .match只在模式出现于字符串起始位置时进行匹配，如果没有匹配到，就返回None
# None

# print(regex.sub('REDACTED' , text))      # 把regex代表的正则表达式替代为REDACTTED
# Dave REDACTED
# Steve REDACTED
# Rob REDACTED
# Ryan REDACTED

# pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
# regex = re.compile(pattern, flags=re.IGNORECASE)
# m = regex.match('wesm@bright.net')
# m.group()
# Out[6]: 'wesm@bright.net'

# pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'   # 用括号把正则表达式的部分括起来，用.groups()可以返回元组
# regex = re.compile(pattern, flags=re.IGNORECASE)
# m = regex.match('wesm@bright.net')
# m.groups()
# Out[12]: ('wesm', 'bright', 'net')

# regex.findall(text)             # 当模式可以分组的时候返回的是包含元组的列表
# Out[15]:
# [('dave', 'google', 'com'),
#  ('steve', 'gmail', 'com'),
#  ('rob', 'gmail', 'com'),
#  ('ryan', 'yahoo', 'com')]
#
# print(regex.sub(r'Username:\1 , Domain:\2 , Suffix:\3' , text))       # .sub 可以使用\1   \2  \3来访问每一匹配对象的分组
# Dave Username:dave , Domain:google , Suffix:com
# Steve Username:steve , Domain:gmail , Suffix:com
# Rob Username:rob , Domain:gmail , Suffix:com
# Ryan Username:ryan , Domain:yahoo , Suffix:com

# 7.3.3 pandas 中的向量化字符串函数

# data = {'Dave': 'dave@google.com' , 'Steve':'steve@gmail.com' , 'Rob':'rob@gmail.com' , 'Wes':np.nan}
# data = pd.Series(data)
# data
# Out[22]:
# Dave     dave@google.com
# Steve    steve@gmail.com
# Rob        rob@gmail.com
# Wes                  NaN
# dtype: object
#
# data.isnull()
# Out[23]:
# Dave     False
# Steve    False
# Rob      False
# Wes       True
# dtype: bool

#
# data.str.contains('gmail')         # .str.contains('  ') 用来检测是否包含
# Out[24]:
# Dave     False
# Steve     True
# Rob       True
# Wes        NaN
# dtype: object
# pattern
# Out[25]: '([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\\.([A-Z]{2,4})'
# data.str.findall(pattern , flags = re.IGNORECASE)
# Out[26]:
# Dave     [(dave, google, com)]
# Steve    [(steve, gmail, com)]
# Rob        [(rob, gmail, com)]
# Wes                        NaN
# dtype: object

# matches = data.str.match(pattern , flags = re.IGNORECASE)
# matches
# Out[28]:
# Dave     True
# Steve    True
# Rob      True
# Wes       NaN
# dtype: object
# matches.str.get(1)
# Out[29]:
# Dave    NaN
# Steve   NaN
# Rob     NaN
# Wes     NaN
# dtype: float64

#
# matches.str[0]
# Out[31]:
# Dave    NaN
# Steve   NaN
# Rob     NaN
# Wes     NaN
# dtype: float64


# data.str[:5]     # 向量化切片
# Out[32]:
# Dave     dave@
# Steve    steve
# Rob      rob@g
# Wes        NaN
# dtype: object
















